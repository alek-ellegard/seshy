"""Seshy CLI - manage sesh.toml sessions."""

import os
import subprocess
import sys

import click

from .fzf import fzf_select, fzf_select_icon, fzf_select_path_recursive
from .toml_ops import (
    SESH_TOML_PATH,
    add_session,
    delete_session,
    find_next_5x_number,
    generate_session_block,
    get_session_line_number,
    list_sessions,
)

DEFAULT_ICON = "💻"


def get_parent_dir_name() -> str:
    """Get parent directory name as project name."""
    return os.path.basename(os.getcwd())


def get_cwd_as_path() -> str:
    """Get current working directory in ~ format."""
    cwd = os.getcwd()
    home = os.path.expanduser("~")
    if cwd.startswith(home):
        return "~" + cwd[len(home):]
    return cwd


def preview_session(name: str, path: str, icon: str, number: int) -> str:
    """Generate preview of session to be added."""
    return generate_session_block(name, path, icon, number)


def confirm(prompt: str = "Proceed?") -> bool:
    """Ask for Y/n confirmation."""
    response = input(f"{prompt} [Y/n] ").strip().lower()
    return response in ("", "y", "yes")


@click.group()
def cli():
    """Seshy - manage sesh.toml tmux sessions."""
    pass


@cli.command("add")
@click.option("-q", "--quick", is_flag=True, help="Quick mode: auto-fill from cwd")
def add_cmd(quick: bool):
    """Add a new session to sesh.toml."""
    if quick:
        # Quick mode - auto-fill from current directory
        name = get_parent_dir_name()
        path = get_cwd_as_path()
        icon = DEFAULT_ICON
        number = find_next_5x_number()

    else:
        # Interactive mode
        name = click.prompt("Session name")

        click.echo("\nSelect project path...")
        path = fzf_select_path_recursive()
        if not path:
            click.echo("No path selected, aborting.", err=True)
            sys.exit(1)

        click.echo("\nSelect icon...")
        icon = fzf_select_icon()
        if not icon:
            click.echo(f"No icon selected, using default {DEFAULT_ICON}")
            icon = DEFAULT_ICON

        number = click.prompt("Session number", type=int)

    # Show preview
    click.echo("\n" + "=" * 40)
    click.echo("Preview:")
    click.echo("=" * 40)
    click.echo(preview_session(name, path, icon, number))
    click.echo("=" * 40 + "\n")

    if confirm("Add this session?"):
        add_session(name, path, icon, number)
        click.echo(f"Added session: {number} {name} {icon}")
    else:
        click.echo("Aborted.")


@cli.command("list")
def list_cmd():
    """List all session names."""
    sessions = list_sessions()
    for s in sessions:
        click.echo(s)


@cli.command()
def read():
    """Open sesh.toml in nvim."""
    os.execvp("nvim", ["nvim", str(SESH_TOML_PATH)])


@cli.command()
def update():
    """Select a session and open sesh.toml at that line in nvim."""
    sessions = list_sessions()
    if not sessions:
        click.echo("No sessions found.", err=True)
        sys.exit(1)

    selected = fzf_select(sessions, "update> ")
    if not selected:
        click.echo("No session selected.", err=True)
        sys.exit(1)

    line = get_session_line_number(selected)
    if line:
        os.execvp("nvim", ["nvim", f"+{line}", str(SESH_TOML_PATH)])
    else:
        click.echo(f"Could not find line for session: {selected}", err=True)
        sys.exit(1)


@cli.command()
def delete():
    """Select a session and delete it (with associated windows)."""
    sessions = list_sessions()
    if not sessions:
        click.echo("No sessions found.", err=True)
        sys.exit(1)

    selected = fzf_select(sessions, "delete> ")
    if not selected:
        click.echo("No session selected.", err=True)
        sys.exit(1)

    click.echo(f"\nAbout to delete session: {selected}")
    click.echo("This will also remove associated [[window]] blocks.\n")

    if confirm("Delete this session?"):
        if delete_session(selected):
            click.echo(f"Deleted session: {selected}")
        else:
            click.echo(f"Failed to delete session: {selected}", err=True)
            sys.exit(1)
    else:
        click.echo("Aborted.")


# Aliases
cli.add_command(add_cmd, name="a")
cli.add_command(list_cmd, name="ls")
cli.add_command(read, name="r")
cli.add_command(update, name="u")
cli.add_command(delete, name="rm")


def main():
    try:
        cli(standalone_mode=False)
    except click.Abort:
        click.echo("\nAborted.")
        sys.exit(130)
    except KeyboardInterrupt:
        click.echo("\nAborted.")
        sys.exit(130)


if __name__ == "__main__":
    main()
