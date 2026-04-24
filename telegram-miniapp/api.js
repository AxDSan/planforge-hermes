/**
 * PlanForge Mini App — API Bridge
 * 
 * Reads .planning/ files from the project directory.
 * In production, this should call a small backend API
 * that has filesystem access. For demo, it can use
 * Telegram's CloudStorage or a local server.
 */

const API = {
  // Base URL for the PlanForge API server
  // Set this to your Hermes webhook or local server
  baseUrl: localStorage.getItem('planforge_api_url') || 'http://localhost:8765',

  /**
   * Fetch project status from .planning/STATE.md and ROADMAP.md
   */
  async getStatus() {
    try {
      const res = await fetch(`${this.baseUrl}/api/planforge/status`);
      if (!res.ok) throw new Error('Failed to fetch');
      return await res.json();
    } catch (e) {
      // Fallback: return demo data
      console.warn('API unavailable, using demo data');
      return this._getDemoData();
    }
  },

  /**
   * Update a task's completion status
   */
  async updateTask(phase, taskIndex, completed) {
    try {
      const res = await fetch(`${this.baseUrl}/api/planforge/task`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phase, taskIndex, completed })
      });
      return await res.json();
    } catch (e) {
      return { error: e.message };
    }
  },

  /**
   * Send a command to Hermes via the bot
   */
  async sendCommand(command) {
    // This would integrate with your Telegram bot's API
    // to trigger Hermes commands like /planforge-status
    Telegram.WebApp.sendData(JSON.stringify({ command }));
  },

  /**
   * Demo data for testing without backend
   */
  _getDemoData() {
    return {
      project: 'FluxSpeak v3',
      currentPhase: 2,
      locked: true,
      phases: [
        { number: 1, name: 'Research & Context', status: 'completed', progress: 100 },
        { number: 2, name: 'Planning', status: 'in_progress', progress: 60 },
        { number: 3, name: 'Execution', status: 'pending', progress: 0 },
        { number: 4, name: 'Verification', status: 'pending', progress: 0 },
        { number: 5, name: 'Shipping', status: 'pending', progress: 0 }
      ]
    };
  }
};
