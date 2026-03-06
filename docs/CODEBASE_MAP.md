---
last_mapped: 2026-02-04T12:00:00Z
total_files: 29
total_tokens: 18663
---

# Codebase Map

## System Overview

```
                     ┌─────────────────────────────────────────┐
                     │              CLI Entry                   │
                     │           (cli.py:main)                  │
                     └──────────────────┬──────────────────────┘
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           │                            │                            │
           ▼                            ▼                            ▼
    ┌──────────────┐            ┌──────────────┐            ┌──────────────┐
    │   Workflows  │            │  Direct CLI  │            │   Editor     │
    │  (add/del/   │            │   Commands   │            │ Integration  │
    │   startup)   │            │ (list/read)  │            │  (update)    │
    └──────┬───────┘            └──────┬───────┘            └──────┬───────┘
           │                            │                          │
           ▼                            ▼                          ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │                         Core Services                             │
    │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌─────────────┐ │
    │  │  toml_ops  │  │    fzf     │  │   config   │  │     ui      │ │
    │  │ (TOML I/O) │  │(selection) │  │ (settings) │  │  (prompts)  │ │
    │  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └──────┬──────┘ │
    └────────┼───────────────┼───────────────┼────────────────┼────────┘
             │               │               │                │
             ▼               ▼               ▼                ▼
    ┌────────────────┐  ┌─────────┐  ┌───────────────┐  ┌───────────────┐
    │ ~/.config/sesh │  │   fzf   │  │~/.config/seshy│  │    stdout     │
    │   /sesh.toml   │  │ process │  │  /config.toml │  │               │
    └────────────────┘  └─────────┘  └───────────────┘  └───────────────┘
```

## Directory Structure

```
seshy/
├── src/seshy/
│   ├── __init__.py        # Package init, version string
│   ├── cli.py             # Click CLI entry point, command routing
│   ├── config.py          # Seshy settings (icons, paths, groups)
│   ├── fzf.py             # FZF subprocess integration
│   ├── toml_ops.py        # TOML parsing/manipulation for sesh.toml
│   ├── ui.py              # User prompts (confirm, preview)
│   ├── utils.py           # Pure utilities (path helpers)
│   └── workflows/
│       ├── __init__.py    # Package marker
│       ├── add.py         # Session creation workflow
│       ├── delete.py      # Session deletion workflow
│       └── startup.py     # Startup group launcher
├── specs/
│   └── spec.seshy.md      # Original design specification
├── docs/                  # Documentation (this file)
├── pyproject.toml         # Package config (hatchling, click, tomlkit)
├── Makefile               # Dev shortcuts (install, reinstall)
├── install.sh             # Standalone installer script
├── CLAUDE.md              # AI assistant guidance
└── README.md              # Usage documentation
```

## Module Guide

### src/seshy/ (Core Package)

- **Purpose**: Python CLI for managing tmux sessions defined in sesh.toml
- **Key Files**: `cli.py` (entry), `toml_ops.py` (persistence), `fzf.py` (selection)
- **Dependencies**:
  - External: `click`, `tomlkit`
  - System: `fzf` (required for interactive selection)
- **Exports**: `main()` CLI entry point

### src/seshy/workflows/

- **Purpose**: High-level user workflows (add/delete/startup sessions)
- **Key Files**: `add.py`, `delete.py`, `startup.py`
- **Dependencies**: Core modules (`toml_ops`, `fzf`, `config`, `ui`)
- **Exports**: `run()` function in each module

## Data Flow

### Add Session Flow
```
User: seshy add [--quick]
         │
         ▼
┌─────────────────────────┐
│ Quick mode?             │──Yes──▶ Auto-fill from cwd
│ (--quick flag)          │              │
└──────────┬──────────────┘              │
           │No                           │
           ▼                             ▼
    fzf_select_path ──────────▶ fzf_select_icon
           │                             │
           ▼                             ▼
    find_next_5x_number ──────▶ generate_session_block
           │                             │
           ▼                             ▼
    preview_session ──────────▶ confirm("Add?")
           │                             │
           ▼                             ▼
    add_session() ────────────▶ sesh.toml updated
```

### Delete Session Flow
```
User: seshy delete
         │
         ▼
    list_sessions() ──────────▶ fzf_select()
         │                             │
         ▼                             ▼
    confirm("Delete?") ───────▶ delete_session()
         │                             │
         ▼                             ▼
    Session + windows removed from sesh.toml
```

### Startup Flow
```
User: seshy startup [group]
         │
         ▼
    get_startup_groups() ─────▶ Pattern matching (fnmatch)
         │                             │
         ▼                             ▼
    list_sessions() ──────────▶ match_sessions()
         │                             │
         ▼                             ▼
    For each match: subprocess("sesh connect <name>")
         │
         ▼
    Report: "Launched X sessions, Y failures"
```

## Conventions

| Convention | Description |
|------------|-------------|
| **Workflow Pattern** | High-level workflows in `workflows/` delegate to core modules |
| **Thin CLI** | `cli.py` does minimal work, delegates to workflows |
| **TOML Preservation** | Uses `tomlkit` to preserve formatting/comments |
| **Session Numbering** | 50-range (51, 52, 53...) for branch sessions |
| **Session Name Format** | `"{number} {name} {icon}"` (e.g., "52 feature-branch") |
| **Path Format** | Tilde-prefixed paths (`~/code/...`) for portability |
| **Window Defaults** | 4 windows per session: editor, dual, lazydocker, lazygit |
| **FZF Integration** | All interactive selection via `fzf` subprocess |

## Gotchas

### Dual Configuration Files
- `~/.config/sesh/sesh.toml` - sesh's session config (this tool **modifies** it)
- `~/.config/seshy/config.toml` - seshy's own settings (icons, paths, groups)

### Editor Integration
`read` and `update` commands use `os.execvp()` to replace the process with nvim - they never return to Python.

### Delete Complexity
Deletion must find and remove both `[[session]]` block AND its associated `[[window]]` blocks; uses window count from parsed TOML to determine end boundary.

### FZF Dependency
All interactive selection requires `fzf` to be installed. Subprocess calls will fail if not found.

### Session Numbering
`find_next_5x_number()` scans existing sessions to find the next available number in the 50-range sequence.

## Navigation Guide

**To add a session quickly**: `seshy add --quick` (uses current directory)

**To add interactively**: `seshy add` (fzf prompts for path and icon)

**To edit a session**: `seshy update` (opens nvim at session line)

**To delete a session**: `seshy delete` (fzf select, then confirm)

**To launch a group**: `seshy startup work` (launches all matching sessions)

**To list all sessions**: `seshy list`

**To view session config**: `seshy read` (opens sesh.toml in nvim)

## Key Entry Points

| Entry Point | Location | Purpose |
|-------------|----------|---------|
| CLI main | `src/seshy/cli.py:main()` | Application entry, exception handling |
| Add workflow | `src/seshy/workflows/add.py:run()` | Session creation |
| Delete workflow | `src/seshy/workflows/delete.py:run()` | Session deletion |
| Startup workflow | `src/seshy/workflows/startup.py:run()` | Group launching |
| TOML operations | `src/seshy/toml_ops.py` | All sesh.toml manipulation |
