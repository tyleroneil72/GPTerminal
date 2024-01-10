#!/bin/bash

# Install dependencies
pip3 install -r requirements.txt
# Make the script executable
chmod +x GPTerminal.py
# Make the uninstallation script executable
chmod +x uninstallation.sh
# Create a symbolic link to move the script to a directory in your PATH
sudo ln -s $(pwd)/GPTerminal.py /usr/local/bin/GPTerminal

echo -e "\033[32mGPTerminal has been installed.\033[0m"
