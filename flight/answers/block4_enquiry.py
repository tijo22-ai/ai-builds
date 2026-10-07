# Block 4 answer: enquiry.py
# Check yours with:  uv run flight/check.py 4

import json
from typing import Literal

from pydantic import BaseModel, ValidationError

# Must match the job_type column in data/rules.csv, plus "other" for anything else.
# If these drift apart, the quoting step silently fails. check.py tests this for you.
JobType = Literal[
    "leaky_faucet",
    "clogged_drain",
    "toilet_repair",
    "burst_pipe",
    "water_heater_repair",
    "water_heater_replace",
    "other",
]


class Enquiry(BaseModel):
    job_type: JobType
    urgency: Literal["emergency", "soon", "flexible"]
    customer_name: str | None   # "str | None" = text, or nothing if the customer didn't say
    phone: str | None
    location: str | None
    details: str                # one-line summary of the problem in plain words


def parse_json(text):
    """Return a dict from JSON text, or None if the text isn't valid JSON."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


if __name__ == "__main__":
    good = '{"job_type": "leaky_faucet", "urgency": "soon", "customer_name": "Priya", "phone": null, "location": "Mill Woods", "details": "Kitchen tap drips"}'
    data = parse_json(good)
    print(Enquiry.model_validate(data))

    print(parse_json("{this is broken"))   # None, not a crash

    try:
        Enquiry.model_validate({"job_type": "roofing", "urgency": "soon", "details": "x"})
    except ValidationError as err:
        print("Rejected, as it should be:", err.error_count(), "problems")
