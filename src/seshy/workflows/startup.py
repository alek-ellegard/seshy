"""Startup workflow - launch multiple sessions at once."""

import fnmatch
import subprocess
import sys

import click

from ..config import get_startup_groups
from ..toml_ops import list_sessions


def match_sessions(patterns: list[str], sessions: list[str]) -> list[str]:
    """Match session names against patterns (supports wildcards)."""
    matched = []
    for session in sessions:
        for pattern in patterns:
            if fnmatch.fnmatch(session.lower(), pattern.lower()):
                matched.append(session)
                break
    return matched


def launch_session(name: str) -> bool:
    """Launch a session via sesh connect (detached)."""
    try:
        subprocess.run(
            ["sesh", "connect", name],
            check=True,
            capture_output=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def list_groups() -> None:
    """List available startup groups."""
    groups = get_startup_groups()
    sessions = list_sessions()

    if not groups:
        click.echo("No startup groups defined.", err=True)
        click.echo("\nAdd [groups] to ~/.config/seshy/config.toml:", err=True)
        click.echo('  [groups]\n  work = ["dotfiles*", "caes*", "cam*"]', err=True)
        sys.exit(1)

    click.echo("Available groups:\n")
    for name, patterns in groups.items():
        matched = match_sessions(patterns, sessions)
        click.echo(f"  {name} ({len(matched)} sessions)")
        for pattern in patterns:
            click.echo(f"    - {pattern}")
    click.echo("\nUsage: seshy startup <group>")


def run(group_name: str | None) -> None:
    """Run startup workflow for a named group."""
    groups = get_startup_groups()

    if not groups:
        click.echo("No startup groups defined.", err=True)
        click.echo("\nAdd [groups] to ~/.config/seshy/config.toml:", err=True)
        click.echo('  [groups]\n  work = ["dotfiles*", "caes*", "cam*"]', err=True)
        sys.exit(1)

    if group_name is None:
        list_groups()
        return

    if group_name not in groups:
        click.echo(f"Group '{group_name}' not found.", err=True)
        click.echo(f"Available: {', '.join(groups.keys())}", err=True)
        sys.exit(1)

    patterns = groups[group_name]
    sessions = list_sessions()
    matched = match_sessions(patterns, sessions)

    if not matched:
        click.echo(f"No sessions matched patterns: {patterns}", err=True)
        sys.exit(1)

    click.echo(f"Launching {len(matched)} sessions...")

    launched = []
    failed = []

    for session in matched:
        if launch_session(session):
            launched.append(session)
            click.echo(f"  ✓ {session}")
        else:
            failed.append(session)
            click.echo(f"  ✗ {session}", err=True)

    click.echo(f"\nLaunched {len(launched)}/{len(matched)} sessions.")

    if failed:
        click.echo(f"Failed: {', '.join(failed)}", err=True)
        sys.exit(1)
