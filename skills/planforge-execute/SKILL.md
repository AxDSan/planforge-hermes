---
name: planforge-execute
description: Execute a phase plan using Hermes tools.
trigger: planforge execute, run phase, execute tasks
---

# PlanForge Execute

Execute tasks from a phase plan.

## Usage

```
/planforge-execute <phase_number>
```

## How it works

1. Parses `.planning/XX-1-PLAN.md`
2. Locks phase (prevents concurrent execution)
3. Presents task list
4. User completes tasks via Hermes tools
5. Run `/planforge-verify` when done

## Parallel execution

Use `delegate_task` for independent tasks within a wave.

## Next steps

Run `/planforge-verify <phase>` to verify completion.
