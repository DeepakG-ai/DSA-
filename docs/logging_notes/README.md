# Logging — full reference

Everything about Python logging: the official `logging` stdlib module (the important one),
plus `loguru` and `structlog`, with **which one in which scenario** — grounded in what real
open-source projects actually ship, not in opinion.

---

## ⚠️ First: why this folder is NOT called `logging`

You were right to worry. Here is the exact failure.

Python 3 has **implicit namespace packages** (PEP 420). A *directory* with no `__init__.py`
is still importable as a package. And `sys.path[0]` is the directory of the script you ran.

So if you had done this:

```
docs/
  logging/          <-- folder named "logging"
    notes.md
  demo.py           <-- you run: python demo.py
```

and `demo.py` says `import logging`, Python searches `sys.path` **in order**:

1. `docs/`  (because `demo.py` lives there)  → finds the folder `logging/` → **wins**
2. stdlib   → never reached

Result: `logging` is now an empty namespace package. Every real call explodes:

```
AttributeError: module 'logging' has no attribute 'getLogger'
```

And it is a *confusing* error, because the module "imported fine". The same trap kills people
who name a file `logging.py`, `json.py`, `random.py`, `email.py`, `queue.py`, `types.py`,
`select.py`, `token.py`, `copy.py`, `string.py`, `test.py`, `secrets.py`.

This is a known enough hazard that projects call it out in their own source. Django's
logging module is `django/utils/log.py`, not `logging.py`. Flask's is `flask/logging.py`
only because it's inside a package that's always imported as `flask.logging`.

**Rule to memorise:** never name a file or folder after a stdlib module. When in doubt:

```python
import logging
print(logging.__file__)
# GOOD: C:\...\Python314\Lib\logging\__init__.py
# BAD:  C:\Users\deepa\Projects\...\docs\logging\__init__.py   (or no __file__ at all)
```

That is why this folder is `logging_notes/`.

---

## Read in this order

| # | File | What it covers |
|---|------|----------------|
| — | **`QUICKSTART.md`** | **Start here.** A read-once intro covering the whole topic end to end (from Perplexity / Claude Sonnet 5). Corrections appended at the bottom. |
| 00 | `00_mental_model.md` | The 5 objects and the pipeline. Read first — everything assumes it. |
| 01 | `01_stdlib_core.md` | Levels, `getLogger`, propagation, `LogRecord`, formatters, filters, adapters |
| **02** | **`02_open_source_survey.md`** | **How Django / uvicorn / Flask / pip / Airflow / Home Assistant actually do it. Is logging centralized? (Yes — and why.)** |
| **03** | **`03_queuehandler_verdict.md`** | **Is `QueueHandler` good advice or over-engineering? Honest answer with receipts.** |
| 04 | `04_handlers_scenarios.md` | Every handler + the scenario it exists for. The lookup table. |
| 05 | `05_config_patterns.md` | `basicConfig` / `dictConfig`, correlation IDs, JSON, redaction, env-driven levels |
| 06 | `06_pitfalls.md` | The 22 mistakes that actually bite in production |
| 07 | `07_loguru.md` | loguru: API, sinks, rotation, and its one real weakness |
| 08 | `08_structlog.md` | structlog: processors, `bind()`, contextvars, stdlib interop |
| 09 | `09_choosing.md` | Decision matrix. Scenario → library. What I'd actually build. |

If you only read two: **02** and **03**.

## Runnable examples

All nine run standalone and are **verified working** on this machine (Python 3.14.6).
From the repo root:

```powershell
.\.venv\Scripts\python.exe docs\logging_notes\examples\ex01_basic_config.py
```

| File | Shows |
|------|-------|
| `ex01_basic_config.py` | `basicConfig`, levels, lazy `%s` vs f-strings (proven), `exception()`, `stack_info` |
| `ex02_hierarchy.py` | Logger tree, lazy `PlaceHolder` parents, propagation, the duplicate-line bug + 3 fixes |
| `ex03_dictconfig.py` | Production `dictConfig` — filters that drop, filters that stamp, `defaults=`, `ext://` |
| `ex04_rotation.py` | `RotatingFileHandler` vs `TimedRotatingFileHandler` rolling over live |
| `ex05_queue_async.py` | **Measures** an event-loop stall, fixes it with `QueueHandler`, then the 3.12 `dictConfig` way, then the 2 classic bugs |
| `ex06_context_filter.py` | `contextvars` + `Filter` → correlation IDs across 3 interleaved async requests |
| `ex07_json_logs.py` | Structured JSON with **zero dependencies** |
| `ex08_loguru_demo.py` | loguru: 3 sinks in 20 lines, `bind`, `contextualize`, `@catch`, and the InterceptHandler tax |
| `ex09_structlog_demo.py` | structlog processors, `bind_contextvars`, and the `ProcessorFormatter` stdlib bridge |

`loguru` (0.7.3) and `structlog` (26.1.0) are installed in `.venv`, so ex08 and ex09 run.
They skip with a clear message if the library is ever missing.

Output files land in `examples/_out/` (gitignored).

---

## The 30-second summary

**Is logging centralized in real projects?** Yes, universally, and the rule has two halves:

> **Libraries never configure logging — they do `getLogger(__name__)` + `NullHandler` and
> nothing else. Applications configure it once, centrally, at startup, with `dictConfig()`.**

Django, uvicorn, pip, Airflow, and Celery all call `logging.config.dictConfig()` exactly
once from the entry point. `requests`, `urllib3`, `boto3`, and `httpx` all ship a
`NullHandler` and never touch config.

**Which library?**

- **`logging` (stdlib)** — always available, zero dependencies, every package on PyPI
  already logs through it. Verbose to configure. **This is the one that matters.**
- **`loguru`** — one import, no config, rotation/retention/compression/JSON built in.
  Great for scripts and CLIs. Needs a 20-line `InterceptHandler` to control third-party
  library logs, and must never be a dependency of a published library.
- **`structlog`** — key-value events instead of sentences, `bind()` for context, designed
  for JSON going into Datadog/Loki/CloudWatch. Steepest curve, best for large services.

structlog sits **on top of** stdlib and keeps the whole ecosystem (dictConfig, QueueHandler,
Sentry, OpenTelemetry). loguru largely replaces it. That single fact decides most real
architecture arguments.

**And the container rule that overrides most of the above:** if you deploy in Docker/k8s/ECS,
write JSON to **stdout** and stop. No file handlers, no rotation, no log shipping in-process.
The platform collects it. That's 12-Factor, and it's what uvicorn does.

---

## Sources

Primary source code read for `02_open_source_survey.md`:

- [Django `django/utils/log.py`](https://github.com/django/django/blob/main/django/utils/log.py)
- [uvicorn `uvicorn/config.py`](https://github.com/encode/uvicorn/blob/master/uvicorn/config.py)
- [Flask `src/flask/logging.py`](https://github.com/pallets/flask/blob/main/src/flask/logging.py)
- [pip `src/pip/_internal/utils/logging.py`](https://github.com/pypa/pip/blob/main/src/pip/_internal/utils/logging.py)
- [Airflow `airflow_local_settings.py`](https://github.com/apache/airflow/blob/main/airflow-core/src/airflow/config_templates/airflow_local_settings.py)
- [Home Assistant `homeassistant/util/logging.py`](https://github.com/home-assistant/core/blob/dev/homeassistant/util/logging.py)

Official docs:

- [logging — Python 3.14](https://docs.python.org/3/library/logging.html)
- [logging.handlers — Python 3.14](https://docs.python.org/3/library/logging.handlers.html)
- [logging.config — Python 3.14](https://docs.python.org/3/library/logging.config.html)
- [Logging Cookbook — Python 3.14](https://docs.python.org/3/howto/logging-cookbook.html)
- [Configuring Logging for a Library](https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library)
- [dictConfig QueueHandler/QueueListener support (3.12) — discuss.python.org](https://discuss.python.org/t/a-new-feature-is-being-added-in-logging-config-dictconfig-to-configure-queuehandler-and-queuelistener/16124)
- [loguru docs](https://loguru.readthedocs.io/en/stable/) · [structlog docs](https://www.structlog.org/en/stable/)
- [The Twelve-Factor App — Logs](https://12factor.net/logs)

Commentary:

- [Logging in asyncio applications — Martijn Pieters](https://www.zopatista.com/python/2019/05/11/asyncio-logging/)
- [Python Logging Config: dictConfig, QueueHandler & Thread Safety — Uptrace](https://uptrace.dev/blog/python-logging)
- [Logging in Python: A Comparison of the Top 6 Libraries — Better Stack](https://betterstack.com/community/guides/logging/best-python-logging-libraries/)
- [5 Best Python Logging Libraries in 2026 — Dash0](https://www.dash0.com/guides/python-logging-libraries)
- [Leveling Up Your Python Logs with Structlog — Dash0](https://www.dash0.com/guides/python-logging-with-structlog)
- [Loguru vs Structlog: When to Use Which — Vijay, Medium](https://viju-londhe.medium.com/loguru-vs-structlog-when-to-use-which-fe1e9d6c3933)
- [Python Logging Handlers: Types, Setup, and Best Practices — Toptal](https://www.toptal.com/developers/python/in-depth-python-logging)
