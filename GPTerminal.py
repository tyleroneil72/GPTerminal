#!/usr/bin/env python3
import sys
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")

client = OpenAI(
  api_key=API_KEY
)

def main():
    if len(sys.argv) > 1:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": sys.argv[1]}],
        )
        print(response.choices[0].message.content)
        
    else:
        print("No input provided.")

if __name__ == "__main__":
    main()
