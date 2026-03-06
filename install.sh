#!/usr/bin/env bash
set -euo pipefail

REPO="https://github.com/alek-ellegard/seshy.git"
TMP_DIR=$(mktemp -d)

cleanup() { rm -rf "$TMP_DIR"; }
trap cleanup EXIT

# Check for uv
if ! command -v uv &>/dev/null; then
    echo "uv not found. Install it first: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "Cloning seshy..."
git clone --depth 1 "$REPO" "$TMP_DIR"

echo "Installing..."
uv tool install "$TMP_DIR"

# Create default sesh.toml if it doesn't exist
SESH_TOML="$HOME/.config/sesh/sesh.toml"
if [ ! -f "$SESH_TOML" ]; then
    echo ""
    echo "seshy requires ~/.config/sesh/sesh.toml to store session definitions."
    read -r -p "Create it now? [Y/n] " response
    case "$response" in
        [nN]*)
            echo "Skipped. Create it manually before using seshy."
            ;;
        *)
            mkdir -p "$(dirname "$SESH_TOML")"
            touch "$SESH_TOML"
            echo "Created $SESH_TOML"
            ;;
    esac
fi

echo ""
echo "Done! Run 'seshy --help' to get started."
echo ""
echo "To enable tmux window functions, add to your shell config:"
echo '  source "$(seshy shell-path)"'
