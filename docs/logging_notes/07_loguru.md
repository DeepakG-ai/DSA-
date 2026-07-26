# 07 — loguru

`pip install loguru`

The pitch: **no configuration ceremony.** One pre-made logger object, `add()` a sink, done.
Rotation, retention, compression, colours, JSON, and thread/process safety are constructor
arguments instead of classes you assemble.

---

## Hello world

```python
from loguru import logger

logger.info("it just works")
logger.debug("and DEBUG is on by default")
```

That's the whole difference from stdlib: there is no `getLogger`, no handler, no formatter,
no level to set. A default sink writes colourised output to `sys.stderr` at `DEBUG`.

## The one API you need: `logger.add()`

```python
import sys
from loguru import logger

logger.remove()                       # drop the default stderr sink first — do this ALWAYS

logger.add(
    sys.stdout,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} — {message}",
    colorize=True,
    backtrace=True,      # extended traceback beyond the catching frame
    diagnose=False,      # variable VALUES in the traceback — MUST be False in production
    enqueue=False,
)

logger.add(
    "logs/app_{time:YYYY-MM-DD}.log",
    level="DEBUG",
    rotation="100 MB",          # or "00:00", or "1 week", or a callable
    retention="30 days",        # or a count, or a callable
    compression="zip",          # gz, bz2, xz, tar, zip...
    encoding="utf-8",
    enqueue=True,               # <- multiprocess-safe AND non-blocking
    serialize=False,
)

logger.add("logs/errors.jsonl", level="ERROR", serialize=True, enqueue=True)
```

Every one of those lines replaces a class you'd have written by hand in stdlib.

### `add()` arguments worth knowing

| Arg | Does |
|---|---|
| `sink` | a file path (str/Path), a file object, a callable, a `logging.Handler`, or a coroutine function |
| `level` | `"DEBUG"`, `"INFO"`, … or an int |
| `format` | `{}`-style. Also accepts a callable for dynamic formats. |
| `filter` | callable `record -> bool`, or `{"module.name": "LEVEL"}` dict for per-module levels |
| `serialize=True` | emit one JSON object per line — production structured logging, free |
| `rotation` | `"500 MB"`, `"12:00"`, `"1 week"`, `datetime.time`, `timedelta`, or callable |
| `retention` | `"10 days"`, `5` (files), or callable |
| `compression` | `"gz"`, `"zip"`, `"xz"`, … applied on rotation |
| `enqueue=True` | records go through a multiprocessing queue → **process-safe and non-blocking** |
| `backtrace` | extend the traceback past the catching frame |
| `diagnose` | annotate the traceback with variable values — **leaks secrets, keep `False` in prod** |
| `catch=True` | errors inside the sink don't propagate |

`add()` returns an int id; `logger.remove(id)` removes just that sink.

### `enqueue=True` is loguru's answer to `QueueHandler`

Same idea as `03_queuehandler_verdict.md`, but one keyword instead of a `QueueHandler` +
`QueueListener` + start/stop lifecycle. It uses a `multiprocessing.SimpleQueue`, so unlike
stdlib's in-process `queue.Queue` it is genuinely **multi-process safe** — several worker
processes can write the same file.

Cost: pickling per record, and you should call `logger.complete()` before exit to drain it.

---

## Context: `bind()` and `contextualize()`

```python
# bind() returns a NEW logger with extra fields attached
user_log = logger.bind(user_id=42, tenant="acme")
user_log.info("charged")          # record["extra"] == {"user_id": 42, "tenant": "acme"}

# contextualize() is a context manager — applies to everything inside, contextvar-based
with logger.contextualize(request_id="abc123"):
    do_work()                     # every log inside, at any depth, carries request_id
```

`contextualize()` is built on `contextvars`, so it works correctly in asyncio and threads.
This is loguru's equivalent of the `ContextVar` + `Filter` dance in `05_config_patterns.md`,
in one line.

Reference bound fields in the format string via `extra`:

```python
logger.add(sys.stdout, format="{time} | {extra[request_id]} | {message}")
# use logger.configure(extra={"request_id": "-"}) to supply a default
```

## Exceptions: `@logger.catch`

```python
@logger.catch
def risky(x):
    return 1 / x

risky(0)      # logged with full traceback, function does not raise
```

```python
@logger.catch(reraise=True, message="render failed")
def render(): ...
```

Or as a context manager:

```python
with logger.catch(message="batch failed"):
    process_batch()
```

Loguru's tracebacks are genuinely better than stdlib's — colourised, and with
`backtrace=True` they show the full chain including frames above the `try`.

## Custom levels

```python
logger.level("NOTICE", no=25, color="<cyan>", icon="📢")
logger.log("NOTICE", "deploy started")
```

Cleaner than `logging.addLevelName` + a custom method on Logger.

## `logger.opt()`

```python
logger.opt(exception=True).error("failed")     # attach current exception
logger.opt(lazy=True).debug("heavy={}", lambda: expensive())   # only called if DEBUG on
logger.opt(depth=1).info("from my wrapper")    # like stdlib stacklevel
logger.opt(colors=True).info("<red>danger</red>")
logger.opt(raw=True).info("no formatting at all\n")
```

---

## The critical problem: third-party libraries

**Every library on PyPI logs through stdlib `logging`, not loguru.** So by default,
SQLAlchemy, boto3, uvicorn, and httpx logs bypass loguru entirely and go wherever stdlib
sends them. You get two disjoint log streams.

The standard fix is an `InterceptHandler` — a stdlib handler that forwards into loguru:

```python
import logging, sys
from loguru import logger

class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        # walk back to the frame that actually made the call
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

def setup_logging(level="INFO"):
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(level)
    for name in list(logging.root.manager.loggerDict):
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    logger.remove()
    logger.add(sys.stdout, level=level, serialize=False)
```

It works, and it is in loguru's own documented recipes — but note what just happened: you
wrote 20 lines of stdlib logging code to make loguru usable in a real app. **That is the
honest cost of loguru in a service.** In a script or CLI, this problem doesn't exist.

Going the other direction (loguru → a stdlib handler) is easy: `logger.add(some_handler)`
accepts a `logging.Handler` as a sink.

---

## When loguru wins

- Scripts, CLIs, data pipelines, notebooks, ML training loops, personal tools
- Any project where **you own every line of code that logs**
- When you want rotation + retention + compression + JSON in four lines
- When you want the best tracebacks available in Python without effort
- Prototyping — you can always migrate later; the call sites are similar

## When loguru loses

- **Libraries.** Never make a published library depend on loguru; it forces your dependency
  and your configuration onto every user. Libraries use stdlib + `NullHandler`. Full stop.
- Large services where third-party log control matters → the InterceptHandler tax
- Teams/infra standardised on `dictConfig`, or platforms that inject a logging config
- Anywhere ops needs to change logging via config file without a code change (loguru config
  is Python code; `logger.configure(**json.load(...))` helps but is less established)
- OpenTelemetry / APM integrations, which nearly all hook stdlib `logging`

---

## Sources

- [loguru documentation](https://loguru.readthedocs.io/en/stable/)
- [loguru — `add()` API reference](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.add)
- [Logging in Python: A Comparison of the Top 6 Libraries — Better Stack](https://betterstack.com/community/guides/logging/best-python-logging-libraries/)
- [5 Best Python Logging Libraries in 2026 — Dash0](https://www.dash0.com/guides/python-logging-libraries)
