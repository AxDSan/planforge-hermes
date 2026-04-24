"""
PlanForge Mini App API Server

A lightweight HTTP server that serves the Telegram Mini App
and provides API endpoints for reading .planning/ files.

Run: python miniapp_server.py
"""

import os
import json
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Config
PROJECT_DIR = os.getcwd()  # Directory where .planning/ lives
MINIAPP_DIR = os.path.join(os.path.dirname(__file__), "telegram-miniapp")
PORT = 8765


class PlanForgeHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=MINIAPP_DIR, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        
        # API endpoints
        if parsed.path == '/api/planforge/status':
            self._send_json(self._get_status())
            return
        
        if parsed.path == '/api/planforge/phases':
            self._send_json(self._get_phases())
            return
        
        # Serve static files (index.html, app.js, etc.)
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        
        if parsed.path == '/api/planforge/task':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)
            result = self._update_task(data)
            self._send_json(result)
            return
        
        self.send_error(404)

    def _send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _get_status(self):
        """Read STATE.md and ROADMAP.md to build status response."""
        planning_dir = os.path.join(PROJECT_DIR, '.planning')
        
        if not os.path.exists(planning_dir):
            return {"error": "No .planning/ found"}
        
        # Read STATE.md
        state_file = os.path.join(planning_dir, 'STATE.md')
        current_phase = 0
        status_text = "Unknown"
        
        if os.path.exists(state_file):
            with open(state_file) as f:
                content = f.read()
            match = re.search(r'\*\*Current Phase:\*\*\s*(\d+)', content)
            if match:
                current_phase = int(match.group(1))
            match = re.search(r'\*\*Current Phase:\*\*\s*\d+\s*[-–—]\s*(.+)', content)
            if match:
                status_text = match.group(1).strip()
        
        # Read ROADMAP.md
        roadmap_file = os.path.join(planning_dir, 'ROADMAP.md')
        phases = []
        
        if os.path.exists(roadmap_file):
            with open(roadmap_file) as f:
                content = f.read()
            
            # Parse table rows
            for line in content.split('\n'):
                if '|' in line and 'Phase' in line:
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 5:
                        try:
                            num = int(parts[1].replace('Phase', '').strip())
                            name = parts[2]
                            status_str = parts[3]
                            
                            # Map status emoji to status string
                            status = 'pending'
                            if '✅' in status_str or 'Complete' in status_str:
                                status = 'completed'
                            elif '🔄' in status_str or 'Progress' in status_str:
                                status = 'in_progress'
                            elif '⚠️' in status_str or 'Blocked' in status_str:
                                status = 'blocked'
                            
                            # Calculate progress
                            progress = 0
                            if status == 'completed':
                                progress = 100
                            elif status == 'in_progress':
                                # Try to read plan file for better progress
                                plan_file = os.path.join(planning_dir, f'{num:02d}-1-PLAN.md')
                                if os.path.exists(plan_file):
                                    with open(plan_file) as pf:
                                        plan_content = pf.read()
                                    total_tasks = len(re.findall(r'- \[.\]', plan_content))
                                    done_tasks = len(re.findall(r'- \[x\]', plan_content))
                                    if total_tasks > 0:
                                        progress = int(done_tasks / total_tasks * 100)
                                else:
                                    progress = 50
                            
                            phases.append({
                                'number': num,
                                'name': name,
                                'status': status,
                                'progress': progress
                            })
                        except (ValueError, IndexError):
                            pass
        
        # Read PROJECT.md for project name
        project_file = os.path.join(planning_dir, 'PROJECT.md')
        project_name = 'Untitled Project'
        if os.path.exists(project_file):
            with open(project_file) as f:
                first_line = f.readline().strip()
                if first_line.startswith('# '):
                    project_name = first_line[2:]
        
        # Check lock state
        lock_file = os.path.expanduser('~/.hermes/planforge_state.json')
        locked = False
        if os.path.exists(lock_file):
            with open(lock_file) as f:
                lock_data = json.load(f)
            locked = lock_data.get('locked', False)
        
        return {
            'project': project_name,
            'currentPhase': current_phase,
            'status': status_text,
            'locked': locked,
            'phases': sorted(phases, key=lambda p: p['number'])
        }

    def _get_phases(self):
        """Get detailed phase data."""
        status = self._get_status()
        return status.get('phases', [])

    def _update_task(self, data):
        """Update a task's completion status in a plan file."""
        phase = data.get('phase')
        task_index = data.get('taskIndex')
        completed = data.get('completed', False)
        
        if phase is None or task_index is None:
            return {'error': 'Missing phase or taskIndex'}
        
        planning_dir = os.path.join(PROJECT_DIR, '.planning')
        plan_file = os.path.join(planning_dir, f'{phase:02d}-1-PLAN.md')
        
        if not os.path.exists(plan_file):
            return {'error': f'Plan file not found: {plan_file}'}
        
        with open(plan_file) as f:
            lines = f.readlines()
        
        # Find and update the task
        task_count = 0
        for i, line in enumerate(lines):
            if re.match(r'- \[.\]', line):
                if task_count == task_index:
                    marker = '[x]' if completed else '[ ]'
                    lines[i] = re.sub(r'- \[.\]', f'- {marker}', line, count=1)
                    break
                task_count += 1
        
        with open(plan_file, 'w') as f:
            f.writelines(lines)
        
        return {'success': True, 'phase': phase, 'task': task_index, 'completed': completed}


def run_server(port=PORT):
    server = HTTPServer(('0.0.0.0', port), PlanForgeHandler)
    print(f"PlanForge Mini App server running on http://localhost:{port}")
    print(f"Serving files from: {MINIAPP_DIR}")
    print(f"Reading .planning/ from: {PROJECT_DIR}")
    print("\nTelegram WebApp URL: http://localhost:{port}/index.html")
    print("\nPress Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == '__main__':
    run_server()
