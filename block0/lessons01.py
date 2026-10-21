import os

job = "leaky faucet"
rate = 85
hours = "2"

total = rate * int(hours)

#leaky faucet: 2 hours at $85 = $170
print (f"{job}: {hours} hours at ${rate} = ${total}")

#B is false because its omparing the string "OLLAMA_MODEL " with the text "qwen3:8b"