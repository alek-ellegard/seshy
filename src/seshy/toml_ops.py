"""TOML operations for sesh.toml management."""

import re
from pathlib import Path

import tomlkit
from tomlkit import TOMLDocument

SESH_TOML_PATH = Path.home() / ".config" / "sesh" / "sesh.toml"

DEFAULT_WINDOWS = ["editor", "dual", "lazydocker", "lazygit"]

WINDOW_SCRIPTS = {
    "editor": "win-editor-git",
    "dual": "win-split-dual",
    "lazydocker": "win-lazydocker",
    "lazygit": "win-lazygit",
}


def load_config() -> TOMLDocument:
    """Load sesh.toml preserving formatting."""
    return tomlkit.parse(SESH_TOML_PATH.read_text())


def save_config(doc: TOMLDocument) -> None:
    """Save config back to sesh.toml."""
    SESH_TOML_PATH.write_text(tomlkit.dumps(doc))


def list_sessions() -> list[str]:
    """Return list of session names."""
    doc = load_config()
    sessions = doc.get("session", [])
    return [s.get("name", "") for s in sessions]


def extract_number(name: str) -> int | None:
    """Extract leading number from session name like '52 feature-branch'."""
    match = re.match(r"^(\d+)", name.strip())
    if match:
        return int(match.group(1))
    return None


def find_next_5x_number() -> int:
    """Find highest 5x number in sessions and return next."""
    sessions = list_sessions()
    nums = []
    for name in sessions:
        num = extract_number(name)
        if num is not None and 50 <= num < 60:
            nums.append(num)
    return max(nums, default=50) + 1


def get_session_line_number(name: str) -> int | None:
    """Find the line number of a session in sesh.toml."""
    lines = SESH_TOML_PATH.read_text().splitlines()
    for i, line in enumerate(lines, start=1):
        if f'name = "{name}"' in line:
            # Return the [[session]] line (usually 1-2 lines before)
            for j in range(i - 1, max(0, i - 4), -1):
                if "[[session]]" in lines[j - 1]:
                    return j
            return i
    return None


def generate_session_block(name: str, path: str, icon: str, number: int) -> str:
    """Generate a session block with windows."""
    full_name = f"{number} {name} {icon}"

    lines = [
        "# ---",
        "",
        "[[session]]",
        f'name = "{full_name}"',
        f'path = "{path}"',
        f'windows = {DEFAULT_WINDOWS}',
        "",
    ]

    for win_name in DEFAULT_WINDOWS:
        script = WINDOW_SCRIPTS.get(win_name, f"win-{win_name}")
        lines.extend([
            "[[window]]",
            f'name = "{win_name}"',
            f'startup_script = "{script}"',
            "",
        ])

    return "\n".join(lines)


def add_session(name: str, path: str, icon: str, number: int) -> None:
    """Append session + windows to sesh.toml."""
    block = generate_session_block(name, path, icon, number)

    with open(SESH_TOML_PATH, "a") as f:
        f.write("\n" + block)


def delete_session(name: str) -> bool:
    """Delete session and its associated windows from sesh.toml."""
    content = SESH_TOML_PATH.read_text()
    lines = content.splitlines()

    # Find session block
    session_start = None
    session_end = None
    windows_count = 0

    # Find session by name
    for i, line in enumerate(lines):
        if f'name = "{name}"' in line:
            # Go back to find [[session]]
            for j in range(i - 1, -1, -1):
                if "[[session]]" in lines[j]:
                    session_start = j
                    break
                # Check for separator comment
                if lines[j].strip() == "# ---":
                    session_start = j
                    break
            break

    if session_start is None:
        return False

    # Find how many windows this session has
    doc = load_config()
    for s in doc.get("session", []):
        if s.get("name") == name:
            windows_count = len(s.get("windows", []))
            break

    # Find end of session (next [[session]] or EOF)
    in_session_windows = True
    window_count_seen = 0

    for i in range(session_start + 1, len(lines)):
        line = lines[i].strip()
        if line == "[[session]]":
            session_end = i
            break
        if line == "[[window]]":
            window_count_seen += 1
            if window_count_seen > windows_count:
                session_end = i
                break
        # Also check for separator
        if line == "# ---" and window_count_seen >= windows_count:
            session_end = i
            break

    if session_end is None:
        session_end = len(lines)

    # Remove the lines
    new_lines = lines[:session_start] + lines[session_end:]

    # Clean up extra blank lines
    new_content = "\n".join(new_lines)
    new_content = re.sub(r"\n{3,}", "\n\n", new_content)

    SESH_TOML_PATH.write_text(new_content)
    return True
