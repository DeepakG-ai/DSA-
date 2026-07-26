r"""
ex08 — loguru: everything ex03 + ex04 + ex06 + ex07 did, in a fraction of the code.

Needs:  pip install loguru      (skips cleanly if missing)
Run:    .\.venv\Scripts\python.exe docs\logging_notes\examples\ex08_loguru_demo.py
"""
import sys
from pathlib import Path

try:
    from loguru import logger
except ModuleNotFoundError:
    print("loguru is not installed — skipping this example.")
    print("Install it with:  .\\.venv\\Scripts\\python.exe -m pip install loguru")
    raise SystemExit(0)

OUT = Path(__file__).parent / "_out" / "loguru"
OUT.mkdir(parents=True, exist_ok=True)

# ─── 1. configuration ─────────────────────────────────────────────────────────
# ALWAYS remove() first — loguru ships a default stderr sink at DEBUG.
logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    format="{time:HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | "
           "{extra[request_id]} | {message}",
    colorize=True,
    backtrace=True,     # extend the traceback past the catching frame
    diagnose=False,     # variable VALUES in tracebacks — MUST be False in prod (leaks secrets)
)

logger.add(
    OUT / "app_{time:YYYY-MM-DD}.log",
    level="DEBUG",
    rotation="500 KB",       # or "00:00" / "1 week" / a callable
    retention="7 days",      # or a file count, or a callable
    compression="zip",       # applied on rotation
    encoding="utf-8",
    enqueue=True,            # non-blocking AND multiprocess-safe (loguru's QueueHandler)
)

logger.add(
    OUT / "events.jsonl",
    level="INFO",
    serialize=True,          # one JSON object per line — ex07's whole formatter, free
    enqueue=True,
)

# supply a default so {extra[request_id]} never blows up
logger.configure(extra={"request_id": "-"})

print("=" * 78)
print("Three sinks configured in ~20 lines: console, rotating+compressed file, JSONL")
print("=" * 78)

# ─── 2. basic use ─────────────────────────────────────────────────────────────
logger.debug("only in the file sink (console is INFO)")
logger.info("service started on port {}", 8000)     # {}-style, still lazy
logger.warning("disk at {pct}%", pct=91)
logger.error("upstream returned {}", 503)

# ─── 3. context: bind() and contextualize() ───────────────────────────────────
print()
print("=" * 78)
print("bind() — a NEW logger carrying fixed fields")
print("=" * 78)

user_log = logger.bind(request_id="req-001", user_id=42)
user_log.info("charged card")
user_log.info("receipt emailed")

print()
print("=" * 78)
print("contextualize() — contextvar-based, applies to EVERYTHING inside")
print("=" * 78)


def query_db(table):
    logger.info("SELECT * FROM {}", table)      # knows nothing about request ids


def handle_request():
    logger.info("request received")
    query_db("invoices")
    logger.info("request complete")


with logger.contextualize(request_id="req-002"):
    handle_request()

# ─── 4. exceptions: @logger.catch ─────────────────────────────────────────────
print()
print("=" * 78)
print("@logger.catch — traceback logged, function does not raise")
print("=" * 78)


@logger.catch(message="render failed")
def render(page):
    return 100 / page


render(0)

# ─── 5. custom levels and opt() ───────────────────────────────────────────────
print()
print("=" * 78)
print("custom levels + opt()")
print("=" * 78)

logger.level("AUDIT", no=25, color="<cyan><bold>")
logger.log("AUDIT", "user 42 downloaded invoice 991")

logger.opt(lazy=True).debug("expensive={}", lambda: "computed only if DEBUG is on")
logger.opt(depth=0).info("depth= is loguru's version of stdlib stacklevel=")

logger.complete()   # drain the enqueue=True sinks before exit

# ─── 6. the catch ─────────────────────────────────────────────────────────────
print()
print("=" * 78)
print("THE CATCH — third-party libraries don't know loguru exists")
print("=" * 78)
print(f"""
   Files written to {OUT.name}/:""")
for p in sorted(OUT.glob("*")):
    print(f"     {p.name}")

print("""
   Every library on PyPI (uvicorn, SQLAlchemy, boto3, httpx) logs through STDLIB
   logging. By default those records bypass loguru completely and you end up with
   two disjoint log streams.

   The fix is an InterceptHandler — a stdlib Handler that forwards into loguru:

       class InterceptHandler(logging.Handler):
           def emit(self, record):
               try:
                   level = logger.level(record.levelname).name
               except ValueError:
                   level = record.levelno
               frame, depth = logging.currentframe(), 2
               while frame and frame.f_code.co_filename == logging.__file__:
                   frame = frame.f_back
                   depth += 1
               logger.opt(depth=depth, exception=record.exc_info).log(
                   level, record.getMessage())

       logging.root.handlers = [InterceptHandler()]
       logging.root.setLevel("INFO")

   It works and it's in loguru's own docs. But notice: you just wrote 20 lines of
   stdlib logging code to make loguru usable in a real service. That is the honest
   cost. In a SCRIPT or CLI — where you own every logging call — the problem never
   arises, and loguru is excellent.

   AND: never make a PUBLISHED LIBRARY depend on loguru. Libraries use stdlib +
   NullHandler, so the application decides where logs go.
""")
