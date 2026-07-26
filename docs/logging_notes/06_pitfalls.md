# 06 — Pitfalls that actually bite

Ordered roughly by how often they cost people a day.

---

### 1. Naming a file/folder after a stdlib module

Covered in `README.md`. `logging.py`, `queue.py`, `json.py`, `types.py`, `select.py`,
`email.py`, `secrets.py`, `random.py`, `copy.py`, `test.py`, `string.py`, `token.py`.
Symptom: `AttributeError: module 'X' has no attribute 'Y'` on a stdlib call.
Check with `print(logging.__file__)`.

### 2. `disable_existing_loggers` defaults to `True`

`dictConfig` silently disables every logger created before it ran. Every library you
imported goes quiet. **Always set `"disable_existing_loggers": False`.**

### 3. Setting the logger level but not the handler level (or vice versa)

Two independent checks. Both must pass.

```python
logger.setLevel(logging.DEBUG)     # record is created
handler.setLevel(logging.WARNING)  # ...and this handler drops it anyway
```

Debug it with:

```python
print(logger.getEffectiveLevel(), [(h, h.level) for h in logger.handlers])
```

Also: `QueueListener(..., respect_handler_level=False)` is the **default**, which means the
listener ignores handler levels entirely and every record goes to every downstream handler.
Pass `respect_handler_level=True`.

### 4. Duplicate log lines

Cause: a handler on both a child logger and root, with `propagate=True` (the default).

```python
logger.propagate = False          # fix A
# fix B: only ever attach handlers to root
# fix C: guard re-configuration so it can't run twice
```

Also caused by running `dictConfig`/`addHandler` twice — common in notebooks, in
`if __name__ == "__main__"` under Gunicorn's `--reload`, and in pytest. Guard it:

```python
_CONFIGURED = False
def configure_logging():
    global _CONFIGURED
    if _CONFIGURED:
        return
    _CONFIGURED = True
    ...
```

Or clear first: `for h in list(root.handlers): root.removeHandler(h)`.

### 5. `basicConfig()` silently does nothing

It's a no-op when root already has handlers. Use `force=True` if you mean it.

### 6. Using f-strings in the log call

```python
logger.debug(f"payload={huge_dict}")     # serializes even when DEBUG is off
logger.debug("payload=%s", huge_dict)    # only if a handler accepts the record
```

Also breaks log aggregation grouping (every message is unique), and enables format-string
injection if the message contains user data with `%` or `{}`.

### 7. `logger.exception()` outside an `except` block

Logs `NoneType: None`. Use `logger.error("...", exc_info=exc)` when you have the object,
or restructure so the call is inside the handler.

### 8. Swallowing exceptions with a bare `except`

```python
try:
    do_work()
except Exception:
    logger.error("failed")          # traceback GONE. Where did it fail? Unknowable.
```

Use `logger.exception("failed")`, or `exc_info=True`. And prefer
`raise MyError("context") from exc` over swallowing.

### 9. Missing `encoding="utf-8"` on file handlers (Windows especially)

Without it, Python uses the locale encoding — `cp1252` on a default Windows install. The
first `→`, `é`, `—`, or emoji in a log message raises:

```
UnicodeEncodeError: 'charmap' codec can't encode character '→'
```

Set `encoding="utf-8"` on **every** `FileHandler`/`RotatingFileHandler`, and consider
`errors="replace"` when reading logs back. Python 3.15 changes the default to UTF-8, but be
explicit. (Same for the console: `PYTHONIOENCODING=utf-8`, or
`sys.stdout.reconfigure(encoding="utf-8")`.)

### 10. Log directory doesn't exist

`FileHandler` won't create it. `FileNotFoundError` at startup, often only in the
container where you forgot the `mkdir`. Do `Path(p).parent.mkdir(parents=True, exist_ok=True)`
before configuring, or subclass `_open()` like pip does.

### 11. Rotating a file from multiple processes

Officially unsupported. Interleaved lines, truncation, and rotation races that lose data.
Gunicorn workers, Celery prefork, `multiprocessing` — all affected.
Answers: per-process files, `SocketHandler` to one collector, or (best) stdout per process.

### 12. External `logrotate` + a plain `FileHandler`

After `logrotate` renames the file, your handler keeps writing to the unlinked inode.
Logs appear to stop; disk keeps filling. Use `WatchedFileHandler`, or `copytruncate` in
the logrotate config, or let Python do the rotation and turn logrotate off for that file.

### 13. `extra` key collisions

```python
logger.info("hi", extra={"message": "x"})
# KeyError: "Attempt to overwrite 'message' in LogRecord"
```

Reserved: `message`, `asctime`, `name`, `msg`, `args`, `levelname`, `levelno`, `pathname`,
`filename`, `module`, `exc_info`, `exc_text`, `stack_info`, `lineno`, `funcName`, `created`,
`msecs`, `relativeCreated`, `thread`, `threadName`, `processName`, `process`, `taskName`.
Namespace yours: `extra={"app_user_id": 42}`.

### 14. A formatter referencing a field that isn't always present

`%(request_id)s` on a record from a third-party library that never went through your filter
→ `ValueError: Formatting field not found in record`. Fixes:
- attach the stamping `Filter` to the **handler**, not the logger, so it covers every record
- or `Formatter(..., defaults={"request_id": "-"})` (Python 3.10+)

### 15. Contextvars evaluated in the wrong thread

Under `QueueListener`, downstream handlers run on the listener thread where your
contextvars are empty. Stamp on the `QueueHandler` (originating thread) or via
`setLogRecordFactory`. Symptom: correlation IDs are always the default value.

### 16. Not stopping the `QueueListener` on shutdown

Records still in the queue when the process exits are lost — exactly the records you want
when investigating why it exited. Call `listener.stop()` from your lifespan shutdown /
`atexit`.

### 17. Logging secrets

Tokens, passwords, API keys, `Authorization` headers, full request/response bodies, PII,
card numbers, connection strings. Logs get shipped to third parties, indexed, and retained
for years. Use a redaction `Filter` (`05_config_patterns.md`) so it's structural, not
a discipline problem.

### 18. Logging inside a tight loop

A million INFO lines per minute costs real money in an aggregator and buries the signal.
Options: log a summary after the loop, sample (`if i % 1000 == 0`), or use a rate-limiting
filter.

```python
class RateLimitFilter(logging.Filter):
    def __init__(self, per_seconds=60):
        super().__init__()
        self.per_seconds, self._seen = per_seconds, {}
    def filter(self, record):
        key = (record.name, record.levelno, record.msg)   # the TEMPLATE, not the message
        now = time.monotonic()
        last = self._seen.get(key, 0.0)
        if now - last < self.per_seconds:
            return False
        self._seen[key] = now
        return True
```

(Note this keys on `record.msg`, which is why lazy `%s` args matter — with f-strings every
message is distinct and rate limiting can't work.)

### 19. `logging.shutdown()` doesn't run on hard exit

It's registered with `atexit`, so `os._exit()`, `SIGKILL`, and a segfault skip it — buffered
records are lost. If a log must not be lost, flush it explicitly at write time, or don't put
it in a log file at all (use the database).

### 20. Using logs where you need something else

- **Metrics** (counts, latencies, rates) → Prometheus/OpenTelemetry, not `logger.info`
  plus a `grep | wc -l`.
- **Traces** (request through 6 services) → OpenTelemetry spans.
- **Billing / audit records that must not be lost** → a database transaction. A log file has
  no durability guarantee, no schema, and no transactional relationship with the work it
  describes. If losing a line costs money, it isn't a log.

### 21. Tests that leak logging config

pytest's `caplog` fixture and `logging` interact badly with global config. Use `caplog` for
assertions; use `caplog.set_level(...)` rather than reconfiguring; and in fixtures that do
configure logging, tear down handlers afterwards.

```python
def test_it(caplog):
    with caplog.at_level(logging.INFO, logger="myapp"):
        do_thing()
    assert "started" in caplog.text
    assert caplog.records[0].levelno == logging.INFO
```

### 22. `%(taskName)s` and asyncio

Available only from Python 3.12. Before that, correlate asyncio work with contextvars.

---

Next: **`07_loguru.md`**.
