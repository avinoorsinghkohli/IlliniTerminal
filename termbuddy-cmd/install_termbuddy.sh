#!/bin/bash

# Define the custom function file name and path
CUSTOM_FILE="$HOME/.zsh_custom_functions.zsh"
ZSHRC_FILE="$HOME/.zshrc"
SOURCE_FILE="script.sh"
SOURCE_LINE="source $CUSTOM_FILE"

# Install glow using Homebrew
if ! command -v glow &> /dev/null; then
    echo "Installing glow using Homebrew"
    brew install glow
else
    echo "Glow is already installed"
fi

# Install boxes using Homebrew
if ! command -v boxes &> /dev/null; then
    echo "Installing boxes using Homebrew"
    brew install boxes
else
    echo "Boxes is already installed"
fi

# Copy the custom functions file if it exists in the current directory
if [ -f "$SOURCE_FILE" ]; then
    echo "Copying custom functions from $SOURCE_FILE to $CUSTOM_FILE"
    cp "$SOURCE_FILE" "$CUSTOM_FILE"
else
    echo "Error: $SOURCE_FILE not found in the current directory"
    exit 1
fi

# Check if the source line is already in .zshrc
if ! grep -qF "$SOURCE_LINE" "$ZSHRC_FILE"; then
    echo "Adding source line to .zshrc"
    echo "" >> "$ZSHRC_FILE"  # Add a newline for clarity
    echo "$SOURCE_LINE" >> "$ZSHRC_FILE"
else
    echo "Source line already present in .zshrc"
fi

echo "Setup complete. Please restart your shell or run 'source ~/.zshrc' to apply changes."
