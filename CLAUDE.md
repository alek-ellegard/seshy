# Seshy

CLI for managing sesh.toml tmux sessions.

## Commands

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

## Project Structure

```
src/seshy/
├── cli.py        # Click CLI commands
├── toml_ops.py   # TOML parsing/modification
└── fzf.py        # fzf subprocess helpers
```

## Install

```bash
uv tool install -e .
```
