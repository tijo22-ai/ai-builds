# Block 5 answer: intake.py, part 1 (the intake agent)
# Check yours with:  uv run flight/check.py 5
#
# In your own repo this file imports from enquiry.py:   from enquiry import Enquiry
# The answers folder uses its own copy:
import json
import os

from dotenv import load_dotenv
from ollama import chat

from block4_enquiry import Enquiry

load_dotenv()
MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")

SYSTEM_PROMPT = """You are the intake desk for a plumbing company in Edmonton.
Read the customer's message and fill in the fields.
Rules:
- job_type: pick the closest match. If nothing fits, use "other".
- urgency: "emergency" if water is leaking or flooding right now, or they have no water;
  "soon" if they want someone in the next few days; otherwise "flexible".
- customer_name, phone, location: copy them exactly as written. If the message
  does not state one, use null. Never invent a name, number or address.
- details: one short sentence describing the problem.
Return JSON matching this schema:
""" + json.dumps(Enquiry.model_json_schema())


def extract(text):
    """Messy customer message in, validated Enquiry out (raises ValidationError if the model slips)."""
    response = chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        format=Enquiry.model_json_schema(),  # Ollama forces the reply into this shape
        think=False,                         # faster, less battery; thinking doesn't help extraction much
        options={"temperature": 0},          # same input, same output: easier to debug
    )
    return Enquiry.model_validate_json(response.message.content)


if __name__ == "__main__":
    message = input("Paste a customer message: ")
    print(extract(message))
