#!/bin/bash

set -e

echo "[1/3] Installing uv..."
curl -Ls https://astral.sh/uv/install.sh | sh

CARGO_BIN="$HOME/.cargo/bin"

echo "[2/3] Adding $CARGO_BIN to PATH..."

# Determine the appropriate shell configuration file
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bash_profile"
else
    SHELL_RC="$HOME/.profile"
fi

# Append to PATH if not already present
if ! grep -q 'export PATH="$HOME/.cargo/bin:$PATH"' "$SHELL_RC"; then
    echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> "$SHELL_RC"
    echo "Appended to: $SHELL_RC"
else
    echo "Already present in PATH."
fi

echo "[3/3] Done. Please open a new terminal session to apply changes."
