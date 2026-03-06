"""Seshy CLI - manage sesh.toml sessions."""

import os
import sys

import click

from .fzf import fzf_select
from .toml_ops import SESH_TOML_PATH, get_session_line_number, list_sessions
from .workflows import add as add_workflow
from .workflows import delete as delete_workflow
from .workflows import startup as startup_workflow


class AliasGroup(click.Group):
    """Click group that displays aliases alongside commands."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._aliases: dict[str, str] = {}  # alias -> canonical name

    def add_alias(self, name: str, alias: str) -> None:
        """Register an alias for a command."""
        self._aliases[alias] = name
        # Add the alias as a command that points to the original
        cmd = self.commands.get(name)
        if cmd:
            self.add_command(cmd, name=alias)

    def format_commands(self, ctx, formatter):
        """Format commands with aliases shown on same line."""
        commands = []
        # Build reverse mapping: canonical -> [aliases]
        alias_map: dict[str, list[str]] = {}
        for alias, canonical in self._aliases.items():
            alias_map.setdefault(canonical, []).append(alias)

        for name, cmd in self.commands.items():
            # Skip aliases in the main listing
            if name in self._aliases:
                continue

            help_text = cmd.get_short_help_str(limit=formatter.width)
            aliases = alias_map.get(name, [])
            if aliases:
                display_name = f"{aliases[0]} / {name}"
            else:
                display_name = name
            commands.append((display_name, help_text))

        if commands:
            with formatter.section("Commands"):
                formatter.write_dl(commands)


@click.group(cls=AliasGroup)
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


@cli.command()
@click.argument("group", required=False)
def startup(group: str | None):
    """Launch all sessions in a named group."""
    startup_workflow.run(group)


@cli.command("shell-path")
def shell_path():
    """Print path to shell functions for sourcing."""
    from pathlib import Path

    pkg_dir = Path(__file__).parent
    functions_path = pkg_dir / "shell" / "functions.sh"
    click.echo(functions_path)


# Aliases
cli.add_alias("add", "a")
cli.add_alias("list", "ls")
cli.add_alias("read", "r")
cli.add_alias("update", "u")
cli.add_alias("delete", "rm")
cli.add_alias("startup", "s")


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
