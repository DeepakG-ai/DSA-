# 40 Industry Scenarios — Tickets, Incidents & Code Reviews

No textbook questions. Every item below is written the way work actually arrives:
a ticket, a production incident, a code review, or a vague requirement from a manager.

**Rules:** Open your editor. Solve for real. Run the code. No AI on first attempt.
For incidents: state ROOT CAUSE first, then the FIX, then how you'd PREVENT it.

---

## SECTION A — PRODUCTION INCIDENTS (debug like it's 2 AM)

### INC-001 · "Script worked for 3 months, crashed last night"
The nightly report script died. Here's the traceback from the server:
```
Traceback (most recent call last):
  File "/opt/jobs/daily_report.py", line 88, in <module>
    total = sum(row["amount"] for row in rows)
  File "/opt/jobs/daily_report.py", line 88, in <genexpr>
    total = sum(row["amount"] for row in rows)
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```
The input is a CSV exported by the finance team.
1. What most likely changed in the CSV last night?
2. Write the defensive version of line 88 that logs bad rows and continues.
3. Should bad rows be skipped silently, skipped with a warning, or crash the job? Justify for a finance report.

### INC-002 · "The API bill is 10x this month"
Your teammate deployed this LLM wrapper:
```python
def get_embedding(text):
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding

def find_similar(query, documents):
    query_emb = get_embedding(query)
    scores = []
    for doc in documents:
        doc_emb = get_embedding(doc)
        scores.append(cosine_similarity(query_emb, doc_emb))
    return scores
```
`find_similar` is called on every user request. `documents` is the same 5,000 docs each time.
1. Why is the bill 10x?
2. Fix it two ways: (a) in-memory dict cache, (b) disk cache that survives restarts.
3. What's the cache KEY, and why does using the raw text as key eventually cause a problem? (Hint: hashing.)

### INC-003 · "Log file ate the disk"
Server down. Investigation: `app.log` is 92 GB. The code:
```python
logging.basicConfig(filename="app.log", level=logging.DEBUG)
```
The app logs every request payload at DEBUG in a busy service.
1. Two separate mistakes here — name both (level AND rotation).
2. Write the corrected setup: INFO to a rotating file (50 MB × 5 backups), DEBUG only when env var `LOG_DEBUG=1` is set.
3. Ops asks: "can we get errors in a separate file too?" Add a second handler that writes ERROR+ to `errors.log`.

### INC-004 · "Duplicate rows in the database every time we retry"
The ingestion job retries on failure. After a network blip, customers appear 2–3 times in the DB:
```python
for customer in customers:
    try:
        db.insert(customer)
    except NetworkError:
        time.sleep(5)
        db.insert(customer)   # retry
```
1. The retry isn't the real problem. What property is this pipeline missing? (The word starts with 'i'.)
2. Redesign the loop so re-running the ENTIRE job from scratch is always safe.
3. Where else in your company's pipelines would this same bug class appear? (Think: LLM batch jobs that crash midway.)

### INC-005 · "Works on my machine, breaks on the server"
```python
with open("data/config.json") as f:
    config = json.load(f)
```
Runs fine locally. On the server: `FileNotFoundError: data/config.json` — but the file EXISTS on the server.
1. What's the actual cause? (Hint: what directory is the script run FROM via cron?)
2. Fix it with `pathlib` so the path is relative to the script file, not the working directory.
3. Bonus: the server also crashed with `UnicodeDecodeError` on another file. What argument was missing from `open()`?

### INC-006 · "The 'fast' version returns wrong results"
A teammate parallelized a scraper:
```python
results = []

def fetch_and_store(url):
    data = requests.get(url).json()
    results.append(data["items"][0])

with ThreadPoolExecutor(max_workers=20) as ex:
    for url in urls:
        ex.submit(fetch_and_store, url)

print(len(results), len(urls))   # sometimes not equal!
```
1. Two bugs: one swallows exceptions invisibly, one is a design smell (shared mutable state). Explain both.
2. Rewrite using `ex.map` or futures with `.result()` so exceptions surface and results are collected safely.
3. When DO you need a `threading.Lock` in Python, given the GIL exists?

### INC-007 · "Numbers are slightly off in the invoice"
```python
total = 0.0
for item in cart:
    total += item.price * item.qty
if total == 149.90:
    apply_free_shipping()
```
Free shipping randomly doesn't apply for carts that clearly total ₹149.90.
1. Root cause?
2. Fix using the `decimal` module — why is `Decimal("149.90")` correct but `Decimal(149.90)` still wrong?
3. Company policy question: should money EVER be a float in your codebase?

### INC-008 · "Timezone bug — reports show yesterday's date"
A daily report at 1 AM IST shows the wrong date for some users:
```python
from datetime import datetime
today = datetime.now().strftime("%Y-%m-%d")
```
The server is in UTC. Users are in IST.
1. Explain exactly why 1 AM IST produces yesterday's date on a UTC server.
2. Fix using `zoneinfo.ZoneInfo("Asia/Kolkata")`.
3. Team rule to prevent this class of bug forever: store in ___, display in ___.

---

## SECTION B — CODE REVIEW (AI wrote it, you must catch the problems)

You said Claude/GPT code "sometimes is overcomplex." Here you play reviewer. Each snippet was AI-generated and "works." Find what a senior would flag.

### CR-101 · Review this AI-generated config loader
```python
import json, os

def load_config():
    try:
        with open("config.json", "r") as file:
            config_data = json.load(file)
            if config_data is not None:
                if isinstance(config_data, dict):
                    if "api_key" in config_data:
                        if config_data["api_key"] != "":
                            return config_data
                        else:
                            return None
                    else:
                        return None
                else:
                    return None
            else:
                return None
    except:
        return None
```
1. List at least 4 problems (nesting, bare except, returning None for 5 different reasons, silent failure of a REQUIRED config...).
2. Rewrite in ≤10 lines: fail LOUDLY with distinct, clear error messages. Why is crashing at startup BETTER than returning None here?

### CR-102 · Review this "helper"
```python
def process_data(data=None, options={}, callbacks=[]):
    options["processed"] = True
    if data:
        callbacks.append(len(data))
    return data, options, callbacks
```
Three parameter-level bugs and one truthiness bug (`if data:` — what happens when data is `0` or `""` or an empty DataFrame?). Find all four. Rewrite correctly.

### CR-103 · Review this retry logic
```python
def call_llm(prompt):
    for i in range(5):
        try:
            return client.chat(prompt)
        except Exception:
            time.sleep(1)
    return None
```
1. Five problems minimum: catching ALL exceptions (should a `KeyboardInterrupt` or auth error be retried?), fixed sleep (thundering herd — what's exponential backoff?), silent `return None`, no logging, no final raise.
2. Rewrite properly: retry ONLY on rate-limit/timeout errors, exponential backoff with jitter, log each attempt, raise after exhaustion.

### CR-104 · Review this file processor
```python
def merge_files(folder):
    all_data = ""
    for f in os.listdir(folder):
        file = open(folder + "/" + f)
        all_data = all_data + file.read()
    return all_data
```
Problems: files never closed, string concatenation in a loop (why is this O(n²)?), path joining by hand, no filtering (what if there's a `.DS_Store` or subfolder?), whole thing in memory. Rewrite with pathlib + generator.

### CR-105 · The overcomplex one — simplify it
AI produced this. Your manager asks "can this be simpler?"
```python
def get_active_emails(users):
    result = []
    for i in range(0, len(users)):
        user = users[i]
        if user.get("active") == True:
            email = user.get("email")
            if email is not None:
                if len(email) > 0:
                    result.append(email.lower())
    return result
```
Rewrite as 1–2 lines that a senior would approve. Every simplification must preserve behavior — including the None/empty checks.

### CR-106 · Security review
```python
import subprocess

def convert_file(filename):
    subprocess.run(f"ffmpeg -i {filename} output.mp4", shell=True)
```
`filename` comes from a user upload form.
1. What can a malicious user do with a filename like `video.mp4; rm -rf /`?
2. What's this vulnerability called? Fix it (list-form args, `shell=False`).
3. Same class of bug with SQL: why is `f"SELECT * FROM users WHERE name = '{name}'"` dangerous, and what's the fix called?

### CR-107 · The leaked secret
A teammate's PR contains:
```python
OPENAI_API_KEY = "sk-proj-Xk29..."
client = OpenAI(api_key=OPENAI_API_KEY)
```
It's already pushed to the company GitHub.
1. What are the immediate remediation steps, in order? (Rotating the key is #1 — why is deleting the commit NOT enough?)
2. Write the corrected pattern: `.env` file + `python-dotenv` + `.gitignore`. What exactly goes in `.gitignore`?
3. Write the startup check that fails fast with a clear message if the key is missing.

---

## SECTION C — TICKETS (build it from a vague requirement)

Written exactly like your Teams meetings: underspecified. Part of the task is asking the right questions BEFORE coding.

### TKT-201 · "We need the Excel the client sends every week loaded into our system"
The file: first 3 rows are a logo/title, headers on row 4, a "TOTAL" row at the bottom that must be excluded, amount column sometimes has "₹1,200.00" as text, dates in DD-MM-YYYY.
1. Write 3 clarifying questions you'd ask before coding.
2. Build the loader (pandas allowed): skip junk rows, drop the TOTAL row, clean currency strings to float, parse dates correctly.
3. The client WILL eventually send a malformed file. Design the failure mode: what gets logged, what gets emailed, does the pipeline halt?

### TKT-202 · "Users say the app is slow, find out why"
You inherit a 500-line script with zero logging. You can't read it all.
1. Write a `@timeit` decorator you can slap onto any suspect function that logs `function_name took 3.42s` — to a logger, not print.
2. How do you profile the whole script in one command without editing it? (`python -m cProfile -s cumulative script.py`)
3. The profile shows 80% of time in `requests.get` called 400 times. Three different fixes, ranked by effort: (session reuse? caching? concurrency?)

### TKT-203 · "Make the chatbot remember the conversation"
Current code sends only the latest message to the LLM. Requirements from the meeting: "it should remember, but don't blow up the context window, and don't lose the system prompt."
1. Design a `ConversationMemory` class: `add(role, content)`, `get_messages()` that always keeps the system prompt, keeps the last N turns, and truncates oldest-first when a token estimate exceeds a budget.
2. Rough token estimation without an API call: what's the ~chars-per-token heuristic?
3. When the history is truncated, what information is silently lost, and what's one strategy real products use? (summarize-and-compress)

### TKT-204 · "The vector search returns garbage for long documents"
Docs are embedded as ONE embedding per document. Some docs are 40 pages.
1. Why does one embedding for 40 pages give bad retrieval?
2. Write a `chunk_text(text, chunk_size=500, overlap=50)` function — character-based is fine. Why does overlap exist?
3. A chunk boundary splits a sentence mid-way. Improve the function to break on sentence boundaries when possible.

### TKT-205 · "Boss wants a daily summary email of yesterday's errors"
Log lines look like: `2026-07-06 14:23:11 ERROR [payment] card declined for order 8812`
1. Write the parser: extract timestamp, level, module, message from each line — using `str.split` with maxsplit OR a regex, your choice. Handle lines that don't match the format.
2. Filter to YESTERDAY's ERRORs only (date math — careful with midnight).
3. Produce the summary: count per module, top 5 most frequent messages, total. Format as a clean text block ready for email.

### TKT-206 · "Process these 10k PDFs through the LLM, it keeps crashing at 7k"
The job takes 6 hours and crashes around document 7,000. Rerunning from zero wastes money.
1. Design checkpointing: after each batch, persist which doc IDs are done (JSON file or SQLite — argue your pick).
2. On startup, skip already-done docs. Why must writing the checkpoint be atomic (write-to-temp-then-rename), and what corruption happens if the crash hits mid-write?
3. Add a `--resume` vs `--fresh` argparse flag.

### TKT-207 · "Sync the two systems"
Every hour, pull items from API-A and push new ones to API-B. Both APIs paginate.
1. Write `fetch_all(url)` handling cursor pagination: response is `{"items": [...], "next_cursor": "abc"}` — loop until cursor is null. What's the infinite-loop risk and your guard?
2. "New ones" needs state. Where do you store the last-seen ID/timestamp between hourly runs?
3. API-B rejects with 429. Handle: respect the `Retry-After` header if present, else exponential backoff.

### TKT-208 · "Wrap the model in an API"
Expose your teammate's `predict(text) -> dict` function as an HTTP endpoint.
1. Write it in FastAPI: POST `/predict`, pydantic request model (`text: str`, non-empty), pydantic response model.
2. `predict()` sometimes throws. Return a proper 500 with a clean error body — WITHOUT leaking the stack trace to the caller. Where does the full trace go instead?
3. Add `/health` endpoint. Why does every deployed service need one?

---

## SECTION D — SYSTEM TASKS (the pieces of every AI pipeline)

### SYS-301 · Structured logging for a multi-module app
Your app: `main.py`, `ingest.py`, `llm.py`, `db.py`. Requirements: one setup function called ONCE in main; every module uses `logging.getLogger(__name__)`; console INFO, rotating file DEBUG (20 MB × 5); ERRORs additionally to `errors.log`; format includes module name and line; libraries you import (urllib3 etc.) capped at WARNING so they don't spam. Write the complete `logging_setup.py`.

### SYS-302 · The token-bucket rate limiter
Build `RateLimiter(rate=50, per=60)` with a `wait()` method that BLOCKS just long enough to keep you under 50 calls/min (not a boolean check — actually sleeps the right amount). Then make it a context manager so usage is `with limiter: call_api()`.

### SYS-303 · Config with layers
`Config` class: defaults dict → overridden by `config.json` if present → overridden by env vars prefixed `APP_`. So `APP_MODEL=claude-opus` beats the JSON. Type coercion: env vars are always strings — `APP_TIMEOUT=30` must come out as int if the default was int. Write it + 3 quick tests.

### SYS-304 · Graceful shutdown
Your batch job runs for hours. When ops sends SIGTERM (or you hit Ctrl+C), it must: finish the CURRENT item, write the checkpoint, log "shutdown clean", exit 0. Use the `signal` module + a `should_stop` flag checked in the loop. Why is `sys.exit()` inside a signal handler mid-write dangerous?

### SYS-305 · The full pipeline (capstone)
Combine everything: 10,000 texts → chunk (TKT-204) → embed via API in batches of 20 → rate-limited (SYS-302) → retried with backoff (CR-103's fix) → checkpointed (TKT-206) → structured logs (SYS-301) → config from env (SYS-303) → graceful shutdown (SYS-304). Write the real thing. When this runs end-to-end, crashes on purpose (kill it at 40%), and RESUMES correctly — you are industry-level. That's the actual bar.

---

## How to work these

- **Incidents (A):** root cause → fix → prevention. Write all three, like a real postmortem.
- **Reviews (B):** write the review comments AS IF commenting on a PR, then the corrected code.
- **Tickets (C):** write your clarifying questions FIRST. Coding a vague ticket without questions is how projects fail — including at your company.
- **1 scenario per day.** These are heavier than they look.
- SYS-305 is the graduation exam. Everything before it is training for it.
