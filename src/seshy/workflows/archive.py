"""Archive legacy bash scripts to ~/.config/sesh/archive/."""

import shutil
from dataclasses import dataclass, field
from pathlib import Path


SESH_CONFIG_DIR = Path.home() / ".config" / "sesh"
ARCHIVE_DIR = SESH_CONFIG_DIR / "archive"

FILES_TO_ARCHIVE = [
    "functions.sh",
    "fzf-config.sh",
    "lib/ui.sh",
    "lib/fzf-helpers.sh",
]


@dataclass
class ArchiveResult:
    """Result of archive operation."""

    success: bool
    files_moved: list[str] = field(default_factory=list)
    files_skipped: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    already_archived: bool = False


def archive_scripts() -> ArchiveResult:
    """Move legacy bash scripts to archive directory.

    Idempotent - safe to run multiple times.
    """
    result = ArchiveResult(success=True)

    # Check if already fully archived
    if _is_already_archived():
        result.already_archived = True
        return result

    # Create archive directories
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    (ARCHIVE_DIR / "lib").mkdir(exist_ok=True)

    # Move each file
    for rel_path in FILES_TO_ARCHIVE:
        src = SESH_CONFIG_DIR / rel_path
        dst = ARCHIVE_DIR / rel_path

        if not src.exists():
            result.files_skipped.append(rel_path)
            result.warnings.append(f"Source not found: {rel_path}")
            continue

        if dst.exists():
            result.files_skipped.append(rel_path)
            continue

        try:
            shutil.move(str(src), str(dst))
            result.files_moved.append(rel_path)
        except OSError as e:
            result.warnings.append(f"Failed to move {rel_path}: {e}")
            result.success = False

    # Clean up empty lib directory if all files moved
    lib_dir = SESH_CONFIG_DIR / "lib"
    if lib_dir.exists() and not any(lib_dir.iterdir()):
        lib_dir.rmdir()

    return result


def _is_already_archived() -> bool:
    """Check if scripts are already archived."""
    # If archive exists and no source files remain, consider archived
    if not ARCHIVE_DIR.exists():
        return False

    source_exists = any(
        (SESH_CONFIG_DIR / f).exists() for f in FILES_TO_ARCHIVE
    )
    return not source_exists
