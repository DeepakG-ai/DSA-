# 08 — structlog

`pip install structlog`

The pitch: **stop writing sentences, start emitting events with fields.**

```python
logger.info("charged card for user 42 amount 9.99")               # stdlib thinking
log.info("card_charged", user_id=42, amount=9.99, currency="usd") # structlog thinking
```

The second one is queryable: `user_id:42 AND amount>5` in Datadog/Loki/CloudWatch/ELK,
with no regex. That is the entire value proposition, and it's why structlog is the choice
for large services.

---

## Hello world

```python
import structlog

log = structlog.get_logger()
log.info("service_started", port=8000, workers=4)
```

Out of the box you get pretty, colourised, aligned key-value console output. No config
needed to start.

## The core idea: a processor chain

Every log call produces a **dict** (`event_dict`). structlog pipes it through a list of
**processors** — plain functions `(logger, method_name, event_dict) -> event_dict`. The last
one is a **renderer** that turns the dict into a string (or bytes).

```
log.info("card_charged", user_id=42)
        |
        v
  {"event": "card_charged", "user_id": 42}
        |
   merge_contextvars   -> adds request_id from contextvars
   add_log_level       -> {"level": "info"}
   add_logger_name     -> {"logger": "billing"}
   TimeStamper(iso)    -> {"timestamp": "2026-07-25T11:02:14Z"}
   StackInfoRenderer   -> handles stack_info=True
   format_exc_info     -> renders exceptions
   JSONRenderer        -> '{"event":"card_charged","user_id":42,...}'
        |
        v
     the sink
```

You compose the chain. That's the whole design.

## Configuration

```python
import logging, sys, structlog

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,      # ALWAYS first
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),          # or ConsoleRenderer() in dev
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
    cache_logger_on_first_use=True,
)
```

| Setting | Meaning |
|---|---|
| `processors` | the chain, in order. Renderer last. |
| `wrapper_class` | what `get_logger()` returns. `make_filtering_bound_logger(level)` is the fast built-in level filter; `structlog.stdlib.BoundLogger` gives you the stdlib-compatible API. |
| `logger_factory` | the final sink. `PrintLoggerFactory` (fast, stdout), `WriteLoggerFactory`, or `structlog.stdlib.LoggerFactory()` to hand off to stdlib. |
| `cache_logger_on_first_use` | `True` in production — big speedup. Means you can't reconfigure after first use. |

Dev vs prod is usually one branch:

```python
renderer = (
    structlog.dev.ConsoleRenderer(colors=True)
    if sys.stderr.isatty()
    else structlog.processors.JSONRenderer()
)
```

## Context: `bind()` and `bind_contextvars()`

**`bind()` — explicit, returns a new logger:**

```python
log = structlog.get_logger()
log = log.bind(request_id="abc123", user_id=42)
log.info("started")     # both fields present
log.info("finished")    # still present

log.unbind("user_id")
log.new(job_id=7)       # clear everything, start fresh
```

Bound loggers are immutable — `bind()` returns a copy. Safe to pass around.

**`bind_contextvars()` — implicit, context-local, the one you want in a server:**

```python
from structlog.contextvars import bind_contextvars, clear_contextvars, bound_contextvars

async def middleware(request, call_next):
    clear_contextvars()                          # ALWAYS clear at request start
    bind_contextvars(request_id=new_id(), path=request.url.path)
    return await call_next(request)

# anywhere, any depth, no plumbing:
structlog.get_logger().info("db_query", table="users", ms=12)
# -> includes request_id and path
```

Or scoped:

```python
with bound_contextvars(job_id=7):
    run_job()
```

This requires `structlog.contextvars.merge_contextvars` to be **first** in your processor
chain. Because it's `contextvars`-based, it is correct in asyncio and in threads.

⚠️ Known wrinkle in Starlette/FastAPI: contextvars set in a sync context (a `def` endpoint
run in a threadpool) don't always appear in logs from the async context and vice versa. Bind
in the middleware, which is async, and it behaves.

---

## Integrating with stdlib — the part that makes structlog the "safe" choice

Unlike loguru, structlog is **designed to sit on top of stdlib logging**. Two directions,
and you usually want both:

**Direction 1 — structlog output goes through stdlib handlers** (so your existing
`dictConfig` handlers, rotation, and QueueHandler still apply):

```python
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,   # <- MUST be last
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
```

**Direction 2 — stdlib records from third-party libraries get rendered by structlog**, so
uvicorn/SQLAlchemy/boto3 logs come out in the same JSON:

```python
formatter = structlog.stdlib.ProcessorFormatter(
    foreign_pre_chain=[                       # applied ONLY to non-structlog records
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
    ],
    processors=[
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
        structlog.processors.JSONRenderer(),
    ],
)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
root = logging.getLogger()
root.handlers = [handler]
root.setLevel(logging.INFO)
```

`ProcessorFormatter` is a `logging.Formatter`, so it drops straight into `dictConfig`:

```python
"formatters": {"structlog": {"()": "myapp.log.make_processor_formatter"}}
```

**This is why structlog wins architecture arguments in big codebases:** you keep the whole
stdlib ecosystem — dictConfig, QueueHandler, Sentry's LoggingIntegration, OpenTelemetry's
LoggingHandler, every library's logger — and you add structured events on top. You are not
choosing *instead of* stdlib; you are choosing *in addition to* it.

---

## Useful processors

| Processor | Does |
|---|---|
| `contextvars.merge_contextvars` | pull in context-local bindings. Put it first. |
| `stdlib.add_log_level` / `add_logger_name` | `level`, `logger` keys |
| `processors.TimeStamper(fmt="iso", utc=True)` | `timestamp` key |
| `processors.format_exc_info` | render `exc_info` to a string. **The safe default.** |
| `processors.dict_tracebacks` | traceback as structured JSON — ⚠️ **also dumps frame locals** |
| `processors.StackInfoRenderer()` | honour `stack_info=True` |
| `processors.CallsiteParameterAdder([...])` | add filename/lineno/func/thread |
| `processors.EventRenamer("msg")` | rename the `event` key (many backends expect `message`) |
| `processors.UnicodeDecoder()` | bytes → str |
| `dev.ConsoleRenderer(colors=True)` | human-readable dev output |
| `processors.JSONRenderer()` | production |

Custom processor — it's just a function:

```python
def drop_healthchecks(logger, method_name, event_dict):
    if event_dict.get("path") == "/health":
        raise structlog.DropEvent          # this is how you drop a record
    return event_dict
```

---

## Exceptions

```python
log = structlog.get_logger()
try:
    charge()
except Exception:
    log.exception("charge_failed", user_id=42)     # level=error + exc_info
```

With `structlog.processors.dict_tracebacks` in the chain, the traceback lands as structured
data (frames as objects) rather than one giant string — searchable in your aggregator.

⚠️ **`dict_tracebacks` also serialises every local variable in each frame.** Run
`examples/ex09_structlog_demo.py` and look at part 4 — the JSON contains the full contents
of the module namespace. In real code those locals hold passwords, tokens, API keys and
customer PII, which then land in your log platform and are retained for years. This is the
same hazard as loguru's `diagnose=True`.

**Use `format_exc_info` in production**; keep `dict_tracebacks` for local development only.

---

## When structlog wins

- Services whose logs go to Datadog / ELK / Loki / CloudWatch Insights / BigQuery
- Microservices needing correlation IDs across service boundaries
- Async web apps — `bind_contextvars` is the cleanest request-scoped context in Python
- Teams: `bind()` makes structured discipline the path of least resistance
- Anywhere you must keep stdlib compatibility (i.e. anywhere with dependencies)

## When structlog loses

- Small scripts — the config block is longer than the script
- Teams that will not adopt the mental shift from sentences to events
- Learning curve is real: bound loggers, processor chains, wrapper classes, logger
  factories, and the `ProcessorFormatter` dual-chain setup all take a while to click

---

## Sources

- [structlog documentation](https://www.structlog.org/en/stable/)
- [Standard Library Logging — structlog](https://www.structlog.org/en/stable/standard-library.html)
- [Context Variables — structlog](https://www.structlog.org/en/stable/contextvars.html)
- [Logging Best Practices — structlog](https://www.structlog.org/en/stable/logging-best-practices.html)
- [Leveling Up Your Python Logs with Structlog — Dash0](https://www.dash0.com/guides/python-logging-with-structlog)
- [Integrating FastAPI with Structlog — wazaari.dev](https://wazaari.dev/blog/fastapi-structlog-integration)
