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

echo "Done! Run 'seshy --help' to get started."
