# Start here: your first session on the plane

The Claude app won't work on the plane, so this file is your guide. It tells you how to open everything, how each block works, and how to do Block 1 step by step. The plan itself (what to build in each block) is in `flight/README.md`.

---

## Part 1: Set up your screen (10 minutes)

1. **Wi-Fi stays off.** Airplane mode is fine; nothing here needs internet.
2. **Plug in** if your seat has power. Turn on **Low Power Mode** (System Settings → Battery) and turn the brightness down.
3. **Check Ollama is running.** Look for the llama icon at the top right of the screen. If it's not there: Cmd+Space, type **Ollama**, press Enter.
4. **Open VS Code**, then **File → Open Folder… → ai-builds** (in your home folder).
5. **Open the terminal inside VS Code:** menu **View → Terminal**. A panel opens at the bottom. Everything you type in this guide goes there.
6. **Type these two lines first, every time you open a new terminal:**
   ```bash
   export UV_OFFLINE=1
   uv run flight/preflight_check.py
   ```
   `export UV_OFFLINE=1` tells uv not to try the internet. It's forgotten whenever the terminal closes, which is why you type it every time. The check should say READY.
7. **Create your log:**
   ```bash
   cp flight/flight-log-template.md flight-log.md
   ```
   `cp` makes a copy. Your log is now `flight-log.md`, in the ai-builds folder.
8. **Open the plan side by side.** In VS Code's file list on the left, click `flight/README.md`, then press **Cmd+K**, let go, and press **V**. The formatted plan opens on the right. Keep it open all flight.

Your screen now has three parts: files on the left, your code in the middle, the plan on the right, and the terminal along the bottom.

---

## Part 2: Which document to open for each block

All reading is in `~/offline-docs`. To open it, type `open ~/offline-docs` in the terminal and a Finder window appears.

| Block | Read first (30 min max) | File you create | When you think it's done |
|---|---|---|---|
| 1 | Nothing new | `hello.py` (rewrite it) | `uv run hello.py` |
| 2 | Automate the Boring Stuff ch 4 (Functions) and ch 7 (Dictionaries) | `drills.py` | `uv run flight/check.py 2` |
| 3 | Ch 18, CSV section only (stop at JSON). Python docs: Library Reference → csv | `pricing.py` | `uv run flight/check.py 3` |
| Break | Nothing | `data/enquiries.txt` | Count your 10 lines |
| 4 | Ch 18, JSON section. Python docs: Tutorial → Errors and Exceptions, sections 8.1–8.4 | `enquiry.py` | `uv run flight/check.py 4` |
| 5 | Ollama structured outputs PDF (the Python + Pydantic example). Ollama thinking PDF (just `think=False`) | `intake.py` | `uv run flight/check.py 5` |
| 6 | `flight/HINTS.md`, Block 6 | Add to `intake.py`, plus `batch.py` | `uv run flight/check.py 6` |
| 7 | `flight/HINTS.md`, Block 7 | `orchestrator.py` | `uv run flight/check.py 7` |

**Finding things in the Python docs:** open the Python docs folder in `~/offline-docs`, then double-click `index.html`. The search box should work offline: type `csv` or `exceptions`. If it doesn't, click through instead: **Library Reference → File Formats → csv**, or **Tutorial → Errors and Exceptions**.

**Reading tip:** don't read a chapter cover to cover. Read until you've seen the thing the block asks for (for example, `DictReader`), try it, and come back to the chapter when you're stuck.

---

## Part 3: The loop for every block

Every block follows the same 10 steps. Once you know the loop, the plan in `README.md` tells you everything else.

1. **Log the start time** in `flight-log.md`.
2. **Read the block** in the plan (right side of the screen): what to build and "Done when".
3. **Read the documents** for that block (table above). Set a 30-minute timer; reading isn't building.
4. **Create the file.** In VS Code: **File → New File**, then **File → Save As**. Name it exactly as the plan says (for example, `drills.py`) and save it in the `ai-builds` folder, next to `hello.py`. Check the spelling; `check.py` looks for that exact name.
5. **Write a little, then run it.** After every 3–5 lines, save (Cmd+S) and run it in the terminal with `uv run drills.py`. Small steps mean that when something breaks, you know which lines did it.
6. **Check it:** `uv run flight/check.py 2` (use the block's number).
7. **A FAIL line?** Read the line under it that starts with `->`; it says what's wrong. Fix it, save, check again. Still stuck after two honest tries? Go to Part 5.
8. **All PASS?** Now **explain every line out loud** (a whisper is fine), or write a short comment above each line in your own words. If there's a line you can't explain, the block isn't done. Write it under "Lines I couldn't explain" in your log and study it.
9. **Save your work in git** (Part 4 explains this):
   ```bash
   git add .
   git commit -m "Block 2: drills"
   ```
10. **Log the end time** and mark the block DONE, ASSISTED or SKIPPED.

Then take a 5-minute break: stand up, drink water. Then start the next block.

---

## Part 4: What `git add` and `git commit` do

Think of git as a camera for your project folder.

- `git add .` puts every file you've changed into the frame. The `.` means "everything in this folder".
- `git commit -m "message"` takes the photo and labels it with your message. The photo is saved on your Mac, and this works offline.
- `git push` uploads your photos to GitHub. That needs internet, so it waits until you land.

If you ever break something badly, you can go back to your last photo. That's why you commit after every block.

**If `git commit` says "Please tell me who you are"**, run these two lines once, then commit again:
```bash
git config --global user.name "Tijo"
git config --global user.email "tijo22@gmail.com"
```

---

## Part 5: When you're stuck

Go through these in order. Don't skip ahead to the answers.

1. **Read the last line of the error.** It names the problem. The line above it, with a line number, shows where.
2. **Open `flight/HINTS.md`** and look at the common-errors table at the top.
3. **Use the hints for your block in `HINTS.md`, one at a time.** Hint 1 → try again → Hint 2 → try again → Hint 3.
4. **Ask the local tutor.** Open a second terminal with the **+** button at the top right of the terminal panel, then run `ollama run qwen3:8b`. Paste the tutor prompt from `HINTS.md`, then your error. Type `/bye` to leave. It can be confidently wrong, so if it disagrees with `HINTS.md` or `check.py`, trust those.
5. **The sealed answer, last.** Read `flight/answers/README.md` first. Read the answer, close it, type your own version from a blank file, and mark the block **ASSISTED** in your log.

**If something seems frozen:** the program may be waiting for you to type (`input()`), or the model may be loading, which takes up to a minute on the first call. To force-stop a program, press **Ctrl+C**.

---

## Part 6: Block 1, step by step

Block 1 closes the gate from Sept 28: write `hello.py` from memory.

1. Log the start time.
2. Click `hello.py` on the left. Press **Cmd+A** (select all), then **Delete**, then **Cmd+S**. It's now blank. That feels uncomfortable, and that's the point.
3. Without looking at anything, write the version that:
   - reads the model name from `.env` (instead of typing `qwen3:14b` into the code)
   - asks you to type a question
   - sends it to the model with `think=False`
   - prints only the answer text
4. Stuck? `HINTS.md`, Block 1, has three hints. Use them in order.
5. Run it:
   ```bash
   uv run hello.py
   ```
   Type a question and press Enter. The first answer takes 10–60 seconds while the model loads. After that it's faster.
6. **Prove `.env` is in control.** Open `.env` (on the left; if you don't see it, use File → Open and type `.env`). Change `qwen3:8b` to `qwen3:4b` and save. Run `uv run hello.py` again. In the second terminal, `ollama ps` shows which model is loaded right now: it should say `qwen3:4b`. Then change `.env` back to `qwen3:8b`.
7. Explain every line out loud.
8. Commit:
   ```bash
   git add .
   git commit -m "Block 1: hello.py rewritten from blank"
   ```
9. Log the end time, mark it DONE, and move on to Block 2 using the loop in Part 3.

---

## Part 7: Battery and breaks

- **Plugged in:** keep `qwen3:8b`.
- **On battery and under 40%:** change `.env` to `OLLAMA_MODEL=qwen3:4b`. No code changes needed.
- **Under 15%:** stop using the model. The break block (writing enquiries) and the reading need no AI, so do those.
- **Before you sleep or eat:** finish or commit the current step first, so you know exactly where you left off.

## Part 8: Before landing (15 min)

```bash
git add .
git commit -m "Flight sprint: blocks 1-N"
git status
```

`git status` should say "nothing to commit". Finish your log: statuses, the lines you couldn't explain, and your top 3 confusions. After landing: `git push`, then bring `flight-log.md` to Claude.
