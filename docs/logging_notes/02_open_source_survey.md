# 02 — How real open-source Python projects do logging

Not opinion. This is what is in the source of projects you already have installed.
Every quote below is from the actual repository.

---

## The question: is logging centralized or not?

**Yes — and there is no disagreement about it across the ecosystem.** The pattern is
universal enough to state as one rule:

> **Libraries never configure logging. Applications configure it once, centrally, at startup.**

There are two halves and both matter:

### Half 1 — library code: `getLogger(__name__)` and nothing else

A library must not decide where the user's logs go. So library modules do exactly one thing:

```python
import logging
logger = logging.getLogger(__name__)
```

...and packages that want to be polite add a `NullHandler` at package import so that a
library logging with no application config produces silence, not a "No handlers could be
found" warning:

```python
# requests/__init__.py  — literally this
import logging
from logging import NullHandler
logging.getLogger(__name__).addHandler(NullHandler())
```

`urllib3`, `boto3`/`botocore`, `httpx`, `SQLAlchemy` and essentially every serious library
do the same. **This is the officially documented rule** in the Python "Configuring Logging
for a Library" HOWTO.

Practical consequence for you: `pip install`-ing something never changes your log output.
And it means **one central config controls every library's logs too**, because they all
propagate to root.

### Half 2 — application code: `dictConfig()` exactly once at startup

Almost every application-shaped project converges on
`logging.config.dictConfig()` called once, from the entry point.

---

## The evidence, project by project

### Django — centralized `dictConfig`, defaults + user merge

`django/utils/log.py`:

```python
DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {"handlers": ["console", "mail_admins"], "level": "INFO"},
        "django.server": {"handlers": ["django.server"], "level": "INFO", "propagate": False},
    },
}
```

Applied by `configure_logging()` → `logging.config.dictConfig()`. The user's
`settings.LOGGING` dict is then applied on top.

**Lessons to steal:**
- `"version": 1` is mandatory and is always literally 1. It has never changed.
- `"disable_existing_loggers": False` — **always set this.** The default is `True`, which
  silently disables every logger created before your config ran (i.e. every library you
  imported at the top of your file). This is the single most common dictConfig bug.
- `"()"` (the "factory key") instantiates an arbitrary callable — that is how you plug in
  a custom formatter/filter/handler class from a config dict.
- Environment differences are expressed as **filters** (`require_debug_true`), not as
  `if DEBUG:` branches sprinkled through the config.
- Log to the console in dev, **email admins on ERROR in prod** — that's `AdminEmailHandler`,
  a `SMTPHandler` derivative with rate limiting.

### uvicorn — centralized `dictConfig`, and it owns only its own logger names

`uvicorn/config.py`:

```python
LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
        },
    },
    "handlers": {
        "default": {"formatter": "default", "class": "logging.StreamHandler", "stream": "ext://sys.stderr"},
        "access":  {"formatter": "access",  "class": "logging.StreamHandler", "stream": "ext://sys.stdout"},
    },
    "loggers": {
        "uvicorn":        {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error":  {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"],  "level": "INFO", "propagate": False},
    },
}
```

Applied in `Config.configure_logging()` via `logging.config.dictConfig(self.log_config)`.

**Lessons to steal:**
- **Only `StreamHandler`. No files.** A server process writes to stdout/stderr and lets the
  platform (systemd, Docker, ECS, k8s) capture it. This is 12-Factor and it is what
  virtually all modern service code does.
- Access logs → **stdout**, error/diagnostic logs → **stderr**. Separate streams so
  operators can route them differently.
- `"stream": "ext://sys.stderr"` — `ext://` is dictConfig's syntax for "resolve this dotted
  name at config time". You need it because JSON/YAML config files can't hold Python objects.
- `propagate: False` on the loggers it owns, so a host app's root handlers don't duplicate
  uvicorn's already-formatted lines.

### Flask — deliberately *minimal*, and a great lesson in restraint

`flask/logging.py` does **not** call `basicConfig` or `dictConfig`. It:

1. `logging.getLogger(app.name)`
2. sets level to `DEBUG` only if `app.debug`
3. adds a single `StreamHandler` **only if no handler in the chain already handles that level**

```python
def has_level_handler(logger):
    """Check if there is a handler in the logging chain that will handle
    the given logger's effective level."""
```

and the stream is dynamic:

```python
def wsgi_errors_stream():
    """Find the most appropriate error stream for the application.
    If a request is active, log to ``wsgi.errors``, otherwise use ``sys.stderr``."""
```

**Lesson to steal:** a framework that might be embedded in someone else's app checks
whether logging is *already* configured before touching anything. `has_level_handler`
is a pattern worth copying if you ever write a reusable component.

### pip — centralized `dictConfig` in a CLI, with custom handlers

`pip/_internal/utils/logging.py` calls `logging.config.dictConfig({...})` from
`setup_logging()`. Its handlers:

- `console`, `console_errors`, `console_subprocess` — three console handlers separated by
  **filters** (`exclude_warnings`, `restrict_to_subprocess`, `exclude_subprocess`)
- `user_log` — an optional `BetterRotatingFileHandler` (subclasses `RotatingFileHandler`,
  overrides `_open()` to `mkdir` the parent first)
- `RichPipStreamHandler` — colour output, and it catches `BrokenPipeError` on stdout and
  raises `BrokenStdoutLoggingError`

**Lessons to steal:**
- Splitting one destination into several handlers separated by filters is normal and clean.
- Subclassing `RotatingFileHandler` just to `mkdir -p` the directory is a well-known
  necessity — the stdlib handler will not create the directory for you.
- A CLI must survive `| head` closing the pipe. Handling `BrokenPipeError` in the handler
  is the correct place.

### Apache Airflow — centralized `dictConfig`, biggest real-world example

`airflow/config_templates/airflow_local_settings.py` builds `DEFAULT_LOGGING_CONFIG` with
`version: 1`, `disable_existing_loggers: False`, formatters, filters, handlers, loggers —
and then swaps the task handler based on config:

- local: `FileTaskHandler`
- remote: `S3RemoteLogIO`, `CloudWatchRemoteLogIO`, `GCSRemoteLogIO`, `WasbRemoteLogIO`,
  `StackdriverRemoteLogIO`, `ElasticsearchRemoteLogIO`, `OpensearchRemoteLogIO`, …

It also ships a **secrets-masking filter** (`_secrets_masker`) that scrubs connection
strings and passwords out of every record.

**Lessons to steal:**
- Sink choice (local file vs S3 vs CloudWatch) is a **config swap of one handler**, not
  a code change. That's the payoff of dictConfig.
- **A masking `Filter` is the right place for redaction** — it applies to every handler at
  once and can't be forgotten at a call site.

### Home Assistant — centralized, *and it uses `QueueHandler`*

`homeassistant/util/logging.py`:

```python
class HomeAssistantQueueHandler(logging.handlers.QueueHandler):
    """Process the log in another thread."""

class HomeAssistantQueueListener(logging.handlers.QueueListener):
    """Custom QueueListener to watch for noisy loggers."""
```

and `async_activate_log_queue_handler()`, whose docstring is the whole justification:

> "Migrate the existing log handlers to use the queue. This allows us to avoid blocking I/O
> and formatting messages in the event loop as log messages are written in another thread."

Note the shape: it **starts with normal handlers, then migrates them behind a queue** once
the event loop is up. It also subclasses `QueueHandler` to skip the stdlib's locking and
`prepare()` overhead, since the queue is in-process.

This one matters for your question — see `03_queuehandler_verdict.md`.

### Celery — centralized, but it *hijacks* stdout too

Celery configures logging on worker start (`setup_logging_subsystem`) and additionally
redirects `sys.stdout`/`sys.stderr` into a logger so that `print()` inside a task lands in
the log instead of vanishing. It also fires signals (`setup_logging`, `after_setup_logger`)
so users can override the whole thing.

**Lesson to steal:** if you own the process (worker, daemon), capturing stray `print()`
is legitimate. If you're a library, never do this.

### Scientific stack — barely logs at all

`numpy`, `pandas`, `scikit-learn` use `warnings.warn()` far more than logging. That is a
real, valid choice: `warnings` is for "your code is doing something questionable" aimed at
the *developer*, logging is for "here is what happened at runtime" aimed at the *operator*.
Bridge them with `logging.captureWarnings(True)`.

---

## The consensus pattern (what "industry standard" actually means)

Combining all of the above, this is the shape almost every production Python service has:

```
1. Every module:          logger = logging.getLogger(__name__)
2. One entry point:       logging.config.dictConfig(CONFIG)   # ONCE, first thing
3. disable_existing_loggers: False                            # ALWAYS
4. Handlers attach to ROOT (or to the few loggers you own)
5. In containers: StreamHandler -> stdout, JSON format, and STOP.
   The platform collects it. No file handlers, no rotation, no log shipping in-process.
6. On a VM / bare metal: RotatingFileHandler or TimedRotatingFileHandler,
   or better, write to stdout and let systemd/journald handle it.
7. Correlation IDs via contextvars + a Filter (or structlog's bind_contextvars).
8. Redaction via a Filter, so it cannot be forgotten.
9. Level from an env var:  LOG_LEVEL=INFO
10. NEVER log secrets, tokens, full request bodies, or PII.
```

### The single biggest one: log to stdout in containers

The [12-Factor App](https://12factor.net/logs) rule — "a twelve-factor app never concerns
itself with routing or storage of its output stream" — is now the default assumption of
every container platform. Docker, Kubernetes, ECS, Cloud Run, Heroku, and systemd all
capture stdout automatically.

If you are deploying in a container and writing to `logs/app.log` inside the container, you
have built a problem for yourself:

- the file dies with the container
- `docker logs` shows nothing
- you need rotation, or the disk fills
- you need a sidecar (Fluent Bit / Filebeat / Vector) to ship the file anyway
- concurrent writes from multiple processes to one file are **not supported by Python**

Writing to stdout deletes all five problems at once.

**When file handlers ARE still correct:**
- desktop / CLI apps (pip's `user_log`, Home Assistant's `home-assistant.log`)
- long-lived VM daemons without a log collector
- an audit/billing trail that must survive independently of the log pipeline —
  and then it usually belongs in a **database or object store**, not a text file
- local development, for convenience

---

## The multi-process rule everyone learns the hard way

Straight from the official cookbook:

> "Although logging is thread-safe, and logging to a single file from multiple threads in a
> single process *is* supported, logging to a single file from *multiple processes* is
> *not* supported, because there is no standard way to serialize access to a single file
> across multiple processes in Python."

So with Gunicorn/uWSGI workers, Celery prefork pools, or `multiprocessing`:

- `RotatingFileHandler` from N processes → **interleaved and truncated lines, and rotation
  races that delete data.** This is real, not theoretical.
- The cookbook's recommendation for web apps:

  > "When deploying web applications using Gunicorn or uWSGI (or similar), multiple worker
  > processes are created to handle client requests. In such environments, avoid creating
  > file-based handlers directly in your web application. Instead, use a `SocketHandler` to
  > log from the web application to a listener in a separate process."

- Or, the modern answer: **every process writes JSON to its own stdout**, and the platform
  merges the streams. No coordination needed at all.

---

## Sources

- [Django `django/utils/log.py`](https://github.com/django/django/blob/main/django/utils/log.py)
- [uvicorn `uvicorn/config.py`](https://github.com/encode/uvicorn/blob/master/uvicorn/config.py)
- [Flask `src/flask/logging.py`](https://github.com/pallets/flask/blob/main/src/flask/logging.py)
- [pip `src/pip/_internal/utils/logging.py`](https://github.com/pypa/pip/blob/main/src/pip/_internal/utils/logging.py)
- [Airflow `airflow_local_settings.py`](https://github.com/apache/airflow/blob/main/airflow-core/src/airflow/config_templates/airflow_local_settings.py)
- [Home Assistant `homeassistant/util/logging.py`](https://github.com/home-assistant/core/blob/dev/homeassistant/util/logging.py)
- [Logging Cookbook — Python docs](https://docs.python.org/3/howto/logging-cookbook.html)
- [Configuring Logging for a Library — Python docs](https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library)
- [The Twelve-Factor App — Logs](https://12factor.net/logs)
