# Seshy

CLI for managing [sesh](https://github.com/joshmedeski/sesh) tmux sessions defined in `~/.config/sesh/sesh.toml`.

## Prerequisites

- [tmux](https://github.com/tmux/tmux)
- [sesh](https://github.com/joshmedeski/sesh) - smart tmux session manager
- [fzf](https://github.com/junegunn/fzf) - fuzzy finder (for interactive selection)
- [nvim](https://neovim.io/) - used by `read` and `update` commands
- [uv](https://docs.astral.sh/uv/) - Python package manager

Optional (used by shell window functions):
- [lazygit](https://github.com/jesseduffield/lazygit)
- [lazydocker](https://github.com/jesseduffield/lazydocker)

## Install

```bash
# One-liner
curl -fsSL https://raw.githubusercontent.com/alek-ellegard/seshy/master/install.sh | bash

# Or clone and install
uv tool install .
```

## Usage

```bash
# List all sessions
seshy list

# Add session interactively
seshy add

# Add session from current directory (quick mode)
seshy add -q

# Open sesh.toml in nvim
seshy read

# Select session and open at that line in nvim
seshy update

# Delete a session (with associated windows)
seshy delete

# Launch all sessions in a group
seshy startup <group>
```

### Shell Functions

To enable tmux window management functions (splits, editor layout, etc.):

```bash
# Add to your .zshrc / .bashrc
source "$(seshy shell-path)"
```

## Configuration

Sessions are defined in `~/.config/sesh/sesh.toml`. Seshy preferences (icons, groups) live in `~/.config/seshy/config.toml` (auto-created on first use).

### Startup Groups

Define groups in `~/.config/seshy/config.toml` to launch multiple sessions at once:

```toml
[groups]
work = ["dotfiles*", "project-*"]
```

Then run `seshy startup work`.
