"""
PlanForge — Spec-driven development planning plugin for Hermes Agent.

Entrypoint: Hermes calls register(ctx) on plugin load.
"""

from typing import Any
import os
import json

__version__ = "0.1.0"
__author__ = "Abdias J (AxDSan)"


def register(ctx: Any) -> None:
    """
    Register PlanForge with the Hermes plugin system.
    Called by Hermes on plugin load.
    """
    # Register slash commands
    ctx.register_command("planforge-init", _cmd_init)
    ctx.register_command("planforge-plan", _cmd_plan)
    ctx.register_command("planforge-execute", _cmd_execute)
    ctx.register_command("planforge-verify", _cmd_verify)
    ctx.register_command("planforge-status", _cmd_status)
    ctx.register_command("planforge-ship", _cmd_ship)

    # Register hooks
    ctx.register_hook("pre_tool_call", _hook_pre_tool_call)
    ctx.register_hook("transform_tool_result", _hook_transform_tool_result)
    ctx.register_hook("transform_terminal_output", _hook_transform_terminal_output)

    # Log registration
    ctx.log.info(f"PlanForge v{__version__} registered — spec-driven planning ready")


# ───────────────────────────────────────────────────────────────
# Slash Commands
# ───────────────────────────────────────────────────────────────

def _cmd_init(ctx: Any, args: str) -> str:
    """
    /planforge-init "Project Name"
    Initialize a new project with .planning/ structure.
    """
    from . import init
    return init.run(ctx, args)


def _cmd_plan(ctx: Any, args: str) -> str:
    """
    /planforge-plan <phase_number>
    Generate or review a phase plan.
    """
    from . import plan
    return plan.run(ctx, args)


def _cmd_execute(ctx: Any, args: str) -> str:
    """
    /planforge-execute <phase_number>
    Execute a phase's tasks via Hermes tools.
    """
    from . import execute
    return execute.run(ctx, args)


def _cmd_verify(ctx: Any, args: str) -> str:
    """
    /planforge-verify <phase_number>
    Verify phase completion against acceptance criteria.
    """
    from . import verify
    return verify.run(ctx, args)


def _cmd_status(ctx: Any, args: str = "") -> str:
    """
    /planforge-status
    Show current project status and progress.
    """
    from . import status
    return status.run(ctx)


def _cmd_ship(ctx: Any, args: str = "") -> str:
    """
    /planforge-ship
    Create PR from verified work.
    """
    from . import ship
    return ship.run(ctx)


# ───────────────────────────────────────────────────────────────
# Hooks
# ───────────────────────────────────────────────────────────────

def _hook_pre_tool_call(ctx: Any, tool_name: str, tool_args: dict) -> dict | None:
    """
    pre_tool_call hook — can veto tool execution.
    PlanForge uses this to pause the agent during critical phase execution.
    """
    from . import state
    if state.is_phase_locked():
        ctx.log.warning(f"Tool '{tool_name}' blocked — phase execution in progress")
        return {"veto": True, "reason": "Phase execution in progress. Use /planforge-status to check."}
    return None  # Allow execution


def _hook_transform_tool_result(ctx: Any, tool_name: str, result: Any) -> Any:
    """
    transform_tool_result hook — rewrite tool results.
    PlanForge formats output for verification checklist.
    """
    from . import state, verify
    if state.is_executing_phase():
        return verify.format_result(tool_name, result)
    return result


def _hook_transform_terminal_output(ctx: Any, output: str) -> str:
    """
    transform_terminal_output hook — rewrite terminal output.
    PlanForge parses build/test logs for checklist items.
    """
    from . import state, verify
    if state.is_executing_phase():
        return verify.parse_terminal_output(output)
    return output
