# 03 — Is `QueueHandler` a good idea, or bad AI advice?

You suspected `QueueHandler` might be a hallucinated over-engineering suggestion.
Here is the honest answer, with receipts.

---

## Verdict

**`QueueHandler` + `QueueListener` is a legitimate, officially documented, industry-standard
pattern. It is not made-up advice.** But it is a *conditional* recommendation — it solves
one specific problem, and if you don't have that problem it is pure added complexity.

Three independent pieces of evidence:

**1. It is in the official Python Logging Cookbook**, under "Dealing with handlers that
block":

> "One solution is to use a two-part approach. For the first part, attach only a
> `QueueHandler` to those loggers which are accessed from performance-critical threads.
> They simply write to their queue... The second part of the solution is `QueueListener`,
> which has been designed as the counterpart to `QueueHandler`."

And specifically for async code:

> "when logging from async code, network and even file handlers could lead to problems
> (blocking the event loop) because some logging is done from `asyncio` internals. **It
> might be best, if any async code is used in an application, to use the above approach for
> logging, so that any blocking code runs only in the `QueueListener` thread.**"

That is the CPython docs recommending it for any application using async code.

**2. Home Assistant — one of the largest async Python codebases in existence — ships it.**
`homeassistant/util/logging.py` defines `HomeAssistantQueueHandler(logging.handlers.QueueHandler)`
and `HomeAssistantQueueListener(logging.handlers.QueueListener)`, activated by
`async_activate_log_queue_handler()`, whose docstring says:

> "Migrate the existing log handlers to use the queue. This allows us to avoid blocking I/O
> and formatting messages in the event loop as log messages are written in another thread."

**3. Python 3.12 gave it first-class `dictConfig` support.** The core devs added
`QueueHandler`/`QueueListener` configuration directly to `logging.config.dictConfig()`.
Language maintainers don't wire config syntax for patterns they consider mistakes.
Python 3.14 additionally made `QueueListener` usable as a context manager.

---

## What problem it actually solves

`logging` does **blocking I/O** inside `Handler.emit()`. `logging.FileHandler.emit()` calls
`stream.write()` then `stream.flush()` — a real syscall. `SMTPHandler` opens an SMTP
connection. `HTTPHandler` makes an HTTP request. A CloudWatch handler makes an AWS API call.

In a **synchronous** program this just makes that one thread slower. Fine.

In an **asyncio** program there is only one thread running all your coroutines. A blocking
`write()` + `flush()` on a slow or contended disk stalls **every** in-flight request, not
just the one that logged. A `SMTPHandler` on the event loop can freeze the entire service
for seconds.

`QueueHandler` replaces that with `queue.put_nowait()` — an in-memory append with no syscall.
A background thread (`QueueListener`) does the formatting and the actual I/O.

So the decision rule is:

| Your situation | Do you need QueueHandler? |
|---|---|
| Sync script / CLI | **No.** Pointless complexity. |
| Sync web app (Django + Gunicorn sync workers), logging to stdout | **No.** stdout writes are fast and each worker has its own thread. |
| Any handler that does **network** I/O (HTTP, SMTP, CloudWatch, Elasticsearch, Sentry-as-handler) | **Yes.** Non-negotiable. |
| **asyncio** app (FastAPI/Starlette/aiohttp) writing to **files** | **Yes** — this is the documented case, and what Home Assistant does. |
| asyncio app writing only to **stdout**, container captures it | **Borderline.** Usually fine without it. Add it if you measure latency spikes. |
| Multi-**process** (Gunicorn workers, Celery prefork) writing to one file | Queue helps, but the *better* answer is one stdout stream per process — see below. |

---

## So was the advice wrong for you?

Only you can score this, but here is the test. Answer these:

1. **Is the app asyncio-based?** If yes, and you write to files, the pattern is correct
   and matches Home Assistant and the CPython docs.
2. **Do you have more than one process writing the same log file?** If yes, `QueueHandler`
   with a plain `queue.Queue` **does not help you at all** — an in-process queue is per
   process. You'd need `multiprocessing.Queue` plus a single listener process, or, far
   better, separate files/streams per process.
3. **Are your handlers actually slow?** If every handler is a `StreamHandler` to stdout in a
   container, the queue buys you very little and costs you a thread, a shutdown hook, and a
   class of bugs listed below.

**Where AI-generated logging setups genuinely tend to go wrong** — check for these, they're
more likely to be your real problem than the queue itself:

- A handler on the listener side that reads `contextvars`. **Contextvars do not cross the
  thread boundary.** The record is created in your thread but formatted in the listener
  thread, where the contextvar is empty. The fix is to stamp context onto the record with a
  `Filter` on the `QueueHandler` (originating thread), *not* on the downstream handlers.
  If a setup gets this backwards, correlation IDs silently come out blank.
- **No `listener.stop()` on shutdown** → records sitting in the queue at SIGTERM are lost.
  You need it in the FastAPI `lifespan` shutdown / `atexit`.
- **Double-logging**: leaving the original handlers on root *and* adding the QueueHandler
  that feeds the same handlers → every line twice.
- **Unbounded queue** (`Queue(-1)`): if the listener thread dies or the disk hangs, the
  queue grows until the process OOMs. Unbounded is the cookbook default and is usually
  right, but know the tradeoff.
- **Rotation from multiple processes** behind queues — still broken, queue or no queue.
- Building a queue setup by hand when you're on Python 3.12+, where `dictConfig` does it
  in six lines.

---

## The modern way to write it (Python 3.12+)

Before 3.12 you had to wire it manually. Now `dictConfig` does it:

```python
import logging.config

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "std": {"format": "%(asctime)s %(levelname)-8s %(name)s — %(message)s"},
    },
    "handlers": {
        # the real sinks — note: NOT attached to any logger
        "console": {"class": "logging.StreamHandler", "formatter": "std"},
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app.log",
            "maxBytes": 10_000_000,
            "backupCount": 5,
            "encoding": "utf-8",
            "formatter": "std",
        },
        # the queue front-end — this is what loggers actually use
        "queue": {
            "class": "logging.handlers.QueueHandler",
            "handlers": ["console", "file"],       # <- listener gets these
            "respect_handler_level": True,
            # "queue": "ext://myapp.log_queue"     # optional; omit for an auto queue.Queue
        },
    },
    "root": {"handlers": ["queue"], "level": "INFO"},
})
```

Key points:

- `dictConfig` creates the `QueueListener` for you and puts it on the handler as
  `.listener`. **You still have to start and stop it:**

  ```python
  qh = logging.getHandlerByName("queue")      # Python 3.12+
  qh.listener.start()
  ...
  qh.listener.stop()      # drains the queue — do this on shutdown
  ```

  (In 3.14 you can also use it as a context manager: `with qh.listener: ...`)
- `respect_handler_level=True` makes the listener honour each downstream handler's own
  level. **Default is `False`**, which means every record goes to every handler regardless
  of level — a classic surprise where `error.log` fills up with INFO lines.
- `handlers` listed under the queue handler are **moved** to the listener; they are not
  attached to any logger. Don't also list them under `root` or you get duplicates.

### FastAPI / lifespan wiring

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()                 # dictConfig + listener.start()
    yield
    shutdown_logging()                  # listener.stop() + logging.shutdown()

app = FastAPI(lifespan=lifespan)
```

Without the shutdown half, a container receiving SIGTERM drops whatever is still queued.

---

## The simpler alternative you should seriously consider first

Before reaching for a queue, ask whether you need file handlers at all.

```python
# The whole thing, for a containerized service:
logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"json": {"()": "myapp.log.JsonFormatter"}},
    "handlers": {"stdout": {"class": "logging.StreamHandler",
                            "stream": "ext://sys.stdout",
                            "formatter": "json"}},
    "root": {"handlers": ["stdout"], "level": os.getenv("LOG_LEVEL", "INFO")},
})
```

No queue, no listener, no thread, no shutdown hook, no rotation, no lost records, and it
works identically under 1 process or 50. The platform (Docker/k8s/ECS/systemd) does
collection, and stdout writes to a pipe are fast enough that the event-loop concern
mostly evaporates.

This is what uvicorn does. It is what most modern services do. **Reach for `QueueHandler`
when you have measured a problem, or when a handler genuinely does network I/O.**

---

## Sources

- [Logging Cookbook — "Dealing with handlers that block" — Python docs](https://docs.python.org/3/howto/logging-cookbook.html#dealing-with-handlers-that-block)
- [`logging.handlers` — QueueHandler / QueueListener — Python 3.14 docs](https://docs.python.org/3/library/logging.handlers.html#queuehandler)
- [`logging.config` — dictConfig QueueHandler support — Python 3.14 docs](https://docs.python.org/3/library/logging.config.html)
- [dictConfig support for QueueHandler/QueueListener — discuss.python.org](https://discuss.python.org/t/a-new-feature-is-being-added-in-logging-config-dictconfig-to-configure-queuehandler-and-queuelistener/16124)
- [Home Assistant `homeassistant/util/logging.py`](https://github.com/home-assistant/core/blob/dev/homeassistant/util/logging.py)
- [Logging in asyncio applications — Martijn Pieters](https://www.zopatista.com/python/2019/05/11/asyncio-logging/)
- [How to use Python logging QueueHandler with dictConfig in Python 3.12 — Rob Blackbourn](https://rob-blackbourn.medium.com/how-to-use-python-logging-queuehandler-with-dictconfig-in-python-3-12-3bbef42c5e20)
