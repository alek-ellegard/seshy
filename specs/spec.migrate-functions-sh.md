---
title: "Spec: Migrate Functions Sh"
created: "2026-01-10"
status: "draft"
---

# Spec: Migrate Functions Sh

## Intent

### Core Need

**Why this needs building** (not what to build):

Seshy Python CLI already implements the bash script functionality, but the implementation is incomplete - configuration is hardcoded and the bash scripts still exist creating maintenance burden and confusion about which tool to use. The migration completes the transition from bash to Python, externalizes configuration, and cleanly retires the legacy scripts.

### Success Vision

**What does success look like?**

Seshy is the single source of truth for session management. Configuration (base paths, icons) lives in a TOML file, not hardcoded in source. The bash scripts are archived for reference but no longer needed for daily use.

### Success Criteria

1. Seshy works standalone - no runtime dependency on bash scripts in `~/.config/sesh/`
2. Config externalized - base paths and icons configurable via `~/.config/seshy/config.toml`
3. Auto-initialization - config file created with defaults on first run if missing
4. Scripts archived - bash scripts moved to `~/.config/sesh/archive/`

---

## Context

### Current State

**What exists today:**

- Python CLI (`seshy`) with add, list, read, update, delete commands
- Bash scripts in `~/.config/sesh/`: functions.sh, lib/ui.sh, lib/fzf-helpers.sh, fzf-config.sh
- Configuration hardcoded in `src/seshy/fzf.py` (BASE_PATHS, ICONS_LIST)
- Feature parity between bash and Python already achieved

### Prior Attempts

**What's been tried before:**

The Python implementation was built to replace bash scripts but stopped short of externalizing configuration and archiving the legacy scripts.

### Constraints

**Technical:**
- No new Python dependencies (tomlkit already available)
- No breaking changes to existing CLI commands
- Config auto-creation must handle missing directory

**Non-technical:**
- Keep it simple - don't over-engineer the config system

---

## Scope

### In Scope

- Externalize config to `~/.config/seshy/config.toml`
- Auto-create config with defaults on first run
- Archive bash scripts to `~/.config/sesh/archive/`

### Out of Scope

- New features beyond config externalization
- Changes to sesh.toml structure

### Non-Goals

- Replacing sesh itself
- Complex configuration options

---

## Preferences

### Approach Preferences

- TOML format for config (consistency with sesh.toml)
- Separate config directory (`~/.config/seshy/`) from sesh config
- Mirror current hardcoded values as defaults

### Anti-Patterns to Avoid

- Over-engineering the config system
- Breaking existing seshy commands
- Adding new dependencies

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Config file | `~/.config/seshy/config.toml` | Separate from sesh.toml, consistent format |
| Config init | Auto-create with defaults | Zero-friction setup |
| Archive location | `~/.config/sesh/archive/` | Keep archived scripts near original location |
| What to archive | functions.sh, lib/, fzf-config.sh | All bash scripts used by seshy |

---

## Open Questions

- [x] All questions resolved during interview

---

## Interview Notes

- User wants full migration: port features, externalize config, archive scripts
- Feature parity already complete - no missing features noticed
- Config should be auto-created on first run
- Bash scripts to be archived (not deleted) at `~/.config/sesh/archive/`
- All existing seshy commands must continue working
