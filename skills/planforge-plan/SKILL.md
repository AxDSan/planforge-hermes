---
name: planforge-plan
description: Generate or review a phase plan for a PlanForge project.
trigger: planforge plan, create plan, phase planning
---

# PlanForge Plan

Create a structured plan for a project phase.

## Usage

```
/planforge-plan <phase_number>
```

## Plan structure

Plans are XML-structured with:
- **Objective** — What this phase accomplishes
- **Waves** — Parallelizable task groups
- **Dependencies** — Prerequisites
- **Acceptance Criteria** — Exit gates
- **Risks** — Known blockers

## Example

```
/planforge-plan 1
```

Creates `.planning/01-1-PLAN.md`.

## Next steps

Run `/planforge-execute 1` to start execution.
