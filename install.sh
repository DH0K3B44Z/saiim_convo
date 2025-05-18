#!/data/data/com.termux/files/usr/bin/bash

echo "Updating packages..."
pkg update -y && pkg upgrade -y

echo "Installing Python and required packages..."
pkg install python -y
pip install --upgrade pip
pip install requests

echo "Setup complete!"
echo "You can now run: bash main.sh"
