"""Seshy configuration management."""

from pathlib import Path

import tomlkit

CONFIG_PATH = Path.home() / ".config" / "seshy" / "config.toml"

DEFAULT_ICONS = [
    "💻", "🚀", "🔧", "📦", "🎯", "⚡", "🌟", "🔥", "💡",
    "📊", "🎨", "🏗️", "🧪", "📱", "🌐", "🤖"
]

DEFAULT_BASE_PATHS = [
    "~/code",
    "~/code/work",
    "~/code/personal",
]

DEFAULT_ICON = "💻"


def _ensure_config() -> None:
    """Create config file with defaults if it doesn't exist."""
    if CONFIG_PATH.exists():
        return

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    doc = tomlkit.document()

    icons = tomlkit.table()
    icons.add("list", DEFAULT_ICONS)
    icons.add("default", DEFAULT_ICON)
    doc.add("icons", icons)

    paths = tomlkit.table()
    paths.add("base", DEFAULT_BASE_PATHS)
    doc.add("paths", paths)

    CONFIG_PATH.write_text(tomlkit.dumps(doc))


def _load_config() -> tomlkit.TOMLDocument:
    """Load config from file, creating with defaults if needed."""
    _ensure_config()
    return tomlkit.parse(CONFIG_PATH.read_text())


def get_icons() -> list[str]:
    """Get list of available icons."""
    config = _load_config()
    return list(config.get("icons", {}).get("list", DEFAULT_ICONS))


def get_base_paths() -> list[str]:
    """Get list of base paths for project navigation."""
    config = _load_config()
    return list(config.get("paths", {}).get("base", DEFAULT_BASE_PATHS))


def get_default_icon() -> str:
    """Get default icon for new sessions."""
    config = _load_config()
    return str(config.get("icons", {}).get("default", DEFAULT_ICON))
