"""PlanForge templates — reusable planning document templates."""

PROJECT_TEMPLATE = """# {name}

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
"""

REQUIREMENTS_TEMPLATE = """# Requirements

## v1 (MVP)
- 

## v2 (Post-MVP)
- 

## Out of Scope
- 
"""

ROADMAP_TEMPLATE = """# Roadmap

| Phase | Name | Status | Exit Criteria |
|-------|------|--------|---------------|
| 1 | Research & Context | 🔲 Not Started | Context doc complete |
| 2 | Planning | 🔲 Not Started | PLAN.md approved |
| 3 | Execution | 🔲 Not Started | All waves complete |
| 4 | Verification | 🔲 Not Started | All criteria pass |
| 5 | Shipping | 🔲 Not Started | PR merged |
"""

STATE_TEMPLATE = """# State

**Current Phase:** 0 — Not Started
**Status:** Ready to begin
**Last Updated:** 

## Decisions
- 

## Blockers
- None

## Notes
- 
"""

PLAN_TEMPLATE = """# Phase {phase} Plan

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
- Phase {prev_phase} complete (if applicable)

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Risks
- 

## Notes
- 
"""
