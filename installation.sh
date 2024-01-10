#!/bin/bash

# Install dependencies
pip3 install -r requirements.txt

# Make the script executable
chmod +x GPTerminal.py

# Create a symbolic link to move the script to a directory in your PATH
sudo ln -s $(pwd)/GPTerminal.py /usr/local/bin/GPTerminal

# Print the ASCII art with proper indentation
echo "$(tput setaf 2)"
echo ""
echo "   ___   ___  _____                    _             _  "
echo "  / _ \ / _ \/__   \___ _ __ _ __ ___ (_)_ __   __ _| | "
echo " / /_\// /_)/  / /\/ _ \ '__| '_ \` _ \| | '_ \ / _\` | | "
echo "/ /_\\ / ___/  / / |  __/ |  | | | | | | | | | | (_| | | "
echo "\____/\/      \/   \___|_|  |_| |_| |_|_|_| |_|\__,_|_| "
echo ""
echo "$(tput sgr0)"

# Print the installation message
echo -e "\033[32mGPTerminal has been installed.\033[0m"
