r"""
ex09 — structlog: events with fields, plus the stdlib bridge that makes it the
low-risk choice for a real service.

Needs:  pip install structlog     (skips cleanly if missing)
Run:    .\.venv\Scripts\python.exe docs\logging_notes\examples\ex09_structlog_demo.py
"""
import logging
import sys

try:
    import structlog
except ModuleNotFoundError:
    print("structlog is not installed — skipping this example.")
    print("Install it with:  .\\.venv\\Scripts\\python.exe -m pip install structlog")
    raise SystemExit(0)


def banner(text):
    print(f"\n{'=' * 78}\n{text}\n{'=' * 78}")


# ══════════════════ 1. standalone: pretty console, no stdlib ══════════════════
banner("1. Dev config — ConsoleRenderer")

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,          # ALWAYS first
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="%H:%M:%S", utc=False),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.dev.ConsoleRenderer(colors=False),      # the RENDERER goes last
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
    cache_logger_on_first_use=True,
)

log = structlog.get_logger("billing")
log.info("card_charged", user_id=42, amount_cents=999, currency="usd")
log.warning("rate_limited", user_id=42, retry_after_s=30)

print("""
   Compare:
     stdlib   logger.info("charged user 42 for 9.99")     <- a sentence
     structlog log.info("card_charged", user_id=42, ...)  <- an EVENT + FIELDS
""")


# ═══════════════════════ 2. bind(): explicit context ══════════════════════════
banner("2. bind() — returns a NEW logger carrying fields (immutable, safe to pass)")

req_log = log.bind(request_id="req-001", user_id=42)
req_log.info("request_received", path="/invoices")
req_log.info("db_query", table="invoices", ms=12)
req_log.info("request_complete", status=200)

narrow = req_log.unbind("user_id")
narrow.info("after_unbind")


# ═════════════ 3. bind_contextvars(): implicit, the one for servers ═══════════
banner("3. bind_contextvars() — context-local, works in asyncio AND threads")

from structlog.contextvars import bind_contextvars, clear_contextvars, bound_contextvars


def query_db(table):
    structlog.get_logger("app.db").info("select", table=table)   # knows nothing about ids


def handle_request(rid):
    clear_contextvars()                    # ALWAYS clear at the start of a request
    bind_contextvars(request_id=rid, tenant="acme")
    structlog.get_logger("app.http").info("request_received")
    query_db("invoices")                   # <- picks up request_id automatically
    structlog.get_logger("app.http").info("request_complete")


handle_request("req-002")

with bound_contextvars(job_id=7):
    structlog.get_logger("worker").info("job_started")
structlog.get_logger("worker").info("outside_the_block")

clear_contextvars()


# ════════════════════════ 4. production: JSON ═════════════════════════════════
banner("4. Prod config — JSONRenderer (one line change from #1)")

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.dict_tracebacks,     # traceback as STRUCTURED data
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
    cache_logger_on_first_use=False,              # False so we can reconfigure below
)

jlog = structlog.get_logger("billing")
jlog.info("card_charged", user_id=42, amount_cents=999)

try:
    1 / 0
except ZeroDivisionError:
    jlog.exception("charge_failed", user_id=42)

print("""
   dict_tracebacks makes the traceback searchable JSON, not one giant string.

   ⚠️  BUT LOOK AT THAT OUTPUT: it also dumped every LOCAL VARIABLE in the frame.
   In a real app those locals hold passwords, tokens, API keys, and customer PII —
   now written to your log platform and retained for years. This is exactly the
   same hazard as loguru's diagnose=True.

   In production use plain format_exc_info instead:

       structlog.processors.format_exc_info      # safe: message + frames, no locals

   ...or keep dict_tracebacks only in dev.
""")


# ═══════════ 5. THE IMPORTANT PART: the stdlib bridge ═════════════════════════
banner("5. ProcessorFormatter — third-party stdlib logs come out in the SAME format")

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
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,   # MUST be last
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),              # hand off to stdlib
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=False,
)

formatter = structlog.stdlib.ProcessorFormatter(
    # foreign_pre_chain runs ONLY on records that did NOT come from structlog,
    # i.e. uvicorn / SQLAlchemy / boto3 / your own legacy logging.getLogger() calls
    foreign_pre_chain=[
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
for h in list(root.handlers):
    root.removeHandler(h)
root.addHandler(handler)
root.setLevel(logging.INFO)

print("\n   -- from structlog --")
structlog.get_logger("app").info("structlog_event", user_id=42)

print("\n   -- from PLAIN STDLIB logging (pretend this is uvicorn) --")
logging.getLogger("uvicorn.access").info('GET /invoices HTTP/1.1 200')
logging.getLogger("sqlalchemy.engine").warning("connection pool exhausted, size=%d", 5)

print("""
   Both come out as JSON, through the SAME stdlib handler.

   THIS is why structlog is the low-risk choice in a real service:
     - you keep dictConfig, RotatingFileHandler, QueueHandler, Sentry's
       LoggingIntegration, OpenTelemetry's LoggingHandler — the whole ecosystem
     - you add structured events on top
     - you migrate call sites one module at a time; both styles coexist

   You are not choosing structlog INSTEAD of stdlib. You are choosing it ON TOP.
   (Contrast loguru in ex08, which needs a 20-line InterceptHandler to reach parity.)
""")
