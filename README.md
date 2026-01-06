# Seshy

CLI for managing sesh.toml tmux sessions.

## Install

```bash
uv tool install -e .
```

## Usage

```bash
# List all sessions
seshy list

# Add session interactively
seshy add

# Add session from current git branch (quick mode)
seshy add -b

# Open sesh.toml in nvim
seshy read

# Select session and open at that line in nvim
seshy update

# Delete a session (with associated windows)
seshy delete
```
