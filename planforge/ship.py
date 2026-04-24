"""PlanForge /planforge-ship command — create PR from verified work."""

from typing import Any
import os


def run(ctx: Any) -> str:
    cwd = os.getcwd()
    planning_dir = os.path.join(cwd, ".planning")

    if not os.path.exists(planning_dir):
        return "❌ No `.planning/` found."

    # Check if we have a clean git state
    import subprocess
    try:
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=cwd)
        if result.returncode != 0:
            return "❌ Not a git repository. Initialize git first."

        dirty = result.stdout.strip()
        if not dirty:
            return "⚠️ No changes to ship. Make some commits first."

        # Get current branch
        branch_result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, cwd=cwd)
        branch = branch_result.stdout.strip()

        # Check for uncommitted changes
        if dirty:
            return f"⚠️ Uncommitted changes detected. Commit them first:\n```\n{dirty[:200]}\n```"

        return f"🚀 Ready to ship from branch `{branch}`!\n\nUse `gh pr create` or your preferred method to open a PR."

    except FileNotFoundError:
        return "❌ Git not found. Install git to use shipping."
