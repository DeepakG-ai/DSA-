r"""
ex06 — correlation IDs: contextvars + a Filter.

The problem: with concurrent requests, log lines interleave and you cannot tell
which line belongs to which request. The fix is one ID on every line, injected
without passing it through every function signature.

Run:  .\.venv\Scripts\python.exe docs\logging_notes\examples\ex06_context_filter.py
"""
import asyncio
import contextvars
import logging
import sys
import uuid

# ─── the context variable ─────────────────────────────────────────────────────
# contextvars, NOT threading.local: in asyncio many coroutines share one thread,
# so thread-local storage would give them all the same value.
request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="-")
user_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("user_id", default="-")


# ─── the filter: returns True always; it exists for the SIDE EFFECT ───────────
class ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get()
        record.user_id = user_id_var.get()
        return True


def configure():
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(logging.Formatter(
        "%(asctime)s.%(msecs)03d %(levelname)-5s [%(request_id)s u=%(user_id)-4s] "
        "%(name)-18s — %(message)s",
        datefmt="%H:%M:%S",
    ))
    # On the HANDLER, not the logger: this way it also stamps records from
    # third-party libraries, which propagate to root but never touch your loggers.
    h.addFilter(ContextFilter())
    root.addHandler(h)
    root.setLevel(logging.INFO)


# ─── application code — note it knows NOTHING about request ids ───────────────
db_log = logging.getLogger("app.db")
ocr_log = logging.getLogger("app.ocr")


async def query_db(table):
    db_log.info("SELECT * FROM %s", table)
    await asyncio.sleep(0.01)


async def run_ocr(pages):
    ocr_log.info("ocr start pages=%d", pages)
    await asyncio.sleep(0.02)
    ocr_log.info("ocr done")


# ─── the middleware: the ONLY place that touches the contextvar ───────────────
async def handle_request(user: str, pages: int):
    rid = uuid.uuid4().hex[:8]
    token_r = request_id_var.set(rid)
    token_u = user_id_var.set(user)
    try:
        logging.getLogger("app.http").info("request received pages=%d", pages)
        await query_db("invoices")
        await run_ocr(pages)
        logging.getLogger("app.http").info("request complete")
    finally:
        # ALWAYS reset with the token. Without it the value leaks into whatever
        # runs next on this task/thread.
        request_id_var.reset(token_r)
        user_id_var.reset(token_u)


async def main():
    configure()

    print("=" * 78)
    print("Three concurrent requests. Lines interleave — but each carries its own id.")
    print("=" * 78)
    await asyncio.gather(
        handle_request("alice", 3),
        handle_request("bob", 5),
        handle_request("carol", 2),
    )

    print()
    print("=" * 78)
    print("Third-party libraries get stamped too (the filter is on the HANDLER)")
    print("=" * 78)
    request_id_var.set("outside")
    logging.getLogger("urllib3.connectionpool").info("Starting new HTTPS connection")

    print()
    print("=" * 78)
    print("Alternative: setLogRecordFactory — stamps at record CREATION")
    print("=" * 78)
    print("""
    _old = logging.getLogRecordFactory()
    def factory(*args, **kwargs):
        record = _old(*args, **kwargs)
        record.request_id = request_id_var.get()
        return record
    logging.setLogRecordFactory(factory)

    Runs in the originating thread BY CONSTRUCTION, so it also works correctly
    under a QueueListener (see ex05 Part 4). Downside: it's process-global, so
    only the application may do it — never a library.

    Also note: Formatter(..., defaults={"request_id": "-"}) (Python 3.10+) gives
    a fallback so a record that missed the filter doesn't raise at format time.

    structlog does all of this with bind_contextvars(). loguru does it with
    logger.contextualize(). Same mechanism underneath — contextvars.
    """)


if __name__ == "__main__":
    asyncio.run(main())
