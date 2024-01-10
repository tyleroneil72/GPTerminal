#!/bin/bash

# Install dependencies
pip3 install -r requirements.txt
# Make the script executable
chmod +x GPTerminal.py
# Create a symbolic link to move the script to a directory in your PATH
sudo ln -s $(pwd)/GPTerminal.py /usr/local/bin/GPTerminal