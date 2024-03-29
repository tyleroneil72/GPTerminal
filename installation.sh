#!/bin/bash

# Install dependencies
pip3 install -r requirements.txt

# Make the script executable
chmod +x GPTerminal.py

# Create a symbolic link to move the script to a directory in your PATH
sudo ln -s $(pwd)/GPTerminal.py /usr/local/bin/GPTerminal

# Print the ASCII art with proper indentation only if the terminal is wide enough
if [ "$(tput cols)" -gt 55 ]; then
    echo "$(tput setaf 2)"
    echo ""
    echo "   ___   ___  _____                    _             _  "
    echo "  / _ \ / _ \/__   \___ _ __ _ __ ___ (_)_ __   __ _| | "
    echo " / /_\// /_)/  / /\/ _ \ '__| '_ \` _ \| | '_ \ / _\` | | "
    echo "/ /_\\ / ___/  / / |  __/ |  | | | | | | | | | | (_| | | "
    echo "\____/\/      \/   \___|_|  |_| |_| |_|_|_| |_|\__,_|_| "
    echo ""
    echo "$(tput sgr0)"
fi

# Print the installation message
echo -e "\033[32mGPTerminal has been installed. Run \033[34m'GPTerminal -h'\033[32m or \033[34m'GPTerminal --help'\033[32m for available commands.\033[0m"

