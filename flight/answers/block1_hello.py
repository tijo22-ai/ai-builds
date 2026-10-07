# Block 1 answer: hello.py, rewritten from a blank file.
# Run from the ai-builds folder:  uv run hello.py

import os

from dotenv import load_dotenv
from ollama import chat

# Reads the .env file in the folder you run from. Each laptop has its own .env,
# so the same code uses qwen3:8b on the Mac and qwen3:14b on the Windows PC.
load_dotenv()
MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")  # second value = fallback if .env is missing

question = input("Ask Qwen something: ")

response = chat(
    model=MODEL,
    messages=[{"role": "user", "content": question}],
    think=False,  # skip Qwen's hidden reasoning: faster replies, less battery
)

# The reply is nested: response -> message -> content
print(response.message.content)
