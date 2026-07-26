# 05 — Configuration patterns

Three ways to configure. One of them is right for production.

---

## 1. `basicConfig()` — scripts and tests only

```python
import logging, sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,           # or filename="app.log", not both
    force=True,                  # 3.8+: remove existing root handlers first
    encoding="utf-8",            # 3.9+, only with filename=
    errors="replace",            # 3.9+
)
```

- **It is a no-op if root already has handlers** — unless you pass `force=True`. This is why
  "my basicConfig does nothing" happens: something (pytest, a notebook, an imported module)
  already configured root.
- `handlers=[...]` accepts a list, and is mutually exclusive with `stream`/`filename`.
- Fine for a script, a one-file tool, or a test fixture. **Not** for an application with
  more than one sink.

## 2. `fileConfig()` — legacy, avoid in new code

`logging.config.fileConfig("logging.ini")`. INI format, defaults to
`disable_existing_loggers=True`, can't express filters cleanly. It exists for
backwards compatibility. Alembic still ships one. Don't start here.

## 3. `dictConfig()` — **the production answer**

This is what Django, uvicorn, pip, Airflow, and Celery all use.

```python
import logging.config, os, sys

LOGGING = {
    "version": 1,                          # always literally 1
    "disable_existing_loggers": False,     # ALWAYS. see below.

    "filters": {
        "request_id": {"()": "myapp.log.RequestIdFilter"},
        "redact":     {"()": "myapp.log.SecretsFilter"},
    },

    "formatters": {
        "console": {
            "format": "%(asctime)s.%(msecs)03d %(levelname)-8s [%(request_id)s] %(name)s — %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "json": {"()": "myapp.log.JsonFormatter"},
    },

    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "json" if os.getenv("ENV") == "prod" else "console",
            "filters": ["request_id", "redact"],
            "level": "DEBUG",
        },
        "errors": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "formatter": "json",
            "level": "ERROR",
        },
    },

    "loggers": {
        "myapp":            {"level": os.getenv("LOG_LEVEL", "INFO")},
        "urllib3":          {"level": "WARNING"},
        "botocore":         {"level": "WARNING"},
        "sqlalchemy.engine":{"level": "WARNING"},
        "uvicorn.access":   {"handlers": ["stdout"], "level": "INFO", "propagate": False},
    },

    "root": {"handlers": ["stdout", "errors"], "level": "INFO"},
}

logging.config.dictConfig(LOGGING)
```

### The keys, precisely

| Key | Meaning |
|---|---|
| `version` | Must be `1`. Not a version of *your* config — of the schema. |
| `disable_existing_loggers` | **Default `True`.** Set `False`. See below. |
| `formatters` | name → `{format, datefmt, style, validate, defaults}` or `{"()": factory}` |
| `filters` | name → `{"()": dotted.path.to.Filter}` (+ any constructor kwargs) |
| `handlers` | name → `{class, level, formatter, filters, ...ctor kwargs}` |
| `loggers` | name → `{level, handlers, filters, propagate}` |
| `root` | same shape as a logger entry, for the root logger |
| `incremental` | `True` = only adjust levels on existing objects, don't rebuild. Rarely used. |

### `disable_existing_loggers` — the trap

With the default `True`, every logger that already exists and isn't named in your config
gets `.disabled = True`. Since `getLogger(__name__)` runs at *import* time, and your config
runs later in `main()`, **every library you imported goes silent.** The symptom is
"SQLAlchemy/boto3 logs nothing and I can't figure out why".

Django, uvicorn, pip, and Airflow all set it to `False`. So should you. There is essentially
no case where `True` is what you want.

### `"()"` — the factory key

```python
"formatters": {"json": {"()": "pythonjsonlogger.json.JsonFormatter", "fmt": "%(name)s %(message)s"}}
"filters":    {"debug_only": {"()": "django.utils.log.RequireDebugTrue"}}
"handlers":   {"h": {"()": "myapp.log.make_handler", "size": 10}}
```

`"class"` is for handlers instantiated normally. `"()"` calls an arbitrary callable with the
remaining keys as kwargs — the escape hatch for anything the schema can't express.

### `ext://` and `cfg://`

- `ext://sys.stdout` — resolve a dotted external name (needed because JSON/YAML files
  can't hold Python objects).
- `cfg://handlers.stdout` — reference another part of the same config dict.

### Loading from a file

```python
import json, logging.config, pathlib
logging.config.dictConfig(json.loads(pathlib.Path("logging.json").read_text(encoding="utf-8")))
```

YAML works the same via `yaml.safe_load`. Keeping config out of code lets ops change log
levels without a deploy — which is why uvicorn's `--log-config` accepts `.json`, `.yaml`,
and `.ini`.

---

## Pattern: correlation IDs with `contextvars` + a `Filter`

The problem: in a concurrent server, `request A` and `request B` interleave in the log and
you can't tell which line belongs to which. You need a per-request ID on every line, without
passing it into every function.

`contextvars` is the async-safe (and thread-safe) mechanism. `threading.local` is **not**
sufficient for asyncio — many coroutines share one thread.

```python
# myapp/log.py
import contextvars, logging, uuid

request_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_id", default=None
)

class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get() or "-"
        return True     # never drops; we're here for the side effect
```

```python
# middleware
from starlette.middleware.base import BaseHTTPMiddleware

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        rid = request.headers.get("X-Request-ID") or uuid.uuid4().hex[:12]
        token = request_id_var.set(rid)
        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = rid
            return response
        finally:
            request_id_var.reset(token)      # ALWAYS reset with the token
```

Then `%(request_id)s` works everywhere, including inside third-party library logs, because
the filter is on the handler and everything propagates to root.

⚠️ **The QueueHandler interaction.** Contextvars are read in whichever thread calls
`filter()`. If the filter is attached to a downstream handler owned by a `QueueListener`,
it runs in the *listener thread* where the contextvar is unset, and you get `-` forever.
Attach the context filter to the **`QueueHandler`** (which runs in the originating thread,
before enqueue), and the stamped attribute travels with the record.

```python
queue_handler.addFilter(RequestIdFilter())     # correct: originating thread
file_handler.addFilter(RequestIdFilter())      # WRONG under a QueueListener: always "-"
```

Alternative for pre-3.7 style or non-async code: `logging.setLogRecordFactory` to stamp
every record at creation.

```python
_old = logging.getLogRecordFactory()
def factory(*args, **kwargs):
    record = _old(*args, **kwargs)
    record.request_id = request_id_var.get() or "-"
    return record
logging.setLogRecordFactory(factory)
```

This runs in the originating thread by construction, so it sidesteps the queue problem
entirely. Downside: it's global, so only the application may do it.

---

## Pattern: JSON logs with zero dependencies

```python
import json, logging

_RESERVED = set(logging.LogRecord("", 0, "", 0, "", (), None).__dict__) | {
    "message", "asctime", "taskName"
}

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S") + f".{int(record.msecs):03d}Z",
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
        }
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        if record.stack_info:
            payload["stack"] = self.formatStack(record.stack_info)
        # everything passed via extra={...}
        for k, v in record.__dict__.items():
            if k not in _RESERVED and not k.startswith("_"):
                payload[k] = v
        return json.dumps(payload, default=str, ensure_ascii=False)
```

Usage:

```python
logger.info("charge succeeded", extra={"user_id": 42, "amount_cents": 999})
# {"ts":"2026-07-25T11:02:14.331Z","level":"INFO","logger":"billing","msg":"charge succeeded",
#  "module":"billing","line":88,"user_id":42,"amount_cents":999}
```

`default=str` stops `TypeError: Object of type UUID is not JSON serializable` from taking
down your logging. `ensure_ascii=False` keeps non-English text readable.

Off-the-shelf alternatives: `python-json-logger` (a formatter, drops into dictConfig),
or structlog (see `08_structlog.md`).

---

## Pattern: level from the environment, per-logger overrides

```python
import os, logging

# LOG_LEVEL=INFO
# LOG_LEVELS=sqlalchemy.engine=WARNING,myapp.worker=DEBUG
root_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.getLogger().setLevel(root_level)

for pair in filter(None, os.getenv("LOG_LEVELS", "").split(",")):
    name, _, lvl = pair.partition("=")
    logging.getLogger(name.strip()).setLevel(lvl.strip().upper())
```

Being able to turn on DEBUG for one module in production, via env var, without a code
change, is worth more than most logging features.

---

## Pattern: quieting third-party noise

```python
for name, level in {
    "urllib3": "WARNING",
    "botocore": "WARNING",
    "boto3": "WARNING",
    "s3transfer": "WARNING",
    "asyncio": "WARNING",
    "PIL": "INFO",
    "matplotlib": "WARNING",
    "sqlalchemy.engine": "WARNING",
    "httpx": "WARNING",
    "httpcore": "WARNING",
    "watchfiles": "WARNING",
}.items():
    logging.getLogger(name).setLevel(level)
```

Do this **after** `dictConfig`, or express it in the `loggers` section of the config.

---

## Pattern: redaction as a filter

```python
import re, logging

_PATTERNS = [
    (re.compile(r"(?i)(authorization|api[_-]?key|password|secret|token)\"?\s*[:=]\s*\"?([^\s\"',}]+)"), r"\1=***"),
    (re.compile(r"\b\d{13,19}\b"), "****CARD****"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "***@***"),
]

class SecretsFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        for pat, repl in _PATTERNS:
            msg = pat.sub(repl, msg)
        record.msg, record.args = msg, ()     # collapse args; msg is now final
        return True
```

Attach to handlers (or the QueueHandler). Airflow ships exactly this idea as
`_secrets_masker`. Doing it in a filter means a careless `logger.info(request_body)` at some
call site can't leak — you fix it in one place.

Note the cost: collapsing `record.args` means downstream aggregators lose the message
template for grouping. Accept it, or only redact known-sensitive `extra` fields instead.

---

Next: **`06_pitfalls.md`**.
