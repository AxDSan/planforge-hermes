"""PlanForge /planforge-plan command — generate or review phase plans."""

from typing import Any
import os
import re
import logging

_logger = logging.getLogger("planforge")


def run(ctx: Any, args: str) -> str:
    phase = _parse_phase(args)
    if phase is None:
        return "Usage: `/planforge-plan <phase_number>`"

    cwd = os.getcwd()
    planning_dir = os.path.join(cwd, ".planning")
    if not os.path.exists(planning_dir):
        return "❌ No `.planning/` found. Run `/planforge-init` first."

    plan_file = os.path.join(planning_dir, f"{phase:02d}-1-PLAN.md")

    if os.path.exists(plan_file):
        with open(plan_file) as f:
            content = f.read()
        return f"📋 **Phase {phase} Plan** (existing)\n\n```\n{content[:800]}\n```\n\nTo re-plan, delete `{plan_file}` and run again."

    # Generate plan template
    plan_content = _generate_plan_template(phase)
    with open(plan_file, "w") as f:
        f.write(plan_content)

    # Update STATE.md
    _update_state(planning_dir, phase, "Planning")

    _logger.info(f"Created plan for phase {phase}")
    return f"✅ **Phase {phase} Plan** created at `{plan_file}`\n\nPreview:\n```\n{plan_content[:600]}\n```\n\nEdit the file, then run `/planforge-execute {phase}`."


def _parse_phase(args: str) -> int | None:
    try:
        return int(args.strip().split()[0])
    except (ValueError, IndexError):
        return None


def _generate_plan_template(phase: int) -> str:
    return f"""# Phase {phase} Plan

## Objective
<!-- What this phase accomplishes -->

## Waves

### Wave 1
- [ ] Task 1: <!-- description -->
- [ ] Task 2: <!-- description -->

### Wave 2
- [ ] Task 3: <!-- description -->
- [ ] Task 4: <!-- description -->

## Dependencies
- Phase {phase-1} complete (if applicable)

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Risks
- 

## Notes
- 
"""


def _update_state(planning_dir: str, phase: int, status: str) -> None:
    state_file = os.path.join(planning_dir, "STATE.md")
    if os.path.exists(state_file):
        with open(state_file) as f:
            content = f.read()
        content = re.sub(r"\*\*Current Phase:\*\* .*", f"**Current Phase:** {phase} — {status}", content)
        with open(state_file, "w") as f:
            f.write(content)
