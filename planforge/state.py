"""PlanForge state management — tracks phase execution, locks, and progress."""

from typing import Any
import os
import json
import time

_STATE_FILE = os.path.expanduser("~/.hermes/planforge_state.json")


def _load() -> dict:
    if os.path.exists(_STATE_FILE):
        with open(_STATE_FILE) as f:
            return json.load(f)
    return {"locked": False, "current_phase": None, "current_project": None, "history": []}


def _save(state: dict) -> None:
    os.makedirs(os.path.dirname(_STATE_FILE), exist_ok=True)
    with open(_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def is_phase_locked() -> bool:
    return _load().get("locked", False)


def is_executing_phase() -> bool:
    return _load().get("locked", False) and _load().get("current_phase") is not None


def lock_phase(project_dir: str, phase: int) -> None:
    state = _load()
    state["locked"] = True
    state["current_phase"] = phase
    state["current_project"] = project_dir
    state["history"].append({"event": "lock", "phase": phase, "ts": time.time()})
    _save(state)


def unlock_phase() -> None:
    state = _load()
    state["locked"] = False
    state["history"].append({"event": "unlock", "phase": state.get("current_phase"), "ts": time.time()})
    state["current_phase"] = None
    _save(state)


def get_current_project() -> str | None:
    return _load().get("current_project")


def get_current_phase() -> int | None:
    return _load().get("current_phase")
