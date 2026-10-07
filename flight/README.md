# 12-hour flight plan: offline build sprint

**Start here.** If you haven't done `PREFLIGHT.md` yet, stop and do that first, while you still have internet.

## What this covers, honestly

The 8-week plan was about 40 hours. This flight is about 8½ hours of focused work, so it covers **weeks 1–4**, the pricing script and the intake agent, plus a stretch block that starts weeks 5–6. Booking, the front end and the case study come after you land.

One change from the 8-week plan: the intake agent runs on **Qwen through Ollama on the Mac**, not the Anthropic API. There's no internet on the plane, and it keeps the build zero-cloud. The code is the same shape either way.

## The rules (same as the 8-week plan)

1. **Gates.** Don't start a block until the last one's "Done when" is true. Done means `uv run flight/check.py <block>` passes **and** you can explain every line out loud.
2. **Explain, don't copy.** Claude isn't on the plane. Your fallback ladder is in `HINTS.md`: three hints per step, then the local tutor, then the sealed answers in `answers/`. If you open an answer, the block is **ASSISTED** and you rewrite it from blank within 48 hours of landing.
3. **Commit after every block.** `git commit` works offline. You push after landing.

Every block ends with a commit, so you can stop at any block boundary for a meal, a nap or a layover without losing your place.

## Start of the flight (10 min)

```bash
cd ~/ai-builds
export UV_OFFLINE=1
uv run flight/preflight_check.py
```

`export UV_OFFLINE=1` only lasts for that Terminal window. If you open a new window, run it again.

Then create `flight-log.md` in the `ai-builds` folder and paste this in:

```markdown
# Flight log

| Block | Start | End | DONE / ASSISTED / SKIPPED | What broke or confused me |
|-------|-------|-----|---------------------------|---------------------------|
| 1 | | | | |

## Intake scoring (Block 6)
| # | Correct? | What it got wrong |
|---|----------|-------------------|
```

This log becomes the raw material for your case study, and it's what you bring to Claude after you land.

**Battery rule:** plugged in → `qwen3:8b`. On battery and under 40% → change the line in `.env` to `OLLAMA_MODEL=qwen3:4b`. No code changes needed; that's why the model name lives in `.env`.

## The blocks

| Block | Time | You build | Done when |
|---|---|---|---|
| 1 | 45 min | `hello.py` from a blank file | It answers your typed question using the model named in `.env` |
| 2 | 90 min | `drills.py`: dicts, lists, functions | `check.py 2` passes |
| 3 | 90 min | `pricing.py`: reads the rules table | `check.py 3` passes; a job type you type prints its price |
| Break | 30 min | `data/enquiries.txt`: 10 messy enquiries | 10 lines, written by you |
| 4 | 75 min | `enquiry.py`: JSON, errors, the Enquiry shape | `check.py 4` passes |
| 5 | 90 min | `intake.py`: the intake agent | `check.py 5` passes |
| 6 | 90 min | Follow-up questions and `batch.py` for all 10 | `check.py 6` passes and 10/10 records are correct |
| 7 | 75 min | Stretch: `orchestrator.py`, intake to quote | `check.py 7`: a full message gets a quote, an incomplete one gets a question |
| End | 15 min | Commit, finish the log | |

Core (Blocks 1–6) is about 8½ hours. Block 7 is a bonus. The rest of the 12 hours is meals, sleep and walking the aisle. If you only finish Block 4, that's weeks 1–2 done properly, which beats six blocks done badly.

All your files go in the `ai-builds` folder, next to `hello.py`. Always run things from that folder.

---

### Block 1: hello.py from a blank file (45 min)

This is the gate left open since Sept 28.

- Open `hello.py`, select everything, delete it. Write it again without looking.
- New this time: read the model name from `.env` instead of typing `qwen3:14b` into the code. That's what lets one file work on both laptops.
- Add `think=False` to `chat()`. Qwen3 normally "thinks" before answering; turning that off makes replies faster and saves battery.

**Done when:** `uv run hello.py` asks for a question and prints Qwen's answer, and changing the model in `.env` (try `qwen3:4b`) changes which model answers, without touching the code.

```bash
git add .
git commit -m "Block 1: hello.py rewritten from blank"
```

### Block 2: dicts, lists, functions (90 min)

**Read (30 min max):** Automate the Boring Stuff ch 4 (Functions) and ch 7 (Dictionaries). Skim ch 6 (Lists) only if loops feel shaky.

**Build `drills.py`** with two functions. These are the exact moves the intake agent needs later.

1. `parse_messy(text)` turns messy labelled text into a dict:
   - `"Name: Priya Shah | Phone: 780-555-0142 | Job: leaky faucet"` → `{"name": "Priya Shah", "phone": "780-555-0142", "job": "leaky faucet"}`
   - Labels are lowercased, and spaces are trimmed from both sides.
   - A value can contain a colon: `"When: Thursday 10:30"` → `{"when": "Thursday 10:30"}`
   - A piece with no colon is skipped, not a crash.
2. `merge(defaults, found)` returns a new dict: start from `defaults`; a value from `found` wins **unless it's `None`**. `None` means "the model didn't find it". The original `defaults` must not change.

**Done when:** `uv run flight/check.py 2` passes and you can explain it. Commit.

### Block 3: the pricing script (90 min). Weeks 1–2 deliverable.

**Read:** ch 18, the CSV section only (stop at JSON). In the Python docs: `library/csv.html`, `DictReader`.

**Look at `data/rules.csv`.** It's a pricing table for one trade, plumbing, with made-up demo prices in CAD. If you'd rather demo a different trade later, you only change this file, not the code.

**Build `pricing.py`:**

- `load_rules(path="data/rules.csv")` returns a dict keyed by `job_type`. Each value is a dict with `description`, `low`, `high`, `urgent_fee`. **Prices must be numbers, not text.**
- `get_price(rules, job_type)` returns that job's dict, or `None` if there isn't one. Never crashes.
- A loop that asks for a job type and prints its price, until you enter a blank line. Put it under `if __name__ == "__main__":`. `HINTS.md` explains why.

**Done when:** `check.py 3` passes; `uv run pricing.py` → `leaky_faucet` prints a price range; `roofing` prints a polite "no rule" message. Commit.

### Break: write 10 enquiries (30 min, low battery use)

Create `data/enquiries.txt`. Write **10 made-up customer messages, one per line**, the way real people text a plumber. Include:

- one emergency (water everywhere)
- one with no phone number
- one with no name
- one job that isn't plumbing (a roof, a fence)
- typos, all-caps, "lol", "asap"
- Edmonton neighbourhoods; phone numbers in the 555 range so they're obviously fake

Don't open `answers/enquiries_example.txt`. Writing these yourself is the point, and they're part of your case study.

### Block 4: JSON, errors and the Enquiry shape (75 min)

**Read:** ch 18, the JSON section. Python docs `tutorial/errors.html`, sections 8.1–8.4. The Pydantic models PDF, "Basic model usage" only.

**Build `enquiry.py`:**

- `JobType`, a `Literal[...]` listing every `job_type` in `rules.csv` **plus `"other"`**
- `class Enquiry(BaseModel)` with these fields:
  - `job_type`: JobType
  - `urgency`: one of `"emergency"`, `"soon"`, `"flexible"`
  - `customer_name`, `phone`, `location`: text **or None**
  - `details`: text
- `parse_json(text)` returns a dict, or `None` if the text isn't valid JSON (use `try`/`except`)

This file is the contract between the AI and your code. The model has to fill this exact shape, and anything that doesn't fit gets rejected before it reaches pricing.

**Done when:** `check.py 4` passes. It also confirms your `JobType` matches `rules.csv`, a mismatch that would otherwise fail silently later. Commit.

### Block 5: the intake agent (90 min). First AI block.

**Read:** the Ollama structured outputs PDF (the Pydantic example) and the thinking PDF (just `think=False`).

**Build `intake.py`** with `extract(text)`: a messy customer message goes in, an `Enquiry` comes out.

- Same `chat()` call as `hello.py`, plus:
  - a **system message** with your rules for each field
  - `format=Enquiry.model_json_schema()`, which makes Ollama reply in exactly that shape
  - `think=False` and `options={"temperature": 0}`, so the same input gives the same output
- Turn the reply text into an `Enquiry` with Pydantic.

The hard part is the system prompt, not the code. The model must **copy** names and numbers, never invent them, and use null when something's missing.

**Done when:** `check.py 5` passes, and you've run three of your own enquiries through it and read the results. Commit.

### Block 6: all 10 enquiries, plus follow-up questions (90 min)

**Add to `intake.py`:**

- `missing_fields(enquiry)` returns a list of which of name / phone / location are missing (`None` or empty)
- `follow_up_question(enquiry)` returns a friendly question asking for what's missing, or `None` if nothing is

**Build `batch.py`:** read every line of `data/enquiries.txt`, run `extract` on each, catch a `ValidationError` instead of crashing, and save everything to `data/intake_results.json`.

**Then score it.** Open `intake_results.json`. For each record, mark it correct or wrong in your log, and why. The 8-week gate is **10 clean, correct records**, not just 10 that parsed. If it's under 10, improve the system prompt and run the batch again. Each round of "read the wrong ones, fix the prompt" is the most valuable hour of the flight.

If you're stuck at 8/10 after three prompt rounds, log the failures and stop. `qwen3:14b` on the Windows PC may get them right; that's a useful finding, not a failure.

**Done when:** `check.py 6` passes and your score is in the log. Commit.

### Block 7 (stretch): connect intake to quoting (75 min)

**Build `orchestrator.py`** with `handle(text)`, which runs your pieces in order and returns one of three replies:

1. a follow-up question, if contact details are missing
2. "a person will look at this", for `other` or a job with no price rule
3. a readable quote, with the urgent fee added for emergencies

Import from your own `pricing.py` and `intake.py`. This is the first time your files work as a system.

**Done when:** `check.py 7` shows a quote for the complete message and a question for the incomplete one. Commit.

### End of flight (15 min)

```bash
git add .
git commit -m "Flight sprint: blocks 1-N"
git status        # should say "nothing to commit"
```

Finish the log: which blocks are DONE, ASSISTED or SKIPPED, and the three things that confused you most.

---

## After you land

1. **Push from the Mac:** `git push`.
2. **On Windows:** `git pull`, then `uv sync`. Copy `.env.example` to `.env` and set `OLLAMA_MODEL=qwen3:14b`.
3. **Rewrite every ASSISTED block from blank** within 48 hours.
4. **Bring `flight-log.md` to Claude.** Start with what broke and what the intake agent got wrong.
5. **Next in the 8-week plan:** finish weeks 5–6 if Block 7 didn't happen, then the booking agent, a simple front end and the one-page case study (weeks 7–8).
