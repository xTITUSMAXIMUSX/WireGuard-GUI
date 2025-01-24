#!/bin/bash

# Function to handle errors
handle_error() {
    echo "Error: $1" >&2
    exit 1
}

# Ensure the target directory exists
mkdir -p ~/.local/share/applications/WireGuard || handle_error "Failed to create WireGuard directory."

# Copy files to the target directory
cp wg.sh wireguard_gui ~/.local/share/applications/WireGuard/ || handle_error "Failed to copy wg.sh or wireguard_gui."
cp -R assets ~/.local/share/applications/WireGuard/ || handle_error "Failed to copy assets directory."

# Copy the desktop entry to the applications folder
cp wireguard.desktop ~/.local/share/applications/ || handle_error "Failed to copy wireguard.desktop."

# Check if wireguard.desktop exists before running sed
if [[ ! -f ~/.local/share/applications/wireguard.desktop ]]; then
    handle_error "wireguard.desktop not found after copying."
fi

# Update Paths in the .desktop file
sed -i "s/user/$USER/g" ~/.local/share/applications/wireguard.desktop || handle_error "Failed to update user in wireguard.desktop."

echo "Installation Complete"
