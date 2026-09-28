from ollama import chat

response = chat(
    model="qwen3:14b",
    messages=[{"role": "user", "content": "Give me a business idea for Edmonton"}],
)

print(response.message.content)