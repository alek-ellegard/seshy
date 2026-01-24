"""Delete session workflow."""

import sys

import click

from ..fzf import fzf_select
from ..toml_ops import delete_session, list_sessions
from ..ui import confirm


def run() -> None:
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
