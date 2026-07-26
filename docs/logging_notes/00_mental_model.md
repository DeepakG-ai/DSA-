# 00 — The mental model

You said you know the concepts but not the code. This file is the bridge. Every confusing
thing about stdlib `logging` comes from not holding these **five objects** in your head at once.

---

## The pipeline

```
   your code
      |
      |  logger.info("hello", extra={...})
      v
 +----------+     level check #1: logger.isEnabledFor(INFO)?
 |  Logger  |---- NO --> dropped, nothing else runs
 +----------+
      |  YES -> builds a LogRecord
      v
 +----------+
 | LogRecord|  a plain object: .msg .args .levelno .name .created .thread .exc_info ...
 +----------+
      |
      v
 +----------+     Filters attached to the LOGGER
 |  Filter  |---- returns False --> dropped
 +----------+
      |
      |  then walk UP the logger tree (propagation)
      v
 for each logger in [self, parent, grandparent, ..., root]:
     for each handler on that logger:
 +----------+     level check #2: record.levelno >= handler.level?
 | Handler  |---- NO --> this handler skips it (others still run)
 +----------+
      |  Filters attached to the HANDLER --- False --> this handler skips it
      v
 +-----------+
 | Formatter |  turns the LogRecord into a string
 +-----------+
      |
      v
   the sink: stdout / file / socket / syslog / HTTP / queue
```

**Two level checks, not one.** This is the #1 source of "why is nothing logging".
`logger.setLevel(DEBUG)` alone does nothing if the handler is still at `WARNING`.

---

## The five objects

### 1. `Logger` — *what happened and who says so*

```python
import logging
logger = logging.getLogger(__name__)   # ALWAYS this. Never logging.getLogger() with no name in a module.
logger.info("user logged in")
```

- `getLogger(name)` is a **registry lookup**, not a constructor. Same name → same object, every time,
  from anywhere in the process. This is a global singleton dict keyed by string.
- The name creates a **tree** by dots: `"backend.worker.ocr"` has parent `"backend.worker"`,
  grandparent `"backend"`, then the **root** logger `""`.
- `__name__` gives you `backend.worker.ocr` for free, matching your package layout. That is
  why everyone writes `getLogger(__name__)`.

### 2. `LogRecord` — *the event as data*

Never construct one yourself. Know its attributes, because formatters reference them by name:

| Attribute | Value |
|-----------|-------|
| `%(name)s` | logger name (`backend.worker`) |
| `%(levelname)s` | `DEBUG` / `INFO` / `WARNING` / `ERROR` / `CRITICAL` |
| `%(levelno)s` | 10 / 20 / 30 / 40 / 50 |
| `%(message)s` | `record.getMessage()` → `msg % args` |
| `%(asctime)s` | formatted time (needs `datefmt`, else ISO-ish with comma-millis) |
| `%(msecs)d` | milliseconds part |
| `%(created)f` | `time.time()` at creation |
| `%(pathname)s` `%(filename)s` `%(module)s` | source file |
| `%(funcName)s` `%(lineno)d` | source function / line |
| `%(process)d` `%(processName)s` | PID |
| `%(thread)d` `%(threadName)s` | thread |
| `%(taskName)s` | asyncio task name (**Python 3.12+**) |
| `%(exc_info)s` `%(exc_text)s` `%(stack_info)s` | traceback data |

Anything you pass in `extra={...}` becomes an attribute too — that is how custom fields work:

```python
logger.info("charged card", extra={"user_id": 42, "amount": 9.99})
# formatter can now use %(user_id)s and %(amount)s
```

⚠️ `extra` keys that collide with built-ins (`message`, `asctime`, `name`, `args`, `levelname`, …)
raise `KeyError: "Attempt to overwrite 'message' in LogRecord"`.

### 3. `Handler` — *where it goes*

One logger, many handlers. Each handler is one destination with its **own** level, formatter,
and filters. This is the whole point of the design:

```python
console = logging.StreamHandler()                    # everything to the terminal
console.setLevel(logging.INFO)

errors  = logging.FileHandler("error.log")           # only failures to disk
errors.setLevel(logging.ERROR)

logger.addHandler(console)
logger.addHandler(errors)
```

Full catalogue with scenarios: **`04_handlers_scenarios.md`**.

### 4. `Formatter` — *what it looks like*

```python
fmt = logging.Formatter(
    "%(asctime)s %(levelname)-8s %(name)s:%(lineno)d — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
handler.setFormatter(fmt)
```

- `%(levelname)-8s` left-pads to 8 chars → columns line up. Your OCR code uses `%(levelname)-5s`.
- Default `style="%"`. You can pass `style="{"` for `{asctime} {message}` or `style="$"`.
- Subclass `Formatter` and override `format(self, record)` for anything custom — JSON, colours,
  suppressing tracebacks. Your OCR code has two subclasses doing exactly that.

### 5. `Filter` — *should this record continue, and can I add to it?*

A filter is any object with `.filter(record) -> bool`. Returning `False` drops the record.

But the real power is that **a filter can mutate the record**, which makes it the
official injection point for context:

```python
class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = current_request_id.get() or "-"
        return True     # always keep the record; we only came to stamp it
```

Now `%(request_id)s` works in every formatter.

Django ships two filters in `django/utils/log.py` that use the *drop* behaviour instead —
`RequireDebugTrue` and `RequireDebugFalse` — so the console handler is live only in DEBUG
and the email-the-admins handler only in production. Same mechanism, opposite purpose.

---

## Propagation — the thing that causes duplicate lines

After a logger's own handlers run, the record goes to the **parent** logger's handlers too,
and up to root. Parent **levels are not re-checked** — only parent *handler* levels are.

```python
logging.basicConfig(level=logging.INFO)        # adds a handler to ROOT
log = logging.getLogger("app")
log.addHandler(logging.StreamHandler())        # adds a handler to "app"
log.info("hi")
# hi          <- from app's handler
# INFO:app:hi <- from root's handler (propagation)
```

Two lines. Three fixes, pick one:

```python
log.propagate = False                    # 1. stop the walk at this logger
# or: don't call basicConfig — configure only root, let everything propagate
# or: configure only root and never addHandler on child loggers   <- usually correct
```

**Best practice:** libraries and modules only ever call `getLogger(__name__)` and log.
**Only the application entry point** attaches handlers, and it attaches them to root.

Real example — uvicorn's `LOGGING_CONFIG` sets `propagate: False` on the two loggers it
owns, so its own pretty-printed access lines never get re-emitted by whatever the host
application configured on root:

```python
"loggers": {
    "uvicorn":        {"handlers": ["default"], "level": "INFO", "propagate": False},
    "uvicorn.error":  {"level": "INFO"},
    "uvicorn.access": {"handlers": ["access"],  "level": "INFO", "propagate": False},
},
```

Django does the same for `django.server`. See `02_open_source_survey.md`.

---

## Levels

| Level | Value | Use it for |
|-------|-------|-----------|
| `CRITICAL` | 50 | the process is about to die / data is being lost |
| `ERROR` | 40 | this operation failed; a human must look |
| `WARNING` | 30 | recovered, degraded, or deprecated — **the default root level** |
| `INFO` | 20 | normal lifecycle: started, finished, 200 OK, job N complete |
| `DEBUG` | 10 | values, branches, payloads — off in production |
| `NOTSET` | 0 | on a logger: inherit parent's effective level. On a handler: process everything. |

```python
logging.getLogger().getEffectiveLevel()   # walks up until it finds a non-NOTSET level
logger.isEnabledFor(logging.DEBUG)        # guard for genuinely expensive message building
```

Custom levels exist (`logging.addLevelName(25, "NOTICE")`) but almost never earn their keep.
loguru gives you `logger.level("NOTICE", no=25)` more cleanly if you really want them.

---

## Two syntax rules you will get wrong at first

**1. Use `%`-style lazy args, never f-strings, in the log call.**

```python
logger.info("processed %d pages for %s", n, filename)   # GOOD
logger.info(f"processed {n} pages for {filename}")      # works, but always pays the cost
```

With `%` args the string is only built if some handler actually accepts the record.
On a `DEBUG` line in production that is a free win. It also keeps the raw `msg` intact so
log-aggregation tools can group identical events.

**2. Inside `except:`, use `logger.exception()`.**

```python
try:
    risky()
except Exception:
    logger.exception("risky() failed")      # ERROR + full traceback, automatically
```

`logger.exception()` == `logger.error(..., exc_info=True)`. It only works inside an
`except` block. Outside one, pass the exception explicitly:
`logger.error("failed", exc_info=exc)`.

---

Next: **`01_stdlib_core.md`** for the API surface in detail.
