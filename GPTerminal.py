#!/usr/bin/env python3
import sys
from openai import OpenAI
client = OpenAI()

def main():
    if len(sys.argv) > 1:
        print("testing")
    else:
        print("No input provided.")

if __name__ == "__main__":
    main()
