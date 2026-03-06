# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Seshy is a Python CLI for managing tmux sessions defined in `~/.config/sesh/sesh.toml`.

## Commands

```bash
# Install for development
uv tool install -e .

# Or via Makefile
make install-edit
```

| Command | Alias | Description |
|---------|-------|-------------|
| `seshy add` | `a` | Interactive session creation |
| `seshy add -q` | `a -q` | Quick mode: auto-fill from cwd |
| `seshy list` | `ls` | List all session names |
| `seshy read` | `r` | Open sesh.toml in nvim |
| `seshy update` | `u` | fzf select → open at line in nvim |
| `seshy delete` | `rm` | fzf select → delete session + windows |

## Quick Mode (`-q`)

Auto-fills session from current directory:
- **name**: parent directory name
- **path**: current working directory
- **icon**: default 💻
- **number**: next available in 50-range (51, 52, 53...)

## Architecture

```
src/seshy/
├── cli.py        # Click CLI entry point (thin layer, delegates to workflows)
├── models.py     # Data models (native Python classes, StrEnum for enums)
├── utils.py      # Pure utility functions
├── ui.py         # User interaction (prompts, fzf, display)
├── toml_ops.py   # TOML parsing with tomlkit (preserves formatting)
└── workflows/    # Business logic, one file per feature
    ├── add.py
    ├── delete.py
    └── ...
```

**Data flow**: cli.py → workflows/*.py → ui.py (user interaction) → toml_ops.py (persistence)

## Code Principles

- **Types**: Use native Python classes and `StrEnum` for type safety
- **Separation**: Models in models.py, utilities in utils.py, UI in ui.py
- **Workflows**: Each feature gets its own file in `workflows/`
- **CLI layer**: Thin - parse args, call workflow, handle errors

**Key constants** in toml_ops.py:
- `SESH_TOML_PATH`: `~/.config/sesh/sesh.toml`
- `DEFAULT_WINDOWS`: `["editor", "dual", "lazydocker", "lazygit"]`
- `WINDOW_SCRIPTS`: Maps window names to startup scripts

## Workflow Tools

- **Package management**: `uv` (astral) with pyproject.toml
- **Sprint management**: `/sam` plugin - manages `.sam/` for sprints and features

## Codebase Map

For comprehensive architecture documentation, data flow diagrams, and navigation guide, see `docs/CODEBASE_MAP.md`.
