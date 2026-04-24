---
name: planforge-init
description: Initialize a new PlanForge project with .planning/ structure.
trigger: planforge init, initialize project, start planning
---

# PlanForge Init

Initialize a new spec-driven project.

## Usage

```
/planforge-init "Project Name"
```

## What it creates

- `.planning/PROJECT.md` — Vision, goals, constraints
- `.planning/REQUIREMENTS.md` — v1/v2/out-of-scope
- `.planning/ROADMAP.md` — Phase breakdown
- `.planning/STATE.md` — Current position tracker
- `.planning/config.json` — Workflow preferences

## Next steps

Run `/planforge-plan 1` to create Phase 1 plan.
