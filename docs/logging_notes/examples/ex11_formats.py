r"""
ex11 — THE FORMAT STRING: timestamps, level, module, message.

Same one log call, printed under 15 different formats so you can see exactly
what each piece does.

Run:  .\.venv\Scripts\python.exe docs\logging_notes\examples\ex11_formats.py
"""
import logging
import sys

logger = logging.getLogger("mini_app.ocr")
logger.setLevel(logging.DEBUG)
logger.propagate = False


def show(label, fmt, datefmt=None, note=""):
    """Print ONE log line using the given format, then explain it."""
    for h in list(logger.handlers):
        logger.removeHandler(h)
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(logging.Formatter(fmt, datefmt=datefmt))
    logger.addHandler(h)

    print(f"\n  {label}")
    print(f"    format  = {fmt!r}")
    if datefmt:
        print(f"    datefmt = {datefmt!r}")
    print("    OUTPUT  -> ", end="")
    logger.warning("extracted %d pages", 12)
    if note:
        print(f"    {note}")


print("=" * 78)
print("1. THE PIECES — build the line up one field at a time")
print("=" * 78)

show("just the message (this is the DEFAULT for a bare handler)",
     "%(message)s")

show("+ the level",
     "%(levelname)s - %(message)s")

show("+ who logged it",
     "%(levelname)s - %(name)s - %(message)s")

show("+ when  <-- THE TIMESTAMP",
     "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
     note="Note the COMMA near the end. Those 3 digits are milliseconds — the default.")

show("+ exactly which line of code",
     "%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s")


print()
print("=" * 78)
print("2. CONTROLLING THE DATE/TIME  ->  datefmt=")
print("=" * 78)
print("""
  %(asctime)s is the ONLY field that has its own separate control: datefmt.
  It takes strftime codes:
      %Y year 2026   %m month 07   %d day 25
      %H hour 23     %M minute 05  %S second 25
      %b Jul         %A Saturday   %p AM/PM   %Z timezone name
""")

show("default (no datefmt given)",
     "%(asctime)s | %(message)s",
     note="ISO-ish date, comma, then milliseconds. Python's built-in default.")

show("date + time, no milliseconds",
     "%(asctime)s | %(message)s",
     datefmt="%Y-%m-%d %H:%M:%S")

show("time only — good for local dev, you know what day it is",
     "%(asctime)s | %(message)s",
     datefmt="%H:%M:%S")

show("day-month-year, human style",
     "%(asctime)s | %(message)s",
     datefmt="%d-%b-%Y %I:%M:%S %p")


print()
print("=" * 78)
print("3. THE MILLISECOND TRAP")
print("=" * 78)

print("""
  Everyone's first instinct for milliseconds is datefmt="...%S.%f", because that
  is how datetime.strftime works. It does NOT work here.

  Formatter uses time.strftime(), not datetime.strftime(), and time.strftime()
  has no %f at all.""")

# Build one record by hand so we can see the real failure instead of losing it.
record = logging.LogRecord(
    name="mini_app.ocr", level=logging.WARNING, pathname=__file__, lineno=30,
    msg="extracted %d pages", args=(12,), exc_info=None,
)

print("\n  WRONG:  datefmt='%Y-%m-%d %H:%M:%S.%f'")
bad = logging.Formatter("%(asctime)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S.%f")
try:
    print("    OUTPUT  ->", bad.format(record))
except ValueError as exc:
    print(f"    RAISES  ->  ValueError: {exc}")
    print("""
    And here is the nasty part: inside real logging that exception is caught by
    Handler.handleError(). Python prints '--- Logging error ---' to stderr and
    THROWS THE LOG LINE AWAY. Your message is gone, and the app keeps running as
    if nothing happened. (On Linux you may instead get a literal 'f' — equally
    wrong, just quieter.)""")

print("\n  RIGHT:  milliseconds are a SEPARATE field  ->  %(msecs)03d")
good = logging.Formatter("%(asctime)s.%(msecs)03d | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
print("    OUTPUT  ->", good.format(record))
print("    This is how every production format string does it.")


print()
print("=" * 78)
print("4. ALIGNMENT — the -8s that makes columns line up")
print("=" * 78)

print("\n  WITHOUT padding — ragged, hard to scan:")
for h in list(logger.handlers):
    logger.removeHandler(h)
h = logging.StreamHandler(sys.stdout)
h.setFormatter(logging.Formatter("    %(levelname)s | %(name)s | %(message)s"))
logger.addHandler(h)
logger.debug("opening file")
logger.info("extracted 12 pages")
logger.warning("scan detected")
logger.error("save failed")

print("\n  WITH padding — %(levelname)-8s and %(name)-14s:")
for h in list(logger.handlers):
    logger.removeHandler(h)
h = logging.StreamHandler(sys.stdout)
h.setFormatter(logging.Formatter("    %(levelname)-8s | %(name)-14s | %(message)s"))
logger.addHandler(h)
logger.debug("opening file")
logger.info("extracted 12 pages")
logger.warning("scan detected")
logger.error("save failed")

print("""
    -8s  = pad to 8 characters, LEFT aligned  (the minus sign means left)
     8s  = pad to 8 characters, RIGHT aligned
    .3s  = TRUNCATE to 3 characters  ->  DEB INF WAR ERR
""")


print("=" * 78)
print("5. EVERY FIELD YOU CAN USE")
print("=" * 78)

FIELDS = [
    ("%(asctime)s",       "human-readable time — controlled by datefmt"),
    ("%(msecs)03d",       "milliseconds, as a separate number"),
    ("%(created)f",       "raw Unix timestamp, e.g. 1785110725.75"),
    ("%(levelname)s",     "DEBUG / INFO / WARNING / ERROR / CRITICAL"),
    ("%(levelno)d",       "10 / 20 / 30 / 40 / 50"),
    ("%(name)s",          "logger name — the __name__ you passed to getLogger"),
    ("%(message)s",       "your text, after %-args are filled in"),
    ("%(filename)s",      "ocr.py"),
    ("%(pathname)s",      "C:\\full\\path\\to\\ocr.py"),
    ("%(module)s",        "ocr   (filename without .py)"),
    ("%(funcName)s",      "the function that logged"),
    ("%(lineno)d",        "line number"),
    ("%(process)d",       "process id"),
    ("%(processName)s",   "MainProcess"),
    ("%(thread)d",        "thread id"),
    ("%(threadName)s",    "MainThread"),
    ("%(taskName)s",      "asyncio task name (Python 3.12+)"),
    ("%(relativeCreated)d", "ms since logging was imported"),
]
for f, desc in FIELDS:
    print(f"    {f:<22} {desc}")

print("""
    Anything you pass via extra={} also becomes a field:
        logger.info("done", extra={"doc_id": "123"})   ->  %(doc_id)s
    But see QUICKSTART.md addendum #1 — you must add it to the format string
    or it will not appear.
""")


print("=" * 78)
print("6. THE THREE FORMATS WORTH MEMORISING")
print("=" * 78)

show("DEV — short, readable, you are watching it live",
     "%(asctime)s %(levelname)-8s %(name)s — %(message)s",
     datefmt="%H:%M:%S")

show("PROD FILE — full date, source location, thread",
     "%(asctime)s.%(msecs)03d %(levelname)-8s [%(process)d/%(threadName)s] "
     "%(name)s %(filename)s:%(lineno)d — %(message)s",
     datefmt="%Y-%m-%d %H:%M:%S")

show("CONTAINER — none of the above; emit JSON instead (see ex07)",
     "%(message)s",
     note="Docker/k8s add their own timestamp, so a plain message + JSON is standard.")

print("""
=============================================================================
  WHY THE TIMESTAMP MATTERS MOST
=============================================================================
  Everything else you can guess. The timestamp is the one thing you cannot
  reconstruct afterwards, and it is what lets you line up:

     - a customer saying "it broke around 3pm"
     - your app.log
     - the database slow-query log
     - the nginx access log

  ...into one story. That is why every production format starts with the time,
  and why servers log in UTC — so logs from machines in different timezones
  can still be sorted into a single sequence.
""")
