"""PlanForge /planforge-status command — show project status and progress."""

from typing import Any
import os
import re


def run(ctx: Any) -> str:
    cwd = os.getcwd()
    planning_dir = os.path.join(cwd, ".planning")

    if not os.path.exists(planning_dir):
        return "❌ No `.planning/` found. Run `/planforge-init` first."

    # Read STATE.md
    state_file = os.path.join(planning_dir, "STATE.md")
    state_content = ""
    if os.path.exists(state_file):
        with open(state_file) as f:
            state_content = f.read()

    # Read ROADMAP.md
    roadmap_file = os.path.join(planning_dir, "ROADMAP.md")
    roadmap_content = ""
    if os.path.exists(roadmap_file):
        with open(roadmap_file) as f:
            roadmap_content = f.read()

    # Extract current phase from STATE.md
    current_phase = "Unknown"
    match = re.search(r"\*\*Current Phase:\*\* (.+)", state_content)
    if match:
        current_phase = match.group(1).strip()

    # Count completed phases from ROADMAP
    completed = len(re.findall(r"✅|🟢|Complete", roadmap_content))
    total = len(re.findall(r"Phase \d+", roadmap_content))

    from . import state
    locked = state.is_phase_locked()

    result = f"📊 **PlanForge Status**\n\n"
    result += f"Project: `{os.path.basename(cwd)}`\n"
    result += f"Current: {current_phase}\n"
    result += f"Progress: {completed}/{total} phases complete\n"
    result += f"Locked: {"🔒 Yes" if locked else "🔓 No"}\n"

    if locked:
        result += f"\nExecuting Phase {state.get_current_phase()}..."

    return result
