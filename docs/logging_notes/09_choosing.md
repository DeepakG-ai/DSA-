# 09 — Choosing: scenario → library

---

## The one-line answer

> **Use stdlib `logging` as the foundation, always. Add `structlog` on top when you need
> structured JSON at scale. Use `loguru` when you own the whole program and want to stop
> thinking about logging.**

Note what that sentence does *not* say: it does not say "pick one of three". stdlib is not
optional — every dependency you install logs through it. The real question is only ever
*"what, if anything, do I put on top?"*

---

## Decision table

| Scenario | Use | Why |
|---|---|---|
| A script you'll run twice | `logging.basicConfig()` | 3 lines, done |
| Jupyter notebook / analysis | `basicConfig(force=True)` or loguru | `force=True` beats the notebook's existing config |
| CLI tool you're publishing | stdlib + `RichHandler` | pip's model; no dependency forced on users of your *library* API |
| **A library on PyPI** | **stdlib + `NullHandler`. Nothing else. Ever.** | You must not impose config or a dependency on your users |
| Personal automation / data pipeline | **loguru** | rotation + retention + JSON in 4 lines |
| ML training loop / research code | **loguru** | best tracebacks, `logger.catch`, zero setup |
| Django app | stdlib `dictConfig` via `settings.LOGGING` | Django already owns the config path |
| FastAPI/Flask service in a container | stdlib `dictConfig` → **stdout JSON** | 12-Factor; matches uvicorn |
| Same, but many services + a log platform | **structlog** over stdlib | `bind_contextvars`, queryable fields, keeps stdlib handlers |
| Microservices with distributed tracing | structlog + OpenTelemetry | OTel hooks stdlib; structlog renders |
| Desktop app (Home Assistant shaped) | stdlib + `TimedRotatingFileHandler` (+ QueueHandler if async) | files are correct here |
| Multi-process workers (Gunicorn/Celery) | stdlib → **stdout per process**, or `SocketHandler` → collector | file rotation across processes is unsupported |
| Anything async with **file or network** handlers | stdlib + `QueueHandler`/`QueueListener` (or loguru `enqueue=True`) | keeps blocking I/O off the event loop — see `03_` |
| You must not lose a record (billing/audit) | **a database**, not logs | logs have no durability guarantee |

---

## Head to head

| | stdlib `logging` | loguru | structlog |
|---|---|---|---|
| Install | built in | `pip install loguru` | `pip install structlog` |
| Lines to useful output | ~1 (`basicConfig`) / ~30 (real config) | 0 | ~3 (defaults are good) |
| Lines to production JSON + rotation | ~40 | ~4 | ~15 |
| Third-party library logs | **native** | needs `InterceptHandler` (~20 lines) | **native** |
| Structured output | manual formatter | `serialize=True` | **the entire point** |
| Request-scoped context | contextvars + Filter (manual) | `logger.contextualize()` | `bind_contextvars()` |
| Config from a file, no code change | **yes** (dictConfig from JSON/YAML) | awkward | yes (via stdlib layer) |
| Non-blocking / async-safe | `QueueHandler` | `enqueue=True` | inherits stdlib's |
| Multi-process safe file writes | no (use socket/stdout) | **yes** (`enqueue=True`) | inherits stdlib's |
| Traceback quality | plain | **best** | good (`dict_tracebacks` = structured) |
| APM/OTel/Sentry integration | **native** | via handler-as-sink | **native** |
| Safe in a published library | **yes** | **no** | no (it's a dependency) |
| Learning curve | medium, unavoidable | tiny | steep |

---

## Migration paths

**stdlib → structlog**: incremental and safe. Configure structlog with
`ProcessorFormatter`, keep all your existing handlers, and convert call sites one module
at a time. Both styles coexist and render identically. This is the reason structlog is the
low-risk choice.

**stdlib → loguru**: add `InterceptHandler`, then convert call sites. Reversible, but the
call sites differ (`logger.bind()`, `logger.opt()`), so a full round trip is work.

**loguru → stdlib**: hardest direction. Budget for it if you're choosing loguru for
something that might become a shared service.

---

## What I'd actually do for a Python backend service

1. stdlib `logging` as the base. `dictConfig`, once, at startup, `disable_existing_loggers: False`.
2. Every module: `logger = logging.getLogger(__name__)`.
3. One handler: `StreamHandler` → **stdout**. Let the platform collect it.
4. `JsonFormatter` in prod, human-readable in dev (branch on `sys.stderr.isatty()`).
5. Correlation IDs via `contextvars` + a `Filter` on the handler.
6. A redaction `Filter`, so secrets can't leak from a careless call site.
7. Level from `LOG_LEVEL` env var; per-logger overrides from `LOG_LEVELS`.
8. Quiet the usual noisy libraries (`urllib3`, `botocore`, `sqlalchemy.engine`).
9. **Skip `QueueHandler`** unless you're async *and* have a file/network handler, or you've
   measured latency from logging. Then add it — via `dictConfig` on 3.12+, and remember
   `listener.stop()` on shutdown.
10. Add structlog **when** the log platform arrives and you want real queryable fields.
    Not before.

Steps 1–8 are maybe 50 lines total and cover the overwhelming majority of real services.
That is what "industry standard" looks like in practice — not clever, just consistent.

---

## Sources

- [Configuring Logging for a Library — Python docs](https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library)
- [Logging Cookbook — Python docs](https://docs.python.org/3/howto/logging-cookbook.html)
- [The Twelve-Factor App — Logs](https://12factor.net/logs)
- [Logging in Python: A Comparison of the Top 6 Libraries — Better Stack](https://betterstack.com/community/guides/logging/best-python-logging-libraries/)
- [5 Best Python Logging Libraries in 2026 — Dash0](https://www.dash0.com/guides/python-logging-libraries)
- [Loguru vs Structlog: When to Use Which — Vijay, Medium](https://viju-londhe.medium.com/loguru-vs-structlog-when-to-use-which-fe1e9d6c3933)
- [Python logging: basic, better and best — Matthew Strawbridge](https://www.matthewstrawbridge.com/content/2024/python-logging-basic-better-best/)
