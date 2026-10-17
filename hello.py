# hello.py: ask a local AI model a question and print the answer
import os
from ollama import chat
from dotenv import load_dotenv
# 1. read the model name from the .env file
load_dotenv()
model = os.getenv("OLLAMA_MODEL")
# 2. ask a question to user
question = input("Ask Qwen anything: ")
# 3. the question gets send to the model 
response = chat(
    model = model,
    messages = [{"role":"user", "content":question}],
    think = False
)
# 4. the answer from the model gets printed
print(response.message.content)