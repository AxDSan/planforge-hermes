# Hermes Plugin: PlanForge

A spec-driven development planning plugin for Hermes Agent, inspired by GSD (Get Shit Done) and fully compatible with the `.planning/` file format.

## What is PlanForge?

PlanForge brings structured, phase-based project planning directly into Hermes. It creates a bridge between high-level project vision and executable development tasks, all while leveraging Hermes' multi-platform delivery, cron jobs, and tool ecosystem.

## Philosophy

> "Fail to plan, plan to fail." — PlanForge ensures every line of code traces back to a requirement.

PlanForge is **not** a replacement for Hermes' agentic capabilities. It is a **force multiplier** — adding structure, traceability, and verification to the agent's execution loop.

## Key Features

- **Phase-based planning** — Break projects into manageable phases with clear entry/exit criteria
- **XML-structured plans** — Machine-readable task definitions with dependencies and acceptance criteria
- **Wave execution** — Parallel task execution within phases via Hermes' `delegate_task`
- **Verification gates** — Every phase must pass verification before proceeding
- **File-based bridge** — All state lives in `.planning/` files, version-controllable and portable
- **Dashboard integration** — Visual roadmap progress in the Hermes web dashboard
- **Multi-platform** — Plan and execute from Telegram, Discord, Slack, or CLI

## Commands

| Command | Description |
|---------|-------------|
| `/planforge-init "Project Name"` | Initialize a new project with `.planning/` structure |
| `/planforge-plan <phase>` | Generate or review a phase plan |
| `/planforge-execute <phase>` | Execute a phase's tasks |
| `/planforge-verify <phase>` | Verify phase completion against criteria |
| `/planforge-status` | Show current project status and progress |
| `/planforge-ship` | Create PR from verified work |

## File Structure

```
.planning/
├── PROJECT.md              # Vision, goals, constraints
├── REQUIREMENTS.md         # Scoped v1/v2/out-of-scope
├── ROADMAP.md              # Phases with traceability
├── STATE.md                # Current position, decisions, blockers
├── config.json             # Workflow preferences
├── 01-CONTEXT.md           # Phase preferences
├── 01-RESEARCH.md          # Research findings
├── 01-1-PLAN.md            # XML-structured plan
├── 01-1-SUMMARY.md         # Execution results
├── 01-VERIFICATION.md      # Compliance check
└── research/               # Domain research artifacts
```

## Hooks

PlanForge registers the following Hermes plugin hooks:

- `register_command` — Adds `/planforge-*` slash commands
- `pre_tool_call` — Can pause agent during critical phase execution
- `transform_tool_result` — Formats tool output for PlanForge verification
- `transform_terminal_output` — Parses build/test logs for checklist items

## Dashboard

PlanForge adds a "Roadmap" tab to the Hermes web dashboard showing:
- Phase completion percentage
- Current wave and task
- Blockers and decisions
- Timeline projection

## License

MIT License — see [LICENSE](LICENSE)

Copyright (c) 2025 Lex Christopherson (original GSD)
Copyright (c) 2025 Abdias Jimenez (PlanForge plugin)

## Acknowledgments

PlanForge is a spiritual successor to [GSD (Get Shit Done)](https://github.com/gsd-build/get-shit-done) by Lex Christopherson. It preserves the `.planning/` file format and core philosophy while extending it for the Hermes ecosystem.
