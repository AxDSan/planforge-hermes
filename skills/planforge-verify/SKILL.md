---
name: planforge-verify
description: Verify phase completion against acceptance criteria.
trigger: planforge verify, check completion, validate phase
---

# PlanForge Verify

Verify that a phase meets its acceptance criteria.

## Usage

```
/planforge-verify <phase_number>
```

## Checks

- All tasks marked complete
- All acceptance criteria satisfied
- No blockers remaining

## Results

- ✅ **Pass** — Phase complete, ready to ship
- ⚠️ **Partial** — Some items remaining
- ❌ **Fail** — Major blockers found

## Next steps

- Pass: `/planforge-ship`
- Partial: Continue execution
- Fail: Re-plan phase
