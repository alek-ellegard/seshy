"""Add session workflow."""

import sys

import click

from ..config import get_default_icon
from ..fzf import fzf_select_icon, fzf_select_path_recursive
from ..toml_ops import add_session, find_next_5x_number
from ..ui import confirm, preview_session
from ..utils import get_cwd_as_path, get_parent_dir_name


def run(quick: bool) -> None:
    """Add a new session to sesh.toml.

    Args:
        quick: If True, auto-fill from current directory.
               If False, prompt interactively.
    """
    if quick:
        name = get_parent_dir_name()
        path = get_cwd_as_path()
        icon = get_default_icon()
        number = find_next_5x_number()
    else:
        name = click.prompt("Session name")

        click.echo("\nSelect project path...")
        path = fzf_select_path_recursive()
        if not path:
            click.echo("No path selected, aborting.", err=True)
            sys.exit(1)

        click.echo("\nSelect icon...")
        icon = fzf_select_icon()
        if not icon:
            click.echo(f"No icon selected, using default {get_default_icon()}")
            icon = get_default_icon()

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
