"""Pure utility functions with no side effects."""

import os


def get_parent_dir_name() -> str:
    """Get parent directory name as project name."""
    return os.path.basename(os.getcwd())


def get_cwd_as_path() -> str:
    """Get current working directory in ~ format."""
    cwd = os.getcwd()
    home = os.path.expanduser("~")
    if cwd.startswith(home):
        return "~" + cwd[len(home) :]
    return cwd
