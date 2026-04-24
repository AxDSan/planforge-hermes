"""PlanForge /planforge-verify command — verify phase completion."""

from typing import Any
import os
import re


def run(ctx: Any, args: str) -> str:
    phase = _parse_phase(args)
    if phase is None:
        phase = _detect_current_phase()
        if phase is None:
            return "Usage: `/planforge-verify <phase_number>`"

    cwd = os.getcwd()
    planning_dir = os.path.join(cwd, ".planning")
    plan_file = os.path.join(planning_dir, f"{phase:02d}-1-PLAN.md")

    if not os.path.exists(plan_file):
        return f"❌ No plan found for phase {phase}."

    with open(plan_file) as f:
        plan_content = f.read()

    criteria = _extract_criteria(plan_content)
    tasks = _extract_tasks(plan_content)

    # Simple heuristic: count checked items
    checked_tasks = len(re.findall(r"- \[x\] .+", plan_content))
    total_tasks = len(tasks)

    checked_criteria = len(re.findall(r"- \[x\] .+", plan_content.split("## Acceptance Criteria")[1] if "## Acceptance Criteria" in plan_content else ""))
    total_criteria = len(criteria)

    # Unlock phase
    from . import state
    state.unlock_phase()

    # Update STATE.md
    _update_state(planning_dir, phase, "Verified" if checked_criteria >= total_criteria else "Partial")

    result = f"📊 **Phase {phase} Verification**\n\n"
    result += f"Tasks: {checked_tasks}/{total_tasks} complete\n"
    result += f"Criteria: {checked_criteria}/{total_criteria} passed\n\n"

    if checked_criteria >= total_criteria and total_criteria > 0:
        result += "✅ **Phase complete!** Ready to ship.\n"
        result += f"Run `/planforge-ship` to create PR."
    else:
        result += "⚠️ Phase incomplete. Review remaining items."

    return result


def _parse_phase(args: str) -> int | None:
    try:
        return int(args.strip().split()[0])
    except (ValueError, IndexError):
        return None


def _detect_current_phase() -> int | None:
    from . import state
    return state.get_current_phase()


def _extract_criteria(content: str) -> list[str]:
    criteria = []
    in_criteria = False
    for line in content.split("\n"):
        if "## Acceptance Criteria" in line:
            in_criteria = True
            continue
        if in_criteria and line.startswith("##"):
            break
        if in_criteria:
            match = re.match(r"- \[.\] (.+)", line)
            if match:
                criteria.append(match.group(1))
    return criteria


def _extract_tasks(content: str) -> list[str]:
    tasks = []
    for line in content.split("\n"):
        match = re.match(r"- \[.\] (.+)", line)
        if match:
            tasks.append(match.group(1))
    return tasks


def format_result(tool_name: str, result: Any) -> Any:
    """Hook: format tool result for verification."""
    return result


def parse_terminal_output(output: str) -> str:
    """Hook: parse terminal output for checklist items."""
    return output


def _update_state(planning_dir: str, phase: int, status: str) -> None:
    state_file = os.path.join(planning_dir, "STATE.md")
    if os.path.exists(state_file):
        with open(state_file) as f:
            content = f.read()
        content = re.sub(r"\*\*Current Phase:\*\* .*", f"**Current Phase:** {phase} — {status}", content)
        with open(state_file, "w") as f:
            f.write(content)
