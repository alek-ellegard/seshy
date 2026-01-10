"""User interaction functions (prompts, display)."""

from .toml_ops import generate_session_block


def confirm(prompt: str = "Proceed?") -> bool:
    """Ask for Y/n confirmation."""
    response = input(f"{prompt} [Y/n] ").strip().lower()
    return response in ("", "y", "yes")


def preview_session(name: str, path: str, icon: str, number: int) -> str:
    """Generate preview of session to be added."""
    return generate_session_block(name, path, icon, number)
