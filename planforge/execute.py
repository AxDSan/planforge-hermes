"""PlanForge /planforge-execute command — execute phase tasks via Hermes tools."""

from typing import Any
import os
import re


def run(ctx: Any, args: str) -> str:
    phase = _parse_phase(args)
    if phase is None:
        return "Usage: `/planforge-execute <phase_number>`"

    cwd = os.getcwd()
    planning_dir = os.path.join(cwd, ".planning")
    plan_file = os.path.join(planning_dir, f"{phase:02d}-1-PLAN.md")

    if not os.path.exists(plan_file):
        return f"❌ No plan found for phase {phase}. Run `/planforge-plan {phase}` first."

    from . import state
    if state.is_phase_locked():
        return f"⚠️ Phase {state.get_current_phase()} is already executing. Finish it first."

    with open(plan_file) as f:
        plan_content = f.read()

    tasks = _extract_tasks(plan_content)
    if not tasks:
        return "⚠️ No tasks found in plan. Check the PLAN.md format."

    state.lock_phase(cwd, phase)

    # Update STATE.md
    _update_state(planning_dir, phase, "Executing")

    ctx.log.info(f"Executing phase {phase} with {len(tasks)} tasks")

    # Build execution summary
    summary = f"🚀 **Phase {phase} Execution Started**\n\n"
    summary += f"Found {len(tasks)} tasks:\n"
    for i, task in enumerate(tasks, 1):
        summary += f"{i}. {task}\n"
    summary += "\nUse Hermes tools to complete each task. Run `/planforge-verify {phase}` when done."

    return summary


def _parse_phase(args: str) -> int | None:
    try:
        return int(args.strip().split()[0])
    except (ValueError, IndexError):
        return None


def _extract_tasks(content: str) -> list[str]:
    tasks = []
    for line in content.split("\n"):
        match = re.match(r"- \[ \] (.+)", line)
        if match:
            tasks.append(match.group(1))
    return tasks


def _update_state(planning_dir: str, phase: int, status: str) -> None:
    state_file = os.path.join(planning_dir, "STATE.md")
    if os.path.exists(state_file):
        with open(state_file) as f:
            content = f.read()
        content = re.sub(r"\*\*Current Phase:\*\* .*", f"**Current Phase:** {phase} — {status}", content)
        with open(state_file, "w") as f:
            f.write(content)
