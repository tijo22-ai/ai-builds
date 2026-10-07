# Pre-flight checklist (MacBook Air)

Do this **at least one day before you fly**. About 90 minutes, mostly waiting for downloads.

Everything that needs internet happens here. Section 7, the dry run, proves nothing on the plane needs it. Don't skip section 7: it's the only part that actually guarantees "nothing breaks".

Confidence tags: **[Certain]** checked or tested, **[Likely]** from current docs or reports, **[Guessing]** my estimate.

---

## 1. Get the latest repo onto the Mac (5 min)

Open **Terminal** (Cmd+Space, type Terminal).

```bash
cd ~/ai-builds          # or wherever you cloned it on Sept 28
git status
```

- If it says **"nothing to commit, working tree clean"**: run `git pull`.
- If it lists changed files, the Mac copy still has old edits from Sept 28. Don't try to merge them. Park the old folder and clone fresh:

```bash
cd ~
mv ai-builds ai-builds-old-mac
git clone https://github.com/tijo22-ai/ai-builds
cd ai-builds
```

Check: `ls flight` should list `README.md`, `PREFLIGHT.md`, `HINTS.md`, `check.py`, `preflight_check.py` and `answers`.

One more check, because this broke uv on both machines on Sept 28: run `ls ~/pyproject.toml`. If it shows a file (not "No such file"), move it out of the way with `mv ~/pyproject.toml ~/pyproject.toml.old`.

## 2. Python packages (5 min)

```bash
uv sync
cp .env.example .env
```

- `uv sync` downloads the Mac versions of everything the project uses, plus Python 3.12 if it's missing. I added `pydantic` as a direct dependency, so this picks it up. **[Certain]**
- `.env` tells your code which model this laptop uses (`qwen3:8b`). It's in `.gitignore`, so the Windows PC keeps its own `.env` with `qwen3:14b`. **[Certain]**
- **On the plane, never run `uv add`.** Adding a package needs the internet. If you find you need one, write it in your log for after landing.

## 3. Ollama models (20–40 min of downloading)

1. Look for the llama icon in the Mac menu bar. If Ollama isn't installed: https://ollama.com/download/mac
2. Pull two models:

```bash
ollama pull qwen3:8b    # main model, 5.2 GB
ollama pull qwen3:4b    # low-battery backup, 2.5 GB
ollama list             # both should be listed
```

Sizes are from the Ollama library page. **[Certain]**

- Why not `qwen3:14b` like on Windows: it's 9.3 GB, which leaves little of the Mac's 16 GB for everything else, and it would be slow and hard on the battery. **[Likely]**
- Never use a model tag with `cloud` in it. Those run on Ollama's servers and need internet. **[Certain]**

## 4. Offline reading (30 min)

```bash
mkdir ~/offline-docs
```

Save everything below into that folder. In Safari, **File → Export as PDF** saves the page you're looking at.

**a) Python's official docs, the whole site (13 MB zip)** **[Certain]**
https://docs.python.org/3.12/archives/python-3.12-docs-html.zip
Unzip it into `~/offline-docs`. Offline, open `index.html` in Safari. You'll use `tutorial/errors.html` and `library/csv.html`.

**b) Automate the Boring Stuff, 3rd edition (Export as PDF, one per chapter)** **[Certain the chapters exist]**
- Ch 4, Functions: https://automatetheboringstuff.com/3e/chapter4.html
- Ch 5, Debugging: https://automatetheboringstuff.com/3e/chapter5.html (your offline lifeline)
- Ch 6, Lists: https://automatetheboringstuff.com/3e/chapter6.html
- Ch 7, Dictionaries: https://automatetheboringstuff.com/3e/chapter7.html
- Ch 8, Strings: https://automatetheboringstuff.com/3e/chapter8.html
- Ch 18, CSV, JSON and XML: https://automatetheboringstuff.com/3e/chapter18.html

**c) The three pages your AI blocks depend on (Export as PDF)**
- Ollama structured outputs: https://docs.ollama.com/capabilities/structured-outputs
- Ollama thinking on/off: https://docs.ollama.com/capabilities/thinking
- Pydantic models: https://docs.pydantic.dev/latest/concepts/models/

**d) Ollama's own Python examples (real code you can read offline)**

```bash
git clone https://github.com/ollama/ollama-python ~/offline-docs/ollama-python
```

Look in its `examples` folder. **[Likely]** it includes a structured-outputs example; I couldn't open the folder listing to confirm.

**e) Already on your Mac, no download needed** **[Certain]**
`uv run python -m pydoc -b` opens Python's built-in help in your browser, offline. Or start `uv run python`, then type `help(dict)` or `help(str.split)`.

## 5. Editor (10 min)

1. VS Code, if you don't have it: https://code.visualstudio.com/download (pick the Mac Apple Silicon or Universal build).
2. In VS Code: Extensions (Cmd+Shift+X), search **Python**, install the one by Microsoft.
3. **File → Open Folder → ai-builds.**
4. Cmd+Shift+P → **Python: Select Interpreter** → pick the one with `.venv` in the path. Without this, VS Code underlines your imports in red even though `uv run` works fine. That kind of false alarm is exactly what you don't want offline.
5. Any AI coding extension (Copilot, Claude) won't work on the plane. Ignore it.

Reading Markdown in VS Code: open a `.md` file, press **Cmd+Shift+V** for the formatted preview.

## 6. Power (Qatar Airways)

- **Check your aircraft:** Manage Booking on qatarairways.com shows the aircraft type for each leg. In-seat power varies by aircraft and seat. Most long-haul economy seats have a power socket and USB. Some older or narrow-body economy seats have USB only. **[Likely]**
- **Pack:** the Apple charger and a USB-C to USB-C cable. If your seat only has a USB-C port, the cable may still charge the Mac slowly. **[Likely]**
- **Power bank rules** (April 2026 policy): at most two, each 100 Wh or less, in your cabin bag only, kept visible while in use, and you can't recharge the power bank on board. **[Likely]** Sources disagree on whether you can charge a laptop from one in flight. Ask the crew, and treat it as a backup, not your plan.
- **Battery:** charge to 100%. Turn on Low Power Mode (System Settings → Battery) and keep the brightness down. A MacBook Air on battery alone probably won't last 12 hours of coding plus running the model. **[Guessing]**

## 7. The dry run (20 min). This is the step that makes it safe.

1. **Wi-Fi ON:** from the `ai-builds` folder, run `uv run flight/preflight_check.py`. Fix every **FAIL**.
2. **Wi-Fi OFF:** click the Wi-Fi icon in the menu bar and turn it off.
3. Run:

```bash
export UV_OFFLINE=1
uv run flight/preflight_check.py
```

   Every line should be **OK**. The only acceptable WARNs are about reading material you've deliberately skipped.
4. Still offline: open one Python doc page and one Automate the Boring Stuff PDF. Then run `uv run flight/check.py 3 --answers`. It should print 5 PASS; that proves the self-checker works offline.
5. **Restart the Mac with Wi-Fi still off**, then repeat step 3. This proves Ollama starts without internet after a reboot. If step 3 now says "Ollama isn't running", open the Ollama app by hand. That's what you'll do on the plane too.
6. Turn Wi-Fi back on.

Don't test with the old `hello.py`. It asks for `qwen3:14b`, which isn't on the Mac, so it will fail. Rewriting it is Block 1.

If anything still says **FAIL**, paste the output into the chat with Claude **before** you fly.

## 8. The night before

- Don't update anything: no macOS update, no Ollama update, no `uv self update`. Updates change what you just tested. **[Certain]** that's the safe rule; nothing here needs the newest version.
- Charge to 100%.
- Put `flight/README.md` in a Safari tab or VS Code preview so it's the first thing you see.
