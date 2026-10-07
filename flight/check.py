"""Offline self-checks for each block. Claude isn't on the plane; this is your reviewer.

Run from the ai-builds folder:
    uv run flight/check.py 3            checks YOUR pricing.py
    uv run flight/check.py 3 --answers  checks the sealed answer instead (to see what PASS looks like)

PASS means the code behaves correctly. It does NOT mean the block is done:
the gate is PASS *and* you can explain every line out loud.
"""

import builtins
import os
import sys
import time

ROOT = os.getcwd()
ANSWERS = os.path.join(ROOT, "flight", "answers")

# Which file each block's functions live in: (your file, answer file)
FILES = {
    "drills": ("drills", "block2_drills"),
    "pricing": ("pricing", "block3_pricing"),
    "enquiry": ("enquiry", "block4_enquiry"),
    "intake": ("intake", "block5_intake"),
    "followup": ("intake", "block6_followup"),
    "orchestrator": ("orchestrator", "block7_orchestrator"),
}

passed = 0
failed = 0


def ok(label):
    global passed
    passed += 1
    print(f"  PASS  {label}")


def bad(label, meaning):
    global failed
    failed += 1
    print(f"  FAIL  {label}")
    print(f"        -> {meaning}")


class AskedForInput(Exception):
    pass


def no_input(*args, **kwargs):
    raise AskedForInput()


def load(kind, use_answers):
    """Import your module (or the answer), with input() blocked so a stray loop can't hang the check."""
    name = FILES[kind][1] if use_answers else FILES[kind][0]
    folder = ANSWERS if use_answers else ROOT
    if not os.path.exists(os.path.join(folder, name + ".py")):
        print(f"\n  Can't find {name}.py in {folder}")
        print(f"  Create it in the ai-builds folder (same level as hello.py), then run this again.")
        sys.exit(1)
    if folder not in sys.path:
        sys.path.insert(0, folder)
    real_input = builtins.input
    builtins.input = no_input
    try:
        return __import__(name)
    except AskedForInput:
        print(f"\n  {name}.py asked for input() the moment it was imported.")
        print("  Put your input loop under   if __name__ == \"__main__\":   (see HINTS.md, Block 3).")
        sys.exit(1)
    finally:
        builtins.input = real_input


def has(module, func):
    if hasattr(module, func):
        return True
    bad(f"{func}() exists", f"Couldn't find a function called {func} in {module.__name__}.py. Check the spelling.")
    return False


def check_2(a):
    m = load("drills", a)
    if has(m, "parse_messy"):
        got = m.parse_messy("Name: Priya Shah | Phone: 780-555-0142 | Job: leaky faucet")
        want = {"name": "Priya Shah", "phone": "780-555-0142", "job": "leaky faucet"}
        ok("parse_messy basic") if got == want else bad("parse_messy basic", f"Got {got}, wanted {want}. Check strip() and lower().")
        got = m.parse_messy("When: Thursday 10:30")
        ok("value containing a colon") if got == {"when": "Thursday 10:30"} else bad(
            "value containing a colon", f"Got {got}. split(':') splits at EVERY colon. Look up split's second argument.")
        try:
            got = m.parse_messy("hello there | name: Sam")
            ok("junk piece skipped") if got == {"name": "Sam"} else bad("junk piece skipped", f"Got {got}, wanted {{'name': 'Sam'}}.")
        except Exception as e:
            bad("junk piece skipped", f"Crashed with {type(e).__name__}: {e}. A piece with no ':' should be skipped.")
    if has(m, "merge"):
        defaults = {"urgency": "flexible", "location": None}
        got = m.merge(defaults, {"location": "Mill Woods", "urgency": None})
        ok("merge keeps defaults, None doesn't overwrite") if got == {"urgency": "flexible", "location": "Mill Woods"} else bad(
            "merge keeps defaults, None doesn't overwrite", f"Got {got}.")
        ok("merge doesn't change the original dict") if defaults == {"urgency": "flexible", "location": None} else bad(
            "merge doesn't change the original dict", "Your merge changed `defaults`. Work on a copy: dict(defaults).")


def check_3(a):
    m = load("pricing", a)
    if not (has(m, "load_rules") and has(m, "get_price")):
        return
    try:
        rules = m.load_rules("data/rules.csv")
    except FileNotFoundError:
        bad("load_rules reads data/rules.csv", "File not found. Run this from the ai-builds folder.")
        return
    ok("load_rules returns a dict") if isinstance(rules, dict) else bad("load_rules returns a dict", f"Got {type(rules).__name__}.")
    if not isinstance(rules, dict):
        return
    ok("leaky_faucet is a key") if "leaky_faucet" in rules else bad("leaky_faucet is a key", f"Keys are: {list(rules)[:6]}")
    rule = rules.get("leaky_faucet", {})
    nums = [rule.get(k) for k in ("low", "high", "urgent_fee")]
    if all(isinstance(n, int) for n in nums):
        ok("prices are numbers, not text")
        ok("low <= high for every job") if all(r["low"] <= r["high"] for r in rules.values()) else bad(
            "low <= high for every job", "Check the low/high columns.")
    else:
        bad("prices are numbers, not text", f"Got {nums}. csv gives text; wrap with int().")
    try:
        ok("unknown job returns None") if m.get_price(rules, "roofing") is None else bad("unknown job returns None", "It should return None.")
    except Exception as e:
        bad("unknown job returns None", f"Crashed with {type(e).__name__}. Use .get() instead of [ ].")


def check_4(a):
    m = load("enquiry", a)
    if not (has(m, "Enquiry") and has(m, "parse_json")):
        return
    from pydantic import ValidationError
    ok("parse_json good") if m.parse_json('{"a": 1}') == {"a": 1} else bad("parse_json good", "Should return {'a': 1}.")
    try:
        ok("parse_json broken -> None") if m.parse_json("{oops") is None else bad("parse_json broken -> None", "Should return None.")
    except Exception as e:
        bad("parse_json broken -> None", f"Crashed with {type(e).__name__}. Wrap json.loads in try/except json.JSONDecodeError.")
    base = {"job_type": "leaky_faucet", "urgency": "soon", "customer_name": "Priya",
            "phone": None, "location": "Mill Woods", "details": "Kitchen tap drips"}
    try:
        m.Enquiry.model_validate(base)
        ok("valid enquiry accepted (phone can be None)")
    except ValidationError as e:
        bad("valid enquiry accepted (phone can be None)", f"Rejected: {e.errors()[0]['loc']} {e.errors()[0]['msg']}. Use `str | None` for optional fields.")
    try:
        m.Enquiry.model_validate({**base, "job_type": "roofing"})
        bad("unknown job_type rejected", "Accepted 'roofing'. job_type should be a Literal[...] of allowed values.")
    except ValidationError:
        ok("unknown job_type rejected")
    try:
        m.Enquiry.model_validate({**base, "urgency": "whenever"})
        bad("unknown urgency rejected", "Accepted 'whenever'. urgency should be a Literal[...] too.")
    except ValidationError:
        ok("unknown urgency rejected")
    import csv
    with open("data/rules.csv", newline="") as f:
        csv_jobs = [row["job_type"] for row in csv.DictReader(f)]
    missing = []
    for job in csv_jobs + ["other"]:
        try:
            m.Enquiry.model_validate({**base, "job_type": job})
        except ValidationError:
            missing.append(job)
    ok("every job_type in rules.csv (+ 'other') is allowed") if not missing else bad(
        "every job_type in rules.csv (+ 'other') is allowed", f"Not allowed: {missing}. Quoting would silently fail for these.")


def check_5(a):
    m = load("intake", a)
    if not has(m, "extract"):
        return
    text = ("Hi, I'm Priya Shah. My kitchen tap won't stop dripping, can someone come Thursday? "
            "780-555-0142, Mill Woods.")
    print("  Calling the model (10-60 seconds)...")
    start = time.time()
    try:
        e = m.extract(text)
    except ConnectionError:
        bad("model reachable", "Ollama isn't running. Open the Ollama app (menu bar) and try again.")
        return
    except Exception as err:
        bad("extract() returns an Enquiry", f"{type(err).__name__}: {str(err)[:300]}")
        return
    print(f"  Took {time.time() - start:.1f}s -> {e}")
    ok("extract() returns an Enquiry") if type(e).__name__ == "Enquiry" else bad("extract() returns an Enquiry", f"Got {type(e).__name__}.")
    ok("job_type = leaky_faucet") if getattr(e, "job_type", None) == "leaky_faucet" else bad(
        "job_type = leaky_faucet", "Wrong category. Tighten the job_type rule in your system prompt.")
    ok("phone copied, not invented") if "555-0142" in str(getattr(e, "phone", "")) else bad(
        "phone copied, not invented", f"Got {getattr(e, 'phone', None)}.")
    e2 = m.extract("toilet keeps running all night. no rush. - Marco")
    print(f"  No-phone message -> phone={e2.phone!r}, location={e2.location!r}")
    ok("missing phone stays None") if not e2.phone else bad(
        "missing phone stays None", "The model invented a phone number. Tell it to use null when a detail isn't stated.")


def check_6(a):
    f = load("followup", a)
    en = load("enquiry", a)
    if not (has(f, "missing_fields") and has(f, "follow_up_question")):
        return
    full = en.Enquiry.model_validate({"job_type": "leaky_faucet", "urgency": "soon", "customer_name": "Priya",
                                      "phone": "780-555-0142", "location": "Mill Woods", "details": "Tap drips"})
    part = full.model_copy(update={"phone": None, "location": ""})
    got = f.missing_fields(part)
    ok("missing_fields finds phone and location") if sorted(got) == ["location", "phone"] else bad(
        "missing_fields finds phone and location", f"Got {got}. An empty string \"\" should count as missing too.")
    ok("complete enquiry -> nothing missing") if f.missing_fields(full) == [] else bad(
        "complete enquiry -> nothing missing", f"Got {f.missing_fields(full)}.")
    q = f.follow_up_question(part)
    ok("follow-up question when something's missing") if isinstance(q, str) and q else bad(
        "follow-up question when something's missing", f"Got {q!r}.")
    ok("no question when complete") if f.follow_up_question(full) is None else bad("no question when complete", "Should return None.")
    path = "data/enquiries.txt"
    if os.path.exists(path):
        with open(path) as fh:
            n = len([line for line in fh if line.strip()])
        ok(f"data/enquiries.txt has 10+ enquiries ({n})") if n >= 10 else bad(
            "data/enquiries.txt has 10+ enquiries", f"Only {n}. Write your own; one per line.")
    else:
        bad("data/enquiries.txt exists", "Write 10 made-up enquiries, one per line (see Block 5 break).")


def check_7(a):
    m = load("orchestrator", a)
    if not has(m, "handle"):
        return
    for text in ["Leaky tap in the kitchen. Priya Shah, 780-555-0142, Mill Woods. Thursday?",
                 "shower drain blocked again"]:
        print(f"\n  IN:  {text}")
        reply = m.handle(text)
        print("  OUT: " + str(reply).replace("\n", "\n       "))
        ok("handle() returned a reply") if isinstance(reply, str) and reply.strip() else bad("handle() returned a reply", "Empty reply.")
    print("\n  Read both replies. The first should be a quote; the second should ask for details.")


CHECKS = {"2": check_2, "3": check_3, "4": check_4, "5": check_5, "6": check_6, "7": check_7}

if __name__ == "__main__":
    if not os.path.exists("pyproject.toml") or not os.path.isdir("flight"):
        print("Run this from the ai-builds folder:  cd ~/ai-builds  (or wherever you cloned it)")
        sys.exit(1)
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not args or args[0] not in CHECKS:
        print("Usage: uv run flight/check.py <block number 2-7> [--answers]")
        sys.exit(1)
    use_answers = "--answers" in sys.argv
    print(f"Block {args[0]} check" + (" (sealed answers)" if use_answers else "") + ":")
    CHECKS[args[0]](use_answers)
    print(f"\n{passed} passed, {failed} failed.")
    if failed == 0 and passed:
        print("Gate: can you explain every line out loud? If yes, commit and move on.")
