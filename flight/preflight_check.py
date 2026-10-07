"""Pre-flight check: proves the whole setup works with NO internet.

Run it twice, from the ai-builds folder:
  1. Now, with Wi-Fi ON:   uv run flight/preflight_check.py
  2. Then turn Wi-Fi OFF:  UV_OFFLINE=1 uv run flight/preflight_check.py

Only the Wi-Fi OFF run counts. Every line must say OK before you fly.
"""

import os
import platform
import shutil
import socket
import subprocess
import sys
import time

fails = 0
warns = 0


def show(status, label, fix=""):
    global fails, warns
    if status == "FAIL":
        fails += 1
    if status == "WARN":
        warns += 1
    print(f"  {status:4}  {label}")
    if fix:
        print(f"        -> {fix}")


print("\nPre-flight check\n")

# 1. Right folder
if os.path.exists("pyproject.toml") and os.path.exists("data/rules.csv"):
    show("OK", "Running from the ai-builds folder")
else:
    show("FAIL", "Not in the ai-builds folder", "cd into ai-builds first, then run this again.")
    sys.exit(1)

# 2. Are we actually offline?
try:
    socket.create_connection(("pypi.org", 443), timeout=3).close()
    show("WARN", "You're online", "Fine for run 1. For the real test, turn Wi-Fi OFF and run again.")
except OSError:
    show("OK", "No internet (good: this is the real test)")

if os.getenv("UV_OFFLINE") == "1":
    show("OK", "UV_OFFLINE=1 is set (uv won't try to download anything)")
else:
    show("WARN", "UV_OFFLINE isn't set", "On the plane, start with:  export UV_OFFLINE=1")

# 3. Python and packages
if sys.version_info >= (3, 12):
    show("OK", f"Python {platform.python_version()}")
else:
    show("FAIL", f"Python {platform.python_version()} is too old", "Run  uv sync  while online.")

try:
    import dotenv  # noqa: F401
    import ollama
    import pydantic  # noqa: F401
    show("OK", "Packages installed: ollama, pydantic, python-dotenv")
except ImportError as err:
    show("FAIL", f"Missing package: {err.name}", "While online, run:  uv sync")
    print(f"\n{fails} problem(s). Fix these first.")
    sys.exit(1)

# 4. .env and model name
from dotenv import load_dotenv

load_dotenv()
model = os.getenv("OLLAMA_MODEL")
if not os.path.exists(".env"):
    show("FAIL", "No .env file", "Run:  cp .env.example .env")
elif not model:
    show("FAIL", ".env has no OLLAMA_MODEL line", "Add:  OLLAMA_MODEL=qwen3:8b")
else:
    show("OK", f".env says OLLAMA_MODEL={model}")
model = model or "qwen3:8b"
if "cloud" in model:
    show("FAIL", f"{model} is a cloud model", "Cloud models need internet. Use qwen3:8b.")

# 5. Ollama running, models pulled
try:
    pulled = [m.model for m in ollama.list().models]
    show("OK", "Ollama is running")
except ConnectionError:
    pulled = None
    show("FAIL", "Ollama isn't running", "Open the Ollama app (llama icon in the menu bar), then run this again.")

if pulled is not None:
    if model in pulled:
        show("OK", f"{model} is downloaded")
    else:
        show("FAIL", f"{model} isn't downloaded", f"While online:  ollama pull {model}")
    if "qwen3:4b" in pulled:
        show("OK", "Low-battery backup qwen3:4b is downloaded")
    else:
        show("WARN", "No low-battery backup model", "While online:  ollama pull qwen3:4b  (2.5 GB)")

    # 6. Live test: same features your intake agent uses (schema, think=False, temperature 0)
    if model in pulled:
        from pydantic import BaseModel

        class City(BaseModel):
            city: str

        print(f"\n  Live test with {model} (first call loads the model: 10-60 s)...")
        start = time.time()
        try:
            reply = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": "Which city? 'Our office is in Edmonton, Alberta.'"}],
                format=City.model_json_schema(),
                think=False,
                options={"temperature": 0},
            )
            got = City.model_validate_json(reply.message.content)
            secs = time.time() - start
            if "edmonton" in got.city.lower():
                show("OK", f"Structured output works ({secs:.0f} s): {got}")
            else:
                show("WARN", f"Model answered {got.city!r}, expected Edmonton", "It runs, but check the model tag.")
        except Exception as err:
            show("FAIL", f"Live test failed: {type(err).__name__}: {str(err)[:200]}",
                 "Copy this error into the chat with Claude BEFORE you fly.")

# 7. Offline reading material
docs = os.path.expanduser("~/offline-docs")
if os.path.isdir(docs):
    n = sum(len(files) for _, _, files in os.walk(docs))
    show("OK" if n >= 8 else "WARN", f"~/offline-docs has {n} files",
         "" if n >= 8 else "Save the reading list in PREFLIGHT.md section 4.")
else:
    show("WARN", "No ~/offline-docs folder", "Create it and save the reading list (PREFLIGHT.md section 4).")

if os.path.exists("data/enquiries.txt"):
    show("OK", "data/enquiries.txt exists")

# 8. Disk and battery
free_gb = shutil.disk_usage(os.path.expanduser("~")).free / 1e9
show("OK" if free_gb > 10 else "WARN", f"{free_gb:.0f} GB free on disk",
     "" if free_gb > 10 else "Free up space; the model needs room to load.")
if platform.system() == "Darwin":
    try:
        batt = subprocess.run(["pmset", "-g", "batt"], capture_output=True, text=True).stdout
        line = [x for x in batt.splitlines() if "%" in x]
        show("OK", "Battery: " + (line[0].split("\t")[-1] if line else "unknown"))
    except OSError:
        pass

print()
if fails:
    print(f"NOT READY: {fails} problem(s). Fix them while you still have internet.")
elif warns:
    print(f"Ready, with {warns} warning(s). Read them; most matter only on the plane.")
else:
    print("READY. Nothing above needs internet.")
