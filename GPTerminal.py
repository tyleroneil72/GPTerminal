#!/usr/bin/env python3
import openai
import argparse

# Default values for API_KEY and MODEL
API_KEY = "your_api_key_here"
MODEL = "your_model_here"

# Setup argument parser
description = """
GPTerminal - A CLI tool for interacting with OpenAI's GPT models.
Created by Tyler O'Neil. For more information, visit: https://tyleroneil.dev
"""
parser = argparse.ArgumentParser(description=description)
parser.add_argument('-setup', action='store_true', help='Setup API_KEY and MODEL for GPTerminal.')
parser.add_argument('-help', action='store_true', help='Show available commands.')
parser.add_argument('query', nargs='?', default=None, help='Query to be processed by the GPT model.')

args = parser.parse_args()

def update_script(api_key, model):
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

def setup_configuration():
    global API_KEY, MODEL
    api_key = input("Enter your API_KEY: ").strip()
    model = input("Enter the MODEL: ").strip()
    update_script(api_key, model)
    API_KEY = api_key
    MODEL = model

def main():
    if args.setup:
        setup_configuration()
    elif args.help:
        parser.print_help()
    elif args.query:
        if API_KEY == "your_api_key_here" or MODEL == "your_model_here":
            print("API_KEY or MODEL not set. Please run 'GPTerminal -setup' first.")
            return
        client = openai.OpenAI(api_key=API_KEY)
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": args.query}],
        )
        print(response.choices[0].message.content)
    else:
        print("No input provided or invalid command. Use '-help' for available commands.")

if __name__ == "__main__":
    main()
