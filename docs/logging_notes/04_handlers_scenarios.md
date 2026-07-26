# 04 — Every handler, and the scenario it exists for

Lookup table first, details after. All live in `logging` or `logging.handlers`.

---

## The table

| Handler | Module | Use it when | Real project using it |
|---|---|---|---|
| `StreamHandler` | `logging` | **Default answer.** Console / stdout / stderr. Containers. | uvicorn, Django, Flask |
| `FileHandler` | `logging` | Single-process, a file that will never grow large | rare alone |
| `RotatingFileHandler` | `logging.handlers` | Size-capped log file on a VM/desktop | pip (`user_log`) |
| `TimedRotatingFileHandler` | `logging.handlers` | "one file per day", retention in days | Home Assistant, many daemons |
| `WatchedFileHandler` | `logging.handlers` | File rotated by **external** `logrotate` (Linux only) | Linux services |
| `NullHandler` | `logging` | **Inside a library**, so it never emits by default | requests, urllib3, boto3 |
| `QueueHandler` / `QueueListener` | `logging.handlers` | Async apps, or any slow/network handler — see `03_` | Home Assistant |
| `SocketHandler` | `logging.handlers` | Multi-process → one collector process | cookbook-recommended for Gunicorn |
| `DatagramHandler` | `logging.handlers` | UDP, fire-and-forget, drops under load | metrics-ish uses |
| `SysLogHandler` | `logging.handlers` | Unix syslog / journald / rsyslog / remote syslog | system daemons |
| `NTEventLogHandler` | `logging.handlers` | Windows Event Log | Windows services |
| `SMTPHandler` | `logging.handlers` | Email on CRITICAL — **always behind a queue** | Django's `AdminEmailHandler` |
| `HTTPHandler` | `logging.handlers` | POST records to a webhook | rarely; prefer a real SDK |
| `MemoryHandler` | `logging.handlers` | Buffer records, flush only when an ERROR happens | "give me the DEBUG lines leading up to the failure" |
| `BufferingHandler` | `logging.handlers` | Base class for your own buffering logic | — |
| `logging.NullHandler` | `logging` | see above | — |

Third-party sinks you'd normally use instead of hand-rolling:
`rich.logging.RichHandler` (pretty CLI — pip uses it),
`sentry_sdk` `LoggingIntegration`, `opentelemetry-sdk` `LoggingHandler`,
`watchtower` (CloudWatch), `python-json-logger` (formatter, not handler).

---

## The ones you'll actually use

### `StreamHandler` — the default answer

```python
import sys, logging

h = logging.StreamHandler(sys.stdout)     # default is sys.STDERR, note that
h.setLevel(logging.INFO)
h.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(name)s — %(message)s"))
logging.getLogger().addHandler(h)
```

- **Default stream is `sys.stderr`, not stdout.** Bites people who pipe stdout somewhere.
- Convention: diagnostics → stderr, structured/access output → stdout. uvicorn splits
  exactly this way.
- In dictConfig: `"stream": "ext://sys.stdout"`.
- It does **not** own the stream — closing the handler does not close `sys.stdout`.

### `RotatingFileHandler` — size-based

```python
from logging.handlers import RotatingFileHandler

h = RotatingFileHandler(
    "app.log",
    maxBytes=10 * 1024 * 1024,   # 10 MB
    backupCount=5,               # app.log, app.log.1 ... app.log.5
    encoding="utf-8",            # ALWAYS set this on Windows
    delay=False,                 # True = don't open the file until the first record
)
```

- Total disk = `maxBytes * (backupCount + 1)`. Budget it deliberately.
- `backupCount=0` means **truncate on rollover, keep nothing**. Almost never what you want.
- **`encoding="utf-8"` is not optional on Windows.** Without it Python uses the ANSI code
  page (cp1252), and the first non-Latin-1 character raises
  `UnicodeEncodeError: 'charmap' codec can't encode character`. On Python 3.15 the default
  becomes UTF-8, but be explicit anyway.
- It does **not create the directory**. `mkdir` first, or subclass `_open()` — pip's
  `BetterRotatingFileHandler` exists purely for this.
- **Not safe across processes.** Two workers rotating the same file will destroy data.

### `TimedRotatingFileHandler` — time-based

```python
from logging.handlers import TimedRotatingFileHandler

h = TimedRotatingFileHandler(
    "app.log",
    when="midnight",      # 'S','M','H','D','W0'-'W6','midnight'
    interval=1,
    backupCount=14,       # keep 14 days
    encoding="utf-8",
    utc=True,             # use UTC for the rollover boundary — do this on servers
    atTime=None,
)
```

- `backupCount` here means **number of files**, i.e. retention period. This is the one
  people reach for when the requirement is phrased in days ("keep 30 days of logs").
- `utc=True` avoids two rollovers (or zero) on DST changeover days.
- Same multi-process warning.

### `WatchedFileHandler` — when Linux `logrotate` owns the file

```python
from logging.handlers import WatchedFileHandler
h = WatchedFileHandler("/var/log/myapp/app.log", encoding="utf-8")
```

The problem it solves: `logrotate` renames `app.log` → `app.log.1`. Your process still holds
the **old inode** and keeps writing into a file nobody can see; disk fills, log looks dead.
`WatchedFileHandler` checks the inode before each write and reopens if it changed.

**Rule: on Linux, either Python rotates (`RotatingFileHandler`) or logrotate rotates
(`WatchedFileHandler`). Never both.** Windows can't rename open files, so this handler is
Unix-only in practice.

### `NullHandler` — the library rule

```python
# mypackage/__init__.py
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
```

Put this in every library you publish. It prevents the
"No handlers could be found for logger X" fallback and guarantees your library is silent
unless the application opts in.

### `MemoryHandler` — the underrated one

"Give me the last 100 DEBUG lines, but only when something actually fails."

```python
from logging.handlers import MemoryHandler

target = logging.FileHandler("incidents.log", encoding="utf-8")
mem = MemoryHandler(
    capacity=100,                    # ring size
    flushLevel=logging.ERROR,        # flush everything buffered when an ERROR arrives
    target=target,
    flushOnClose=False,              # don't dump the buffer on a clean exit
)
logging.getLogger().addHandler(mem)
logging.getLogger().setLevel(logging.DEBUG)
```

Now you run at DEBUG with near-zero disk cost, and you get full context around every failure.
This is the pattern to use when "we can't reproduce it, and DEBUG in prod is too expensive".

### `SysLogHandler`

```python
from logging.handlers import SysLogHandler

h = SysLogHandler(address="/dev/log", facility=SysLogHandler.LOG_DAEMON)   # local
h = SysLogHandler(address=("logs.example.com", 514))                       # remote UDP
h.setFormatter(logging.Formatter("myapp[%(process)d]: %(message)s"))
```

- `/dev/log` on Linux, `/var/run/syslog` on macOS. Doesn't exist on Windows.
- UDP syslog silently drops messages under load. Use TCP
  (`socktype=socket.SOCK_STREAM`) if delivery matters.
- syslog truncates long lines (often ~1KB). Bad fit for JSON payloads or tracebacks.

### `SMTPHandler` — and why Django wrapped it

```python
from logging.handlers import SMTPHandler

h = SMTPHandler(
    mailhost=("smtp.example.com", 587),
    fromaddr="alerts@example.com",
    toaddrs=["oncall@example.com"],
    subject="[PROD] CRITICAL",
    credentials=("user", "pass"),
    secure=(),
)
h.setLevel(logging.CRITICAL)
```

Three things will hurt you:

1. **It blocks.** An SMTP round trip on your request path / event loop. Put it behind a
   `QueueHandler` — this is the textbook justification for the pattern.
2. **No rate limiting.** A failing loop at ERROR sends 10,000 emails and gets your domain
   blacklisted. Django's `AdminEmailHandler` adds throttling on top for this reason.
3. Modern equivalent: don't. Send ERROR to Sentry / PagerDuty / Slack via their SDK, and let
   the alerting system do dedup and escalation.

### `SocketHandler` — the multi-process answer

Every worker process sends pickled `LogRecord`s over TCP to one collector process, which
owns the single file:

```python
h = logging.handlers.SocketHandler("127.0.0.1", logging.handlers.DEFAULT_TCP_LOGGING_PORT)
```

This is what the official cookbook recommends for Gunicorn/uWSGI. ⚠️ It pickles records, so
**never expose that port outside localhost** — unpickling untrusted data is remote code
execution. The cookbook's own receiver example carries this warning.

### `QueueHandler` / `QueueListener`

Covered fully in **`03_queuehandler_verdict.md`**.

---

## Choosing a sink by deployment target

| Deployment | Sink |
|---|---|
| Docker / Kubernetes / ECS / Cloud Run | `StreamHandler` → **stdout**, JSON format. Nothing else. |
| systemd unit on a VM | `StreamHandler` → stdout; journald captures it. `journalctl -u myapp`. |
| VM without a collector | `TimedRotatingFileHandler`, `backupCount` = retention days |
| Linux with logrotate already configured | `WatchedFileHandler` |
| Desktop app / CLI | `RotatingFileHandler` in the user data dir + `RichHandler` on console |
| AWS Lambda | `StreamHandler` (CloudWatch captures stdout automatically) |
| Multi-process on one box, one file required | `SocketHandler` → collector, or per-process files |
| Anything needing alerting | Sentry/OTel SDK, **not** `SMTPHandler` |

---

Next: **`05_config_patterns.md`** — how to wire these up without hand-writing 40 lines.
