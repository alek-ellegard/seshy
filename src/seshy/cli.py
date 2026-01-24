"""Seshy CLI - manage sesh.toml sessions."""

import os
import sys

import click

from .fzf import fzf_select
from .toml_ops import SESH_TOML_PATH, get_session_line_number, list_sessions
from .workflows import add as add_workflow
from .workflows import delete as delete_workflow


@click.group()
def cli():
    """Seshy - manage sesh.toml tmux sessions."""
    pass


@cli.command("add")
@click.option("-q", "--quick", is_flag=True, help="Quick mode: auto-fill from cwd")
def add_cmd(quick: bool):
    """Add a new session to sesh.toml."""
    add_workflow.run(quick)


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
    delete_workflow.run()


# Aliases
cli.add_command(add_cmd, name="a")
cli.add_command(list_cmd, name="ls")
cli.add_command(read, name="r")
cli.add_command(update, name="u")
cli.add_command(delete, name="rm")


def main():
    try:
        cli(standalone_mode=False)
    except click.ClickException as e:
        e.show()
        sys.exit(e.exit_code)
    except click.Abort:
        click.echo("\nAborted.")
        sys.exit(130)
    except KeyboardInterrupt:
        click.echo("\nAborted.")
        sys.exit(130)


if __name__ == "__main__":
    main()
