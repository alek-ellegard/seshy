"""FZF subprocess helpers."""

import os
import subprocess
from pathlib import Path

from .config import get_base_paths, get_icons


def fzf_select(items: list[str], prompt: str = "> ") -> str | None:
    """Generic fzf selection via subprocess."""
    if not items:
        return None

    input_str = "\n".join(items)
    try:
        result = subprocess.run(
            ["fzf", "--prompt", prompt],
            input=input_str,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except FileNotFoundError:
        print("Error: fzf not found. Please install fzf.")
    return None


def fzf_select_icon() -> str | None:
    """Select icon from list."""
    return fzf_select(get_icons(), "icon> ")


def fzf_select_base_path() -> str | None:
    """Select from configured base paths."""
    expanded = [os.path.expanduser(p) for p in get_base_paths()]
    return fzf_select(expanded, "base> ")


def fzf_navigate_recursive(start_path: str) -> str | None:
    """Recursively navigate directories, select '.' to stop."""
    current = Path(start_path).expanduser()

    while True:
        if not current.is_dir():
            return str(current)

        # List directories + '.' option
        items = ["."]  # Select current
        try:
            dirs = sorted([d.name for d in current.iterdir() if d.is_dir() and not d.name.startswith(".")])
            items.extend(dirs)
        except PermissionError:
            pass

        selection = fzf_select(items, f"{current}/> ")

        if selection is None:
            return None
        if selection == ".":
            return str(current)

        current = current / selection


def fzf_select_path_recursive() -> str | None:
    """Select base path then navigate recursively."""
    base = fzf_select_base_path()
    if base is None:
        return None

    result = fzf_navigate_recursive(base)
    if result:
        # Convert to ~ format if in home
        home = str(Path.home())
        if result.startswith(home):
            result = "~" + result[len(home):]
    return result
