#!/usr/bin/env python3
import openai
import argparse

# Default values for API_KEY and MODEL
API_KEY = "your_api_key_here"
MODEL = "gpt-3.5-turbo"

# Setup argument parser
description = """
GPTerminal - A CLI tool for interacting with OpenAI's GPT models.
Created by Tyler O'Neil. For more information, visit: https://tyleroneil.dev
"""
parser = argparse.ArgumentParser(description=description)
parser.add_argument('-setup', action='store_true', help='Setup or change the API_KEY for GPTerminal.')
parser.add_argument('-change-model', action='store_true', help='Change the GPT model.')
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

def setup_api_key():
    global API_KEY
    api_key = input("Enter your new API_KEY: ").strip()
    update_script(api_key, MODEL)
    API_KEY = api_key

def change_model():
    global MODEL
    MODEL = choose_model()
    update_script(API_KEY, MODEL)

def choose_model():
    print("Available models:")
    print("1: gpt-4")
    print("2: gpt-3.5-turbo")
    # Add more models here as needed
    choice = input("Select a model (number): ").strip()
    if choice == "1":
        return "gpt-4"
    elif choice == "2":
        return "gpt-3.5-turbo"
    else:
        print("Invalid choice. Defaulting to gpt-3.5-turbo.")
        return "gpt-3.5-turbo"

def main():
    if args.setup:
        setup_api_key()
    elif args.change_model:
        change_model()
    elif args.query:
        if API_KEY == "your_api_key_here":
            print("API_KEY not set. Please run 'GPTerminal -setup' first.")
            return
        client = openai.OpenAI(api_key=API_KEY)
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": args.query}],
        )
        print(response.choices[0].message.content)
    else:
        print("No input provided or invalid command. Use '-h' or '--help' for available commands.")

if __name__ == "__main__":
    main()
