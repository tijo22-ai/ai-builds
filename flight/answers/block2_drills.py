# Block 2 answer: drills.py
# Check yours with:  uv run flight/check.py 2


def parse_messy(text):
    """Turn 'name: Priya | phone: 780-555-0142' into {'name': 'Priya', 'phone': '780-555-0142'}."""
    result = {}
    for piece in text.split("|"):          # ['name: Priya ', ' phone: 780-555-0142']
        if ":" not in piece:
            continue                       # skip junk with no label, instead of crashing
        key, value = piece.split(":", 1)   # the 1 means split only at the FIRST colon
        result[key.strip().lower()] = value.strip()
    return result


def merge(defaults, found):
    """Start from defaults; a value in found wins, unless it is None (None means 'not found')."""
    merged = dict(defaults)                # a copy, so we don't change the caller's dict
    for key, value in found.items():
        if value is not None:
            merged[key] = value
    return merged


if __name__ == "__main__":
    # This part runs only when you run this file directly, not when another file imports it.
    sample = "Name: Priya Shah | Phone: 780-555-0142 | Job: leaky faucet | When: Thursday 10:30"
    print(parse_messy(sample))
    print(merge({"urgency": "flexible", "location": None}, {"location": "Mill Woods", "urgency": None}))
