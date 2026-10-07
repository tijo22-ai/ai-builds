# Hints, the stuck ladder and the local tutor

## When you're stuck, in this order

1. **Read the last line of the error.** It names the problem. The line just above it, with a line number, shows where.
2. Check the **common errors** table below.
3. Open the hints for your step. **Hint 1 → try again → Hint 2 → try again → Hint 3.**
4. Ask the **local tutor** (next section).
5. Only after two honest tries and all three hints: the sealed answer in `answers/`. Read `answers/README.md` first.
6. Write what happened in `flight-log.md`, even if you solved it. Your "what broke" notes are what we'll work through after you land.

## The local tutor (Qwen, offline)

Open a **second Terminal tab** (Cmd+T) and run:

```bash
ollama run qwen3:8b
```

Paste this first, then your code or error:

```text
You are my Python tutor. I'm a beginner. When I paste code or an error:
explain in plain words why it happens and point to the line. Give me a
hint, not fixed code. Only show code if I write "show me".
```

- Type `/bye` to leave.
- For faster, shorter answers, type `/set nothink` first. **[Likely]**
- A local 8B model can be confidently wrong. **[Likely]** If it contradicts these hints or `check.py`, trust the hints and the check.

## Common errors

| You see | What it means | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'ollama'` | You ran `python file.py`, which uses a Python without your packages | Use `uv run file.py` |
| `ConnectionError: Failed to connect to Ollama` | The Ollama app isn't running | Open Ollama (llama icon in the menu bar) |
| `ResponseError: model "..." not found` | The name in `.env` doesn't match a pulled model | Compare `.env` with `ollama list`, letter by letter |
| `KeyError: 'phone'` | That key isn't in the dict | `print(the_dict.keys())`; use `.get("phone")` if it may be missing |
| `TypeError: can only concatenate str (not "int") to str` | Joining text and a number with `+` | Use an f-string: `f"${low}"` |
| `FileNotFoundError: data/rules.csv` | You're running from the wrong folder | `pwd` should end in `ai-builds`; `cd ~/ai-builds` |
| `json.JSONDecodeError` | The text isn't valid JSON | `print()` the text first and look at it |
| `pydantic ... ValidationError` | Data doesn't fit your model | Read the field name on the error line, then the reason under it |
| `IndentationError` | Spaces don't line up | Use 4 spaces per level; never mix tabs and spaces |
| `NameError: name 'x' is not defined` | Typo, or used before it was created | Check spelling and the order of your lines |
| uv says it **failed to fetch** or **offline** | Something tried to download | You changed dependencies. Don't `uv add` on the plane. Undo with `git checkout pyproject.toml uv.lock` |
| Program seems frozen | It's waiting at `input()`, or loading the model (first call takes 10–60 s) | Type something, or wait a minute |
| Red underlines in VS Code, but `uv run` works | VS Code is using the wrong Python | Cmd+Shift+P → Python: Select Interpreter → `.venv` |

Your debugger is `print()`. Print the variable right before the line that breaks, and also `print(type(x))`. Most beginner bugs are "this isn't what I thought it was".

---

## Block 1: hello.py

**Hint 1.** Three jobs: get the model name, send the question, print the reply. The model name lives in `.env`. One package loads that file, and Python's `os` module reads values from it.

**Hint 2.** `load_dotenv()` (from the `dotenv` package) loads the file; then `os.getenv("OLLAMA_MODEL")` gives you the name. `chat()` needs `model=` and `messages=`. `messages` is a list of dicts, each with a `"role"` and `"content"`. You worked out the reply's nesting on Sept 28.

**Hint 3.** The order: imports (`os`, `load_dotenv`, `chat`) → `load_dotenv()` → `MODEL = os.getenv(...)` → `question = input(...)` → `response = chat(model=..., messages=[...], think=False)` → `print(response.message.content)`. `os.getenv` takes an optional second argument, a fallback if the name isn't found.

## Block 2: drills.py

### parse_messy

**Hint 1.** Two splits. First split the whole text on `|` to get pieces. Then split each piece on `:` into a label and a value.

**Hint 2.** `text.split("|")` gives a list you can loop over. `piece.split(":", 1)` splits at the **first** colon only, so `10:30` survives. `.strip()` trims spaces; `.lower()` turns `Name` into `name`. If `":" not in piece`, use `continue` to skip it.

**Hint 3.** Make an empty dict before the loop: `result = {}`. Inside the loop: `key, value = piece.split(":", 1)`, then `result[key.strip().lower()] = value.strip()`. Put `return result` **after** the loop, not inside it. Returning inside the loop stops after the first piece. That's a classic bug.

### merge

**Hint 1.** Start with a copy of `defaults`. Then go through `found` and copy each value over, skipping any that are `None`.

**Hint 2.** `dict(defaults)` makes a copy. `for key, value in found.items():` gives you both at once. `if value is not None:`

**Hint 3.** Why the copy: dicts are shared, not duplicated. If you change `defaults` directly, the caller's dict changes too, and `check.py 2` tests for exactly that.

## Block 3: pricing.py

**Hint 1.** `csv.DictReader` turns each row into a dict, using the header line as the keys. You want a dict of dicts, where the outer key is `job_type`.

**Hint 2.** `with open(path, newline="") as f:` then `for row in csv.DictReader(f):`. Everything from a CSV arrives as **text**: `"120"`, not `120`. Wrap prices in `int()`. For `get_price`: `rules.get(job_type)` returns `None` when the key is missing, while `rules[job_type]` crashes.

**Hint 3.** About `if __name__ == "__main__":`. Code under it runs only when you run that file directly (`uv run pricing.py`). It does **not** run when another file imports it (`check.py` now, `orchestrator.py` later). Without it, importing your file would stop and wait for typing. Put the input loop there: `while True:`, `job = input(...)`, `if job == "": break`.

## Block 4: enquiry.py

**Hint 1.** `Literal` means "only these exact values". A Pydantic `BaseModel` is a class that lists each field and its type. `str | None` means "text, or nothing".

**Hint 2.** Imports: `from typing import Literal` and `from pydantic import BaseModel, ValidationError`. Write `JobType = Literal["leaky_faucet", ..., "other"]`, then `class Enquiry(BaseModel):` with one `field_name: type` per line. `parse_json`: `try:` return `json.loads(text)`, `except json.JSONDecodeError:` return `None`.

**Hint 3.** Test it yourself at the bottom of the file, under `if __name__ == "__main__":`. Call `Enquiry.model_validate({...})` with a good dict. Then try a dict with `"job_type": "roofing"` inside `try` / `except ValidationError as err:` and `print(err)`. If `check.py 4` says a job type isn't allowed, compare your spelling with `rules.csv` letter by letter.

## Block 5: intake.py, extract()

**Hint 1.** It's the same `chat()` call as `hello.py`, plus three settings: `format` (the shape you want back), `think=False`, and `options` with temperature 0. Then turn the reply text into an `Enquiry`.

**Hint 2.** `format=Enquiry.model_json_schema()`. The reply's `message.content` is JSON text; `Enquiry.model_validate_json(...)` parses and checks it in one step. Send two messages: `{"role": "system", "content": YOUR_RULES}` and then `{"role": "user", "content": text}`. Import `Enquiry` from your own file: `from enquiry import Enquiry`.

**Hint 3.** Your system prompt should cover each field:
- `job_type`: pick from the list; use `other` if nothing fits
- `urgency`: how to tell emergency from soon from flexible
- `customer_name`, `phone`, `location`: copy exactly as written; use null if not stated; **never invent**
- `details`: one short sentence

Ollama's docs also suggest adding the schema to the prompt as text, with `json.dumps(Enquiry.model_json_schema())`. If the check says the phone was invented, make the "never invent" rule more specific.

## Block 6: follow-ups and batch.py

**Hint 1.** `missing_fields`: turn the Enquiry into a dict, loop over the fields you need, and collect the empty ones. `follow_up_question`: if nothing's missing, return `None`; otherwise build a sentence from the list.

**Hint 2.** `enquiry.model_dump()` gives a plain dict. `if not data.get(field):` catches both `None` and `""`. A dict that maps field names to friendly words, like `"phone": "a phone number"`, makes the question easy to build; `", ".join(words)` glues a list of words into one string.

**Hint 3.** For `batch.py`: read the lines and skip blanks. Loop with `for number, text in enumerate(lines, start=1):` so you can print progress. Wrap `extract(text)` in `try` / `except ValidationError:`; on failure, record it and `continue`. Collect one dict per enquiry in a list. After the loop, `json.dump(results, f, indent=2)` into `data/intake_results.json`. `enquiry.model_dump()` makes a record JSON-friendly.

**Scoring tip.** Look for patterns in the wrong ones. Five wrong `urgency` values point to one vague rule in your prompt, not five separate problems.

## Block 7: orchestrator.py

**Hint 1.** `handle(text)` is your three pieces in order: extract → follow-up check → price lookup. Each step can return early with its own reply.

**Hint 2.** `from intake import extract, follow_up_question` and `from pricing import load_rules, get_price`. Load the rules once at the top of the file, not on every call. Urgent means `enquiry.urgency == "emergency"`.

**Hint 3.** There are three possible endings: the follow-up question, a "needs a person" message (for `other`, or when `get_price` returns `None`), or the quote. `handle` **returns** a string; the input loop under `if __name__ == "__main__":` prints it.
