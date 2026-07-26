r"""
ex05 — QueueHandler / QueueListener: what it actually buys you.

Part 1 MEASURES the problem (a slow handler stalling an asyncio event loop).
Part 2 fixes it with QueueHandler and measures again.
Part 3 shows the Python 3.12+ dictConfig way.
Part 4 shows the two bugs people hit.

This is the pattern the official Logging Cookbook recommends for async code, and
the one Home Assistant ships (homeassistant/util/logging.py).

Run:  .\.venv\Scripts\python.exe docs\logging_notes\examples\ex05_queue_async.py
"""
import asyncio
import contextvars
import logging
import logging.config
import logging.handlers
import queue
import sys
import time
from pathlib import Path

OUT = Path(__file__).parent / "_out"
OUT.mkdir(exist_ok=True)


class SlowHandler(logging.Handler):
    """Stands in for a real handler that blocks: SMTP, HTTP, CloudWatch,
    Elasticsearch, or a file handler on a contended disk."""

    def __init__(self, delay=0.02):
        super().__init__()
        self.delay = delay
        self.count = 0

    def emit(self, record):
        try:
            self.format(record)
            time.sleep(self.delay)      # the blocking I/O
            self.count += 1
        except Exception:
            self.handleError(record)    # never let a logging failure kill business code


def clear_root():
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
    root.setLevel(logging.INFO)
    return root


# ════════════════════════════ PART 1 — the problem ════════════════════════════
async def heartbeat(stop_at, ticks):
    """Pretends to be every OTHER request in flight. If the event loop stalls,
    this stops ticking."""
    while time.perf_counter() < stop_at:
        ticks.append(time.perf_counter())
        await asyncio.sleep(0.005)


async def logging_task(n):
    log = logging.getLogger("demo")
    for i in range(n):
        log.info("record %d", i)
        await asyncio.sleep(0)


async def measure(label, n=30):
    ticks = []
    start = time.perf_counter()
    await asyncio.gather(logging_task(n), heartbeat(start + 0.9, ticks))
    gaps = [b - a for a, b in zip(ticks, ticks[1:])]
    worst = max(gaps) if gaps else 0.0
    print(f"   {label:24} heartbeat ticks={len(ticks):4}   worst stall={worst * 1000:7.1f} ms")
    return worst


async def main():
    print("=" * 72)
    print("PART 1 — a slow handler DIRECTLY on the logger stalls the event loop")
    print("=" * 72)

    root = clear_root()
    slow = SlowHandler(delay=0.02)
    root.addHandler(slow)
    await measure("blocking handler:")

    print("""
   30 records x 20ms = 600ms of blocking sleep, all on the event loop thread.
   The heartbeat barely ticks. In a real server that is EVERY in-flight request
   waiting on your log writes.
""")

    # ═══════════════════════ PART 2 — the fix ═════════════════════════════════
    print("=" * 72)
    print("PART 2 — same handler, behind a QueueHandler")
    print("=" * 72)

    root = clear_root()
    slow2 = SlowHandler(delay=0.02)

    log_queue: queue.Queue = queue.Queue(-1)          # -1 = unbounded (cookbook default)
    qh = logging.handlers.QueueHandler(log_queue)     # put_nowait() — no syscall, no blocking
    listener = logging.handlers.QueueListener(
        log_queue,
        slow2,
        respect_handler_level=True,   # DEFAULT IS False! Then every handler sees every
                                      # record regardless of its own level. Set it True.
    )
    listener.start()                  # spawns the background thread
    root.addHandler(qh)

    await measure("queued handler:")

    listener.stop()                   # DRAINS the queue, then joins the thread.
                                      # Skip this and you lose queued records on exit.

    print(f"""
   The event loop never touched the 20ms sleeps — the listener thread did.
   Records actually written: {slow2.count}/30 (listener.stop() drained the rest).

   THAT is the entire value of QueueHandler. Nothing more, nothing less.
""")

    # ══════════════════ PART 3 — the Python 3.12+ way ═════════════════════════
    print("=" * 72)
    print("PART 3 — dictConfig does all of that for you (Python 3.12+)")
    print("=" * 72)

    if sys.version_info < (3, 12):
        print(f"   Skipped — you are on {sys.version_info.major}.{sys.version_info.minor}, "
              "wire it manually as in Part 2.")
    else:
        logging.config.dictConfig({
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"std": {"format": "%(asctime)s %(levelname)-8s %(name)s — %(message)s"}},
            "handlers": {
                # The REAL sinks. Note they are NOT listed under any logger —
                # dictConfig moves them onto the listener. List them in both
                # places and you get every line twice.
                "console": {"class": "logging.StreamHandler",
                            "stream": "ext://sys.stdout", "formatter": "std"},
                "file": {"class": "logging.handlers.RotatingFileHandler",
                         "filename": str(OUT / "queued.log"),
                         "maxBytes": 1_000_000, "backupCount": 2,
                         "encoding": "utf-8", "formatter": "std", "level": "ERROR"},
                # The front-end the loggers actually use:
                "queue": {"class": "logging.handlers.QueueHandler",
                          "handlers": ["console", "file"],
                          "respect_handler_level": True},
            },
            "root": {"handlers": ["queue"], "level": "INFO"},
        })

        qh2 = logging.getHandlerByName("queue")       # Python 3.12+
        qh2.listener.start()                          # YOU still start it
        logging.getLogger("dictdemo").info("through the queue, to console only")
        logging.getLogger("dictdemo").error("through the queue, to console AND file")
        qh2.listener.stop()                           # ...and YOU still stop it

        print(f"\n   ERROR-only file → {OUT / 'queued.log'}")
        print("   " + (OUT / "queued.log").read_text(encoding="utf-8").strip())
        print("\n   Six lines of config replaces Part 2's hand-wiring.")
        print("   (Python 3.14 also allows:  with qh2.listener: ...)")

    # ═════════════ PART 4 — the two bugs everyone hits ════════════════════════
    print()
    print("=" * 72)
    print("PART 4 — the two bugs")
    print("=" * 72)

    request_id = contextvars.ContextVar("request_id", default="-")

    class StampRequestId(logging.Filter):
        def filter(self, record):
            record.request_id = request_id.get()
            return True

    root = clear_root()
    seen = []

    class Capture(logging.Handler):
        def emit(self, record):
            seen.append(getattr(record, "request_id", "<missing>"))

    downstream = Capture()
    downstream.addFilter(StampRequestId())        # <-- BUG: runs in the LISTENER thread

    q2: queue.Queue = queue.Queue(-1)
    qh3 = logging.handlers.QueueHandler(q2)
    lis2 = logging.handlers.QueueListener(q2, downstream)
    lis2.start()
    root.addHandler(qh3)

    request_id.set("req-ABC123")
    logging.getLogger("ctx").info("wrong placement")
    lis2.stop()

    print(f"\n   BUG 1 — contextvars in the wrong thread")
    print(f"     filter on the DOWNSTREAM handler  -> request_id = {seen[-1]!r}")

    # correct placement: on the QueueHandler, which runs in the ORIGINATING thread
    root = clear_root()
    seen.clear()
    downstream2 = Capture()
    q3: queue.Queue = queue.Queue(-1)
    qh4 = logging.handlers.QueueHandler(q3)
    qh4.addFilter(StampRequestId())              # <-- CORRECT
    lis3 = logging.handlers.QueueListener(q3, downstream2)
    lis3.start()
    root.addHandler(qh4)

    request_id.set("req-ABC123")
    logging.getLogger("ctx").info("right placement")
    lis3.stop()

    print(f"     filter on the QUEUE handler       -> request_id = {seen[-1]!r}")
    print("""
     Contextvars are read in whichever thread calls filter(). The listener thread
     has none of your context. Stamp BEFORE the record is enqueued.

   BUG 2 — forgetting listener.stop()
     Records sitting in the queue when the process exits are LOST — exactly the
     records you want when investigating why it exited. Wire it into your
     FastAPI lifespan shutdown or atexit:

         @asynccontextmanager
         async def lifespan(app):
             configure_logging()      # dictConfig + listener.start()
             yield
             shutdown_logging()       # listener.stop() + logging.shutdown()

   AND THE REAL QUESTION: do you need any of this?
     - sync script / CLI ............................ no
     - async app writing only to stdout ............. probably not
     - async app writing to FILES ................... yes (the documented case)
     - any handler doing NETWORK I/O ................ yes, non-negotiable
     - multiple PROCESSES, one file ................. no — an in-process
       queue.Queue is per process. Use one stdout stream per process instead.
""")

    clear_root()


if __name__ == "__main__":
    asyncio.run(main())
