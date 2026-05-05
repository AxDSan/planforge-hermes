"""PlanForge /planforge-init command — bootstrap .planning/ structure."""

from typing import Any
import os
import logging

_logger = logging.getLogger("planforge")


def run(ctx: Any, args: str) -> str:
    project_name = args.strip().strip('"') if args else "Untitled Project"
    cwd = os.getcwd()
    planning_dir = os.path.join(cwd, ".planning")

    if os.path.exists(planning_dir):
        return f"⚠️ .planning/ already exists in {cwd}. Use `/planforge-status` to check progress."

    os.makedirs(planning_dir, exist_ok=True)

    # PROJECT.md
    with open(os.path.join(planning_dir, "PROJECT.md"), "w") as f:
        f.write(f"""# {project_name}

## Vision
<!-- Describe the end goal -->

## Goals
1. 
2. 
3. 

## Constraints
- 

## Out of Scope (v1)
- 
""")

    # REQUIREMENTS.md
    with open(os.path.join(planning_dir, "REQUIREMENTS.md"), "w") as f:
        f.write("""# Requirements

## v1 (MVP)
- 

## v2 (Post-MVP)
- 

## Out of Scope
- 
""")

    # ROADMAP.md
    with open(os.path.join(planning_dir, "ROADMAP.md"), "w") as f:
        f.write("""# Roadmap

| Phase | Name | Status | Exit Criteria |
|-------|------|--------|---------------|
| 1 | Research & Context | 🔲 Not Started | Context doc complete |
| 2 | Planning | 🔲 Not Started | PLAN.md approved |
| 3 | Execution | 🔲 Not Started | All waves complete |
| 4 | Verification | 🔲 Not Started | All criteria pass |
| 5 | Shipping | 🔲 Not Started | PR merged |
""")

    # STATE.md
    with open(os.path.join(planning_dir, "STATE.md"), "w") as f:
        f.write("""# State

**Current Phase:** 0 — Not Started
**Status:** Ready to begin
**Last Updated:** 

## Decisions
- 

## Blockers
- None

## Notes
- 
""")

    # config.json
    with open(os.path.join(planning_dir, "config.json"), "w") as f:
        f.write("""{
  "version": "1.0",
  "strict_mode": true,
  "auto_verify": false,
  "max_waves": 5
}
""")

    _logger.info(f"Initialized PlanForge project: {project_name}")
    return f"✅ PlanForge initialized: **{project_name}**\n📁 `.planning/` created in `{cwd}`\n\nNext: `/planforge-plan 1` to start Phase 1."
