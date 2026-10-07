# Block 6 answer, part 1: add these two functions to your intake.py
# Check yours with:  uv run flight/check.py 6

# What we need before we can book, and how to ask for it in plain words.
NEEDED_TO_BOOK = {
    "customer_name": "your name",
    "phone": "a phone number",
    "location": "your address or neighbourhood",
}


def missing_fields(enquiry):
    """List the fields we still need, e.g. ['phone', 'location']."""
    data = enquiry.model_dump()          # Enquiry object -> plain dict
    missing = []
    for field in NEEDED_TO_BOOK:
        if not data.get(field):          # catches None and empty text ""
            missing.append(field)
    return missing


def follow_up_question(enquiry):
    """A question for the customer if something is missing, otherwise None."""
    missing = missing_fields(enquiry)
    if not missing:
        return None
    asks = []
    for field in missing:
        asks.append(NEEDED_TO_BOOK[field])
    return "Thanks for reaching out! To quote and book this, could you send " + ", ".join(asks) + "?"
