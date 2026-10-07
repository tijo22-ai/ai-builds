# Block 7 answer (stretch): orchestrator.py
# Messy enquiry in -> follow-up question OR readable quote out. No manual steps in between.
# Run:  uv run orchestrator.py   (yours)   or   uv run flight/answers/block7_orchestrator.py

from block3_pricing import format_price, get_price, load_rules
from block5_intake import extract
from block6_followup import follow_up_question

RULES = load_rules()


def handle(text):
    enquiry = extract(text)                       # step 1: intake agent

    question = follow_up_question(enquiry)        # step 2: can we book this person?
    if question:
        return question

    rule = get_price(RULES, enquiry.job_type)     # step 3: quoting, from the rules table only
    if rule is None:                              # "other", or a job type with no rule
        return (f"Thanks {enquiry.customer_name}. This one needs a person to look at it. "
                f"We'll call you at {enquiry.phone}.")

    urgent = enquiry.urgency == "emergency"
    return (f"Hi {enquiry.customer_name}, thanks for your message about: {enquiry.details}\n"
            f"Estimate: {format_price(rule, urgent)}\n"
            f"Final price confirmed on site. Reply YES and we'll book a time at {enquiry.location}.")


if __name__ == "__main__":
    while True:
        text = input("\nCustomer message (blank to quit): ").strip()
        if not text:
            break
        print("\n" + handle(text))
