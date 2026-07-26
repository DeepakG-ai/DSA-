# 01 — stdlib `logging`: the core API

Reference for the code you actually type. Assumes `00_mental_model.md`.

---

## Getting a logger

```python
import logging

logger = logging.getLogger(__name__)   # module logger — do this in EVERY module
root   = logging.getLogger()           # the root logger (name is "")
```

Never do `logging.info(...)` at module top level in library code. The module-level
functions (`logging.info`, `logging.warning`, …) implicitly call `basicConfig()` on the
**root** logger the first time they run. In an application that already configured logging,
that either does nothing or fights your config. In a library it hijacks the user's setup.

```python
# BAD in a library / any module that isn't __main__
logging.info("starting")

# GOOD
logger = logging.getLogger(__name__)
logger.info("starting")
```

### Logger methods

```python
logger.debug(msg, *args, **kwargs)
logger.info(msg, *args, **kwargs)
logger.warning(msg, *args, **kwargs)
logger.error(msg, *args, **kwargs)
logger.critical(msg, *args, **kwargs)
logger.exception(msg, *args)              # ERROR + traceback; only inside `except`
logger.log(level, msg, *args, **kwargs)   # dynamic level — your OCR `event()` uses this
```

Keyword args accepted by all of them:

| kwarg | Effect |
|-------|--------|
| `exc_info=True` | attach the current exception's traceback |
| `exc_info=exc` | attach a specific exception object's traceback (3.5+) |
| `stack_info=True` | attach the *call stack* even without an exception — great for "who called this?" |
| `stacklevel=2` | report the **caller's** file/line instead of this one (3.8+). Essential when you wrap `logger.info` in your own helper. |
| `extra={...}` | inject attributes onto the LogRecord |

`stacklevel` is the fix for the classic wrapper problem:

```python
def audit(msg, **kv):
    logging.getLogger("audit").info(msg, extra=kv, stacklevel=2)
    #                                              ^^^^^^^^^^^^
    # without this, %(filename)s:%(lineno)d always says "helpers.py:2"
```

### Levels

```python
logger.setLevel(logging.DEBUG)
logger.setLevel("DEBUG")                       # string works too
logger.getEffectiveLevel()                     # int, after walking up the tree
logger.isEnabledFor(logging.DEBUG)             # bool
logging.getLevelName(20)                       # 'INFO'
logging.getLevelNamesMapping()                 # {'INFO': 20, ...}   (Python 3.11+)
logging.disable(logging.INFO)                  # global kill switch: drop INFO and below, everywhere
```

`logging.disable(level)` is process-wide and overrides every logger. Use it to silence
logging inside a hot benchmark, then `logging.disable(logging.NOTSET)` to restore.

---

## Handlers: attaching, level, formatter, filters

```python
h = logging.StreamHandler()                       # defaults to sys.stderr
h.setLevel(logging.INFO)
h.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
h.addFilter(SomeFilter())

logger.addHandler(h)
logger.removeHandler(h)
logger.handlers                                   # the list, mutable
h.flush()
h.close()
```

Handler lifecycle notes:

- `logging.shutdown()` (registered via `atexit` automatically) flushes and closes **all**
  handlers. It runs at normal interpreter exit — not on `os._exit()` or `SIGKILL`.
- Removing a handler does **not** close it. Call `h.close()` yourself if you own it.
- Custom handlers should implement `emit(self, record)` and call `self.handleError(record)`
  on failure. Never let `emit` raise — a logging failure must not kill business code.

```python
class MyHandler(logging.Handler):
    def emit(self, record):
        try:
            line = self.format(record)
            ...                       # do the write
        except Exception:
            self.handleError(record)  # honours logging.raiseExceptions
```

`logging.raiseExceptions = False` in production silences the "--- Logging error ---"
dump to stderr that `handleError` prints by default.

---

## Formatters

```python
logging.Formatter(fmt=None, datefmt=None, style='%', validate=True, *, defaults=None)
```

- `fmt` — the layout string.
- `datefmt` — `strftime` pattern for `%(asctime)s`. **Milliseconds are not `%f`.**
  `strftime` has no millisecond code; use `%(msecs)03d` as a separate field:

  ```python
  logging.Formatter(
      "%(asctime)s.%(msecs)03d %(levelname)-5s %(message)s",
      datefmt="%Y-%m-%d %H:%M:%S",
  )
  ```
  This `%(msecs)03d` trick is the standard workaround; you will see it in most production
  format strings.

- `defaults={"request_id": "-"}` (**Python 3.10+**) — supplies fallbacks so a formatter
  referencing `%(request_id)s` doesn't blow up on records that lack it. Before 3.10 you
  needed a Filter to stamp a default. Use `defaults` when you can; use a Filter when the
  value must be computed per record.

### Custom formatter

Override `format()`. Call `super().format(record)` to get the base string, then decorate:

```python
class ShortPathFormatter(logging.Formatter):
    def format(self, record):
        record.short = record.pathname.rsplit("\\", 1)[-1]
        return super().format(record)
```

⚠️ `Formatter.format()` **caches** the rendered traceback on `record.exc_text`. If two
handlers with different formatters process the same record, the second sees the first's
cached traceback rather than rendering its own. If you need genuinely different traceback
rendering per sink, clear it: `record.exc_text = None` at the top of your `format()`.

`formatException`, `formatStack`, and `formatTime` are the three hooks you override for
finer control.

Real examples of `Formatter` subclasses in the wild:

| Project | Class | Does |
|---------|-------|------|
| Django | `django.utils.log.ServerFormatter` | prefixes `[server_time]`, colourises by status code |
| uvicorn | `uvicorn.logging.DefaultFormatter` | adds `%(levelprefix)s` with ANSI colour |
| uvicorn | `uvicorn.logging.AccessFormatter` | adds `%(client_addr)s`, `%(request_line)s`, `%(status_code)s` |
| pip | `IndentingFormatter` | indents continuation lines, optional timestamp |

---

## Filters

```python
class OnlyModule(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.name.startswith("backend.worker")

handler.addFilter(OnlyModule())
logger.addFilter(OnlyModule())     # also valid, different semantics — see below
```

A plain callable works too (3.2+): `handler.addFilter(lambda r: r.levelno != 30)`.

**Logger filter vs handler filter — the distinction that matters:**

| Attached to | Runs when | Affects |
|-------------|-----------|---------|
| Logger | once, before propagation | that logger **and every handler up the tree** |
| Handler | per handler | only that one destination |

So "only auth events go to security.log" is a **handler** filter:

```python
class SecurityOnlyFilter(logging.Filter):
    """Pass only records emitted by logging.getLogger('security')."""
    def filter(self, record):
        return record.name == "security"

security_file.addFilter(SecurityOnlyFilter())
```

And "stamp every record with the current request id" is a filter used purely for its
side effect — it always returns `True`:

```python
class ContextFilter(logging.Filter):
    def filter(self, record):
        record.request_id = current_request_id.get() or "-"
        return True
```

Django ships a generic version of the first kind, `django.utils.log.CallbackFilter`, which
wraps any predicate:

```python
from django.utils.log import CallbackFilter
handler.addFilter(CallbackFilter(lambda record: record.levelno != logging.WARNING))
```

`logging.Filter("a.b")` with a name arg is a shortcut for "only records from logger `a.b`
or its children".

---

## `LoggerAdapter` — attach fixed context without a filter

```python
base = logging.getLogger(__name__)
log = logging.LoggerAdapter(base, {"tenant": "acme"})
log.info("indexed")     # record.tenant == "acme"
```

Since **Python 3.13** `LoggerAdapter` accepts `merge_extra=True`, so per-call `extra`
merges with the adapter's dict instead of replacing it:

```python
log = logging.LoggerAdapter(base, {"tenant": "acme"}, merge_extra=True)
log.info("indexed", extra={"doc_id": 7})       # both tenant and doc_id present
```

Subclass and override `process(self, msg, kwargs)` for dynamic context. In practice, for
async request-scoped context, a `contextvars` + `Filter` combination (or structlog) beats
`LoggerAdapter`, because the adapter has to be threaded through every call site.

---

## Exceptions and tracebacks

```python
try:
    render_pdf(data)
except ValueError:
    logger.exception("render failed")                 # ERROR + traceback
except Exception as exc:
    logger.error("render failed: %s", exc, exc_info=exc)
    raise RuntimeError("render failed") from exc      # chain, don't swallow
```

- `logger.exception()` outside an `except` block logs `NoneType: None` — useless. Guard it.
- `raise ... from exc` sets `__cause__` so the printed traceback says
  "The above exception was the direct cause of…". Your `object_store.py` and `processor.py`
  both do this correctly.
- `stack_info=True` gives you the call stack *leading to the log call*, independent of any
  exception. Best debugging flag almost nobody uses.

### Uncaught exceptions

By default an uncaught exception goes to `stderr` and **never reaches your handlers** —
so it is missing from `error.log`. Wire it up:

```python
import sys

def _log_uncaught(exc_type, exc, tb):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc, tb)
        return
    logging.getLogger("uncaught").critical("unhandled exception", exc_info=(exc_type, exc, tb))

sys.excepthook = _log_uncaught
threading.excepthook = lambda a: _log_uncaught(a.exc_type, a.exc_value, a.exc_traceback)
```

For asyncio: `loop.set_exception_handler(...)`.

---

## Capturing other sources

```python
logging.captureWarnings(True)     # warnings.warn() -> logger "py.warnings"
```

Bridging `print()` is not supported; the fix is to stop using `print`.

For third-party libraries that are too loud:

```python
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.INFO)
logging.getLogger("uvicorn.access").propagate = False     # kill duplicate access lines
```

For libraries that log nothing, or that complain "No handlers could be found":
a well-behaved library adds `logging.getLogger(__name__).addHandler(logging.NullHandler())`
in its `__init__.py`. Do that if you ever publish a package.

---

## Performance knobs

```python
logging.logProcesses = False     # skip os.getpid()      per record
logging.logThreads   = False     # skip threading ident  per record
logging.logMultiprocessing = False
logging._srcfile = None          # skip the stack walk that finds filename/lineno — big win
```

The stack walk for `%(filename)s`/`%(lineno)d`/`%(funcName)s` is the most expensive part of
creating a record. If your format string doesn't use them, disabling `_srcfile` is real
savings in a hot loop. (It's a private name; document why you touched it.)

The bigger lever is not doing I/O on the request path at all → `QueueHandler`, see
`03_queuehandler_verdict.md`.

---

Next: **`02_open_source_survey.md`** — how Django, uvicorn, Flask, pip, Airflow and
Home Assistant actually configure all this.
