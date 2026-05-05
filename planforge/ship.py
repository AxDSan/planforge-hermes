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
        result = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True, cwd=cwd)
        if result.returncode != 0:
            return "❌ Not a git repository. Initialize git first."

        staged = result.stdout.strip()
        if not staged:
            return "⚠️ No changes to ship. Stage some commits first."

        # Get current branch
        branch_result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, cwd=cwd)
        branch = branch_result.stdout.strip()

        # Check for unstaged changes
        unstaged_result = subprocess.run(["git", "diff", "--name-only"], capture_output=True, text=True, cwd=cwd)
        unstaged = unstaged_result.stdout.strip()
        if unstaged:
            return f"⚠️ Uncommitted changes detected. Commit them first:\n```\n{unstaged[:200]}\n```"

        staged_preview = subprocess.run(
            ["git", "diff", "--cached", "--stat"], capture_output=True, text=True, cwd=cwd
        )
        return (
            f"🚀 Ready to ship from branch `{branch}`!\n\n"
            f"Staged changes:\n```\n{staged_preview.stdout.strip()[:500]}\n```\n\n"
            f"Use `gh pr create` or your preferred method to open a PR."
        )

    except FileNotFoundError:
        return "❌ Git not found. Install git to use shipping."
