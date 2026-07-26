# Python Logging — Complete Guide

> **Source:** answered by Claude Sonnet 5 (thinking) via Perplexity, 2026-07-25.
> Kept verbatim. This is the "read once and understand it" intro; the numbered files
> `00`–`09` in this folder are the reference you come back to.
> Three small corrections are appended at the very bottom — read them before typing
> the `extra={}` and `RotatingFileHandler` examples.

---

Logging is the standard way to track what a program does while it runs — recording events, errors, and state changes so you can debug issues or monitor behavior in production, instead of relying on `print()`.  [docs.python](https://docs.python.org/3/howto/logging.html)

## Why not just use `print()`?

`print()` has no levels, no timestamps, no filtering, and no way to redirect output to files/systems without manually rewriting code. Logging solves all of this and is the standard tool once your code moves beyond quick scripts — which is directly relevant to the production pipelines you build.  [realpython](https://realpython.com/python-logging/)

## Basic usage

```python
import logging

logging.debug("A debug message")
logging.info("An info message")
logging.warning("A warning message")
logging.error("An error message")
logging.critical("A critical message")
```

By default, only `WARNING` and above get shown — `debug()` and `info()` are silent unless you configure the logger.  [docs.python](https://docs.python.org/3/howto/logging.html)

## The 5 log levels (in order of severity)

| Level | Numeric value | When to use |
|---|---|---|
| `DEBUG` | 10 | Detailed diagnostic info, useful only during development |
| `INFO` | 20 | Confirmation that things are working as expected |
| `WARNING` | 30 | Something unexpected happened, but the program still works |
| `ERROR` | 40 | A serious problem — some functionality failed |
| `CRITICAL` | 50 | A severe error — the program itself may be unable to continue |

 [docs.python](https://docs.python.org/3/howto/logging.html)

## Basic configuration — `basicConfig()`

```python
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Application started")
logging.error("Something went wrong")
```

This writes logs to `app.log` instead of the console, and sets the minimum level to `INFO` (so `DEBUG` messages get ignored).  [docs.python](https://docs.python.org/uk/3.13/library/logging.html)

Example output in `app.log`:
```
2026-07-25 21:37:12,102 - INFO - Application started
2026-07-25 21:37:14,556 - ERROR - Something went wrong
```

## The proper way — using a named logger (recommended over the root logger)

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler("app.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

logger.info("Started")
logger.warning("Low disk space")
```

Using `logging.getLogger(__name__)` (instead of calling `logging.info()` directly) is the recommended pattern in real projects, because `__name__` automatically labels logs with the module they came from — very useful when you have multiple files/agents logging simultaneously.  [medium](https://medium.com/@jugalsolanki1072/logging-with-python-a-deep-dive-096e03efa248)

## Core building blocks

| Component | Purpose |
|---|---|
| **Logger** | The object you call `.info()`, `.error()`, etc. on |
| **Handler** | Decides *where* logs go — console, file, network, email |
| **Formatter** | Decides *how* the log message looks (timestamp, level, message) |
| **Filter** | Optional — lets you selectively allow/block certain log records |

 [docs.python](https://docs.python.org/3/howto/logging.html)

## Logging to both console and file at the same time

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)   # only warnings+ to console

file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)         # everything to file

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.debug("Debug detail")     # only in file
logger.warning("Careful!")       # in both console and file
```

This pattern — verbose logs to a file, only important stuff to console — is extremely common in real production systems.  [youtube](https://www.youtube.com/watch?v=9L77QExPmI0)

## Adding extra context (very useful for multi-agent/pipeline systems)

```python
logger.info("Processing document", extra={"doc_id": "123", "agent": "ocr_agent"})
```

The `extra` parameter lets you attach structured metadata to a log entry, which is essential when tracing what happened across multiple agents or pipeline stages.  [youtube](https://www.youtube.com/watch?v=9L77QExPmI0)

## Exception logging — capturing full tracebacks

```python
try:
    1 / 0
except ZeroDivisionError:
    logger.error("Division failed", exc_info=True)
```

`exc_info=True` automatically attaches the full traceback to the log entry — extremely useful for debugging production failures without needing `print(traceback.format_exc())` manually.  [docs.python](https://docs.python.org/3/howto/logging-cookbook.html)

## Modern best practices (2025–2026 standard)

- **Use structured logging (JSON)** instead of plain text strings — makes logs machine-parsable and queryable, standard in modern observability setups.  [dash0](https://www.dash0.com/guides/logging-best-practices)
- **Log at the right level** — don't flood `INFO` with things that should be `DEBUG`; don't hide real problems in `WARNING` when they should be `ERROR`.  [dataset](https://www.dataset.com/blog/the-10-commandments-of-logging/)
- **Add context to every message** — a log without context (like a request ID, doc ID, or agent name) is often useless when debugging distributed/multi-agent systems.  [dataset](https://www.dataset.com/blog/the-10-commandments-of-logging/)
- **Always include timestamps** — critical for correlating events across a pipeline.  [newrelic](https://newrelic.com/blog/log/best-log-management-practices)
- **Avoid logging sensitive data** (API keys, PII) directly into log files.  [last9](https://last9.io/blog/logging-best-practices/)
- **Use log rotation** for long-running services, so log files don't grow unbounded:

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler("app.log", maxBytes=5_000_000, backupCount=3)
```

This automatically rotates to a new file once `app.log` hits 5MB, keeping up to 3 backups.  [docs.python](https://docs.python.org/3/howto/logging-cookbook.html)

## Quick comparison: `print()` vs `logging`

| Feature | `print()` | `logging` |
|---|---|---|
| Severity levels | No | Yes (DEBUG → CRITICAL) |
| Redirect to file | Manual | Built-in (`FileHandler`) |
| Timestamps | Manual | Automatic (via formatter) |
| Filter by importance | No | Yes (`setLevel`) |
| Structured/JSON output | Manual | Supported via custom formatters |
| Production-ready | No | Yes |

## Why this matters for your work specifically

Given you're building multi-agent orchestration and document processing pipelines, structured logging with context (`extra={}`), proper log levels, and file rotation is exactly what separates a toy script from a production-grade system — it's how you'd trace which agent failed, on which document, at what time, without digging through raw print statements.  [last9](https://last9.io/blog/logging-best-practices/)

---
---

# Addendum — three corrections before you type these

*Not part of the original answer. Added because these three bite on this machine.*

### 1. The `extra={}` example prints nothing

```python
logger.info("Processing document", extra={"doc_id": "123", "agent": "ocr_agent"})
```

With the formatter used earlier in this guide (`"%(asctime)s - %(levelname)s - %(message)s"`)
the output is just:

```
2026-07-25 21:37:12,102 - INFO - Processing document
```

`doc_id` and `agent` are attached to the `LogRecord`, but **no formatter references them, so
they never appear.** `extra` puts data *on the record*; it does not put data *in the output*.

Two ways to actually see them:

```python
# A) name them in the format string — but then EVERY record must have them,
#    or you get: ValueError: Formatting field not found in record
logging.Formatter(
    "%(asctime)s - %(levelname)s - [%(doc_id)s/%(agent)s] %(message)s",
    defaults={"doc_id": "-", "agent": "-"},      # Python 3.10+, supplies fallbacks
)

# B) use a formatter that sweeps everything off the record — this is what makes
#    the guide's "use structured logging (JSON)" bullet actually work
```

Option B is `examples/ex07_json_logs.py` in this folder. Run it.

### 2. Don't `addHandler` inside a module

Both named-logger examples above do `getLogger(__name__)` **and** `addHandler(...)` in the
same file. If anything else configures the root logger — `basicConfig`, a framework, pytest,
uvicorn — every line prints **twice**, because the record fires the module's handler and then
propagates up to root's.

The rule real projects follow:

```python
# every module — ONLY this:
logger = logging.getLogger(__name__)

# the application entry point — ALL handler/level setup, once:
logging.config.dictConfig(LOGGING)
```

`examples/ex02_hierarchy.py` demonstrates the duplicate and all three fixes.

### 3. `RotatingFileHandler` needs `encoding="utf-8"` on Windows

```python
handler = RotatingFileHandler("app.log", maxBytes=5_000_000, backupCount=3)   # crashes
handler = RotatingFileHandler("app.log", maxBytes=5_000_000, backupCount=3,
                              encoding="utf-8")                               # correct
```

Without it, Python uses the Windows ANSI code page (cp1252). The first `—`, `→`, `é`, or emoji
in a log message raises `UnicodeEncodeError: 'charmap' codec can't encode character` — mid-request,
in production. Also note `FileHandler` will **not** create the log directory; `mkdir` it first.

### One thing the guide doesn't cover

Its "modern best practices" list omits the rule that outranks most of the others for deployed
code: **in a container, write JSON to stdout and stop.** No file handler, no rotation, no log
shipping in-process — Docker/k8s/ECS collect stdout for you. That's what uvicorn and Django's
defaults do. See `02_open_source_survey.md`.

File-based logging (and therefore rotation) is still correct for CLIs, desktop apps, and VM
daemons — just not for services in containers.
