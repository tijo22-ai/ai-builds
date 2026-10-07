# Block 6 answer, part 2: batch.py
# Runs every line of data/enquiries.txt through the intake agent and saves the results.
# Run:  uv run batch.py   (yours)   or   uv run flight/answers/block6_batch.py

import json

from pydantic import ValidationError

from block5_intake import extract
from block6_followup import follow_up_question

with open("data/enquiries.txt") as f:
    lines = []
    for line in f:
        if line.strip():                 # skip blank lines
            lines.append(line.strip())

results = []
ok = 0
for number, text in enumerate(lines, start=1):
    print(f"[{number}/{len(lines)}] {text[:60]}...")
    try:
        enquiry = extract(text)
    except ValidationError as err:       # the model returned something that doesn't fit the schema
        print("   FAILED:", err.error_count(), "problems")
        results.append({"text": text, "record": None, "error": str(err), "follow_up": None})
        continue
    ok += 1
    question = follow_up_question(enquiry)
    print("  ", enquiry.job_type, "|", enquiry.urgency, "| follow-up:", question or "none needed")
    results.append({"text": text, "record": enquiry.model_dump(), "error": None, "follow_up": question})

with open("data/intake_results.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\n{ok}/{len(lines)} parsed. Saved to data/intake_results.json")
print("Valid is not the same as correct: open the JSON and check every record by hand.")
