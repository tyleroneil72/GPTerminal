#!/usr/bin/env python3
import openai
import argparse

# Global default values
API_KEY = None
MODEL = "gpt-4"

# ANSI escape sequences for terminal colours
class Colours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Setup argument parser for command line interface
description = """
GPTerminal - A CLI tool for interacting with OpenAI's GPT models.
Created by Tyler O'Neil. Check out my website -> https://tyleroneil.dev
"""
epilog = "For more detailed instructions, visit https://github.com/tyleroneil72/GPTerminal"
parser = argparse.ArgumentParser(description=description, epilog=epilog)
parser.add_argument('-setup', action='store_true', help='Setup or change the API_KEY for GPTerminal.')
parser.add_argument('-change-model', action='store_true', help='Change the GPT model.')
parser.add_argument('query', nargs='?', default=None, help='Query to be processed by the GPT model.')
args = parser.parse_args()

def update_script(api_key, model):
    """Update the script file with new API key or model."""
    with open(__file__, 'r') as file:
        lines = file.readlines()

    with open(__file__, 'w') as file:
        for line in lines:
            if line.startswith('API_KEY ='):
                file.write(f'API_KEY = "{api_key}"\n')
            elif line.startswith('MODEL ='):
                file.write(f'MODEL = "{model}"\n')
            else:
                file.write(line)

def setup_api_key():
    """Prompt user to enter a new API key and update the script."""
    global API_KEY
    api_key = input("Enter your new API_KEY: ").strip()
    update_script(api_key, MODEL)
    API_KEY = api_key

def change_model():
    """Change the GPT model being used."""
    global MODEL
    MODEL = choose_model()
    update_script(API_KEY, MODEL)

def print_coloured(message, colour):
    """Print a message in the terminal with the specified colour."""
    print(colour + message + Colours.ENDC)

def choose_model():
    """Allow the user to choose a GPT model."""
    print_coloured("Available models:", Colours.OKBLUE)
    print_coloured("1: gpt-4", Colours.OKGREEN)
    print_coloured("2: gpt-3.5-turbo", Colours.OKGREEN)
    # Add more models here as needed
    choice = input("Select a model (number): ").strip()
    if choice == "1":
        return "gpt-4"
    elif choice == "2":
        return "gpt-3.5-turbo"
    else:
        print_coloured("Invalid choice. Defaulting to gpt-3.5-turbo.", Colours.WARNING)
        return "gpt-3.5-turbo"

def main():
    """Main function to handle command line arguments and execute corresponding actions."""
    if args.setup:
        setup_api_key()
    elif args.change_model:
        change_model()
    elif args.query:
        if not API_KEY:
            print_coloured("API_KEY not set. Please run 'GPTerminal -setup' first.", Colours.FAIL)
            return
        client = openai.OpenAI(api_key=API_KEY)
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": args.query}],
        )
        print_coloured(response.choices[0].message.content, Colours.OKBLUE)
    else:
        print_coloured("No input provided or invalid command. Use '-h' or '--help' for available commands.", Colours.FAIL)

if __name__ == "__main__":
    main()
