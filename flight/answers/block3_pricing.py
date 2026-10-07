# Block 3 answer: pricing.py (the weeks 1-2 deliverable)
# Check yours with:  uv run flight/check.py 3
# Try it with:       uv run pricing.py

import csv


def load_rules(path="data/rules.csv"):
    """Read the rules table into {job_type: {description, low, high, urgent_fee}}."""
    rules = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):      # each row is a dict keyed by the header line
            rules[row["job_type"]] = {
                "description": row["description"],
                # CSV gives you text. '120' + '75' is '12075', so convert to int.
                "low": int(row["low"]),
                "high": int(row["high"]),
                "urgent_fee": int(row["urgent_fee"]),
            }
    return rules


def get_price(rules, job_type):
    """Return the rule for this job type, or None if there isn't one. Never crashes."""
    return rules.get(job_type)


def format_price(rule, urgent=False):
    text = f"{rule['description']}: ${rule['low']}-${rule['high']} CAD"
    if urgent:
        text += f" + ${rule['urgent_fee']} urgent call-out"
    return text


if __name__ == "__main__":
    rules = load_rules()
    print("Job types:", ", ".join(rules))
    while True:
        job = input("Job type (blank to quit): ").strip().lower()
        if job == "":
            break
        rule = get_price(rules, job)
        if rule is None:
            print("No price rule for that. A person will follow up.")
        else:
            print(format_price(rule))
