#!/usr/bin/env python3
import openai
import argparse
import sys
import os
import subprocess
import readchar
from typing import Optional

# Global default values
API_KEY: Optional[str] = None
MODEL: str = "gpt-3.5-turbo"
SYSTEM_PROMPT: str = "You are GPTerminal, a version of Chat GPT that runs in the terminal."
# These are stored in the script itself rather than a config/env file to make it easier to install/uninstall the script

class Colours:
    """ANSI escape sequences for terminal colours."""
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def print_coloured(message: str, colour: str) -> None:
    """Print a message in the terminal with the specified colour."""
    print(colour + message + Colours.ENDC)

# Setup argument parser for command line interface
description = f"""
    GPTerminal - A CLI tool for interacting with OpenAI's GPT models.
    For more detailed instructions, visit {Colours.OKBLUE}https://github.com/tyleroneil72/GPTerminal{Colours.ENDC}
    """
epilog = f"Created by Tyler O'Neil. Check out my website -> {Colours.OKBLUE}https://tyleroneil.dev{Colours.ENDC}"

parser = argparse.ArgumentParser(description=description, epilog=epilog)
parser.add_argument('-setup', action='store_true', help='Setup or change the API_KEY for GPTerminal.')
parser.add_argument('-change-model', action='store_true', help='Change the GPT model.')
parser.add_argument('-change-prompt', action='store_true', help='Change the GPT system prompt.')
parser.add_argument('-update', action='store_true', help='Update the program. Must be ran in the same directory as the repository.')
parser.add_argument('-uninstall', action='store_true', help='Uninstall GPTerminal from the system.')
parser.add_argument('query', nargs='?', default=None, help='Query to be processed by the GPT model.')
args = parser.parse_args()

def update_script(api_key: str, model: str, system_prompt: str) -> None:
    """ Update the script with the new API_KEY and MODEL."""
    try:
        with open(__file__, 'r') as file:
            lines = file.readlines()

        with open(__file__, 'w') as file:
            for line in lines:
                if line.startswith('API_KEY: Optional[str] = None') and api_key is None:
                    file.write(line)
                elif line.startswith('API_KEY: Optional[str] ='):
                    file.write(f'API_KEY: Optional[str] = "{api_key}"\n')
                elif line.startswith('MODEL: str ='):
                    file.write(f'MODEL: str = "{model}"\n')
                elif line.startswith('SYSTEM_PROMPT: str ='):
                    file.write(f'SYSTEM_PROMPT: str = "{system_prompt}"\n')
                else:
                    file.write(line)
    except IOError as e:
        print_coloured(f"Error updating script: {e}", Colours.FAIL)
        sys.exit(1)

def setup_api_key() -> None:
    """Prompt user to enter a new API key and update the script."""
    global API_KEY
    api_key = input("Enter your new API_KEY: ").strip()
    update_script(api_key, MODEL, SYSTEM_PROMPT)
    API_KEY = api_key

def change_model() -> None:
    """Change the GPT model being used."""
    global MODEL
    MODEL = choose_model()
    update_script(API_KEY, MODEL, SYSTEM_PROMPT)

def choose_model() -> str:
    models = ["gpt-4", "gpt-3.5-turbo"]
    selected = 0
    print_coloured("Choose a model: (Arrow Keys)", Colours.OKGREEN)

    def print_models(first_time=False) -> None:
        if not first_time:
            # Move the cursor up by the number of models
            print(f"\033[{len(models)}A", end="")
        for idx, model in enumerate(models):
            if idx == selected:
                print(f"{Colours.OKGREEN}>{Colours.ENDC} {model}")
            else:
                print(f"  {model}")

    print_models(first_time=True)
    while True:
        key = readchar.readkey()
        if key == readchar.key.UP and selected > 0:
            selected -= 1
            print_models()
        elif key == readchar.key.DOWN and selected < len(models) - 1:
            selected += 1
            print_models()
        elif key == readchar.key.ENTER:
            break

    return models[selected]

def change_prompt() -> None:
    """Change the GPT system prompt."""
    global SYSTEM_PROMPT
    SYSTEM_PROMPT = input("Enter your new system prompt: ").strip()
    update_script(API_KEY, MODEL, SYSTEM_PROMPT)

def uninstall_script() -> None:
    """Uninstall the script by removing it from /usr/local/bin."""
    confirmation = input("Are you sure you want to uninstall GPTerminal? (yes/no): ").strip().lower()
    if confirmation in ["yes", "y"]:
        try:
            os.system("sudo rm /usr/local/bin/GPTerminal")
            print_coloured("GPTerminal has been uninstalled.", Colours.OKGREEN)
        except Exception as e:
            print_coloured(f"Error during uninstallation: {e}", Colours.FAIL)
    else:
        print_coloured("Uninstallation cancelled.", Colours.WARNING)

def update_program() -> None:
    """Update the script if new code has been pushed to the repository."""
    confirmation = input("Are you sure you want to update the script and overwrite all local changes? (yes/no): ").strip().lower()

    if confirmation in ["yes", "y"]:
        try:
            # Reset any local changes
            subprocess.run(["git", "reset", "--hard"], check=True)
            # Pull the latest changes from the repository and capture output
            result = subprocess.run(["git", "pull"], check=True, stdout=subprocess.PIPE, text=True)
            if "Already up to date." not in result.stdout:
                print_coloured("Script updated successfully.", Colours.OKGREEN)
            else:
                print_coloured("No updates were found. Your script is already up to date.", Colours.WARNING)
        except Exception as e:
            print_coloured(f"An error occurred while updating the script. Please make sure you are running this command in the repository directory: {e}", Colours.FAIL)
    else:
        print_coloured("Update cancelled.", Colours.WARNING)


def main() -> None:
    """Main function to handle command line arguments and execute corresponding actions."""
    try:
        if args.uninstall:
            uninstall_script()
        elif args.update:
            update_program()
        elif args.setup:
            setup_api_key()
        elif args.change_model:
            change_model()
        elif args.change_prompt:
            change_prompt()
        elif args.query:
            if not API_KEY:
                print_coloured("API_KEY not set. Please run 'GPTerminal -setup' first.", Colours.FAIL)
                return
            client = openai.OpenAI(api_key=API_KEY)
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": args.query}, {"role": "system", "content": SYSTEM_PROMPT}],
            )
            print_coloured(response.choices[0].message.content, Colours.OKBLUE)
        else:
            print_coloured("No input provided or invalid command. Use 'GPTerminal -h' or 'GPTerminal --help' for available commands.", Colours.FAIL)
    except Exception as e:
        print_coloured(f"An error occurred: {e}", Colours.FAIL)

if __name__ == "__main__":
    main()
