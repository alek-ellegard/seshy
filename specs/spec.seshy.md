---
title: "Spec: Seshy"
created: "2026-01-06"
status: "draft"
---

# Spec: Seshy

## Intent

### Core Need

**Why this needs building** (not what to build):

Quick session management when working with git branches. Currently, switching to a new branch requires manually editing sesh.toml or running an interactive bash script with multiple prompts. Need a fast path: switch to branch → one command → tmux session ready.

### Success Vision

**What does success look like?**

From any git branch, run `seshy add -b`, see a preview, hit Enter, and have a new tmux session configured in sesh.toml. The session appears in sesh's session picker immediately. Full CRUD for sessions without manually editing TOML.

### Success Criteria

1. `seshy add -b` creates session from current branch in <3 seconds with single confirmation
2. `seshy delete` removes session AND its associated window blocks cleanly
3. CLI installable via `uv tool install -e .` and available globally
4. Interactive mode (`seshy add`) preserves fzf-based path/icon selection UX

---

## Context

### Current State

**What exists today:**

- Bash script (`~/.config/sesh/functions.sh`) with `add-new-session` function
- Interactive workflow: prompt name → fzf path → fzf icon → prompt number → preview → confirm
- Modular lib structure (`lib/ui.sh`, `lib/fzf-helpers.sh`)
- sesh.toml with ~40 sessions, each with associated `[[window]]` blocks

### Prior Attempts

**What's been tried before:**

The bash implementation works but requires too many prompts for the common case (adding a branch as a session). No quick path exists.

### Constraints

**Technical:**
- Must parse/modify TOML without breaking existing sessions
- Must handle `[[session]]` + associated `[[window]]` blocks together
- fzf must be available for interactive selection

**Non-technical:**
- Keep it simple - just CRUD, no advanced features

---

## Scope

### In Scope

- `seshy add` - Interactive session creation (fzf for path/icon)
- `seshy add -b/--from-branch` - Quick branch mode with auto-fill
- `seshy list` - Simple list of session names
- `seshy read` - Open sesh.toml in nvim
- `seshy update` - fzf select → open sesh.toml at that line in nvim
- `seshy delete` - fzf select → preview → confirm → delete session + windows

### Out of Scope

- Window CRUD (future feature per original prompt.md)
- Session templates beyond the fixed default
- Syncing with external systems
- Any sesh runtime functionality (just config management)

### Non-Goals

- Replacing sesh itself
- Managing tmux directly
- Complex configuration options

---

## Preferences

### Approach Preferences

- Python with uv (astral) - single-file script or minimal package
- Shell out to fzf via subprocess (proven pattern from bash)
- Use `tomlkit` for TOML parsing (preserves formatting/comments)
- Click or Typer for CLI framework
- Location: `~/code/tools/seshy`

### Anti-Patterns to Avoid

- Over-engineering (no plugin system, no config files)
- Breaking existing sesh.toml formatting
- Requiring Python libraries that need compilation

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| CLI name | `seshy` | Short, friendly |
| Branch mode | Flag `-b` on add | Single command, more flexible than subcommand |
| 5x numbering | Scan sesh.toml | Find highest 5x number and increment |
| Windows array | Fixed default | `["editor", "dual", "lazydocker", "lazygit"]` |
| Update UX | Open in editor | fzf select → nvim at line (simplest approach) |
| Delete cleanup | Auto-cleanup | Remove session + associated windows |
| fzf integration | Shell out | Subprocess to fzf, like bash version |
| Project location | Separate repo | `~/code/tools/seshy` |

---

## Open Questions

- [x] All questions resolved during interview

---

## Interview Notes

- User manages ~40 tmux sessions via sesh.toml
- Primary pain point: adding sessions for new git branches is too slow
- Branch sessions should use 50-range numbers (51, 52, 53...)
- Default icon for branch mode (avoids icon selection step)
- Update = "open at line in nvim" (simpler than field-by-field editing)
- Delete must clean up orphaned `[[window]]` blocks
- Read = just `nvim ~/.config/sesh/sesh.toml`
- Preserve fzf UX for interactive mode (muscle memory)
