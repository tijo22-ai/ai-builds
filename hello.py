import os
from ollama import chat
from dotenv import load_dotenv
load_dotenv()
model = os.getenv("OLLAMA_MODEL")
question = input("Whats your question: ")
response = chat (
    model = model, 
    messages =[{"role":"user", "content":question}],
    think=False
)
print (response.message.content)