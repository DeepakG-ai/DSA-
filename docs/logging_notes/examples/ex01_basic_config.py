r"""
ex01 — basicConfig, levels, and why print() loses.

Run:  .\.venv\Scripts\python.exe docs\logging_notes\examples\ex01_basic_config.py
"""
import logging
import sys

# ---------------------------------------------------------------- 1. the setup
# force=True (Python 3.8+) removes any handlers root already has.
# Without it, basicConfig is a NO-OP whenever something configured root first
# (pytest, a notebook, an imported module). This is pitfall #5.
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s.%(msecs)03d %(levelname)-8s %(name)s:%(lineno)d — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
    force=True,
)

log = logging.getLogger(__name__)   # __name__ is "__main__" when run directly

# ------------------------------------------------------------ 2. the 5 levels
log.debug("DEBUG   — values and branches; off in production")
log.info("INFO    — normal lifecycle: started, finished, 200 OK")
log.warning("WARNING — recovered or degraded; this is the DEFAULT root level")
log.error("ERROR   — this operation failed, a human should look")
log.critical("CRITICAL— the process is about to die")

# ------------------------------------------------ 3. lazy %-args vs f-strings
n, filename = 12, "invoice.pdf"

log.info("processed %d pages for %s", n, filename)   # GOOD — lazy
log.info(f"processed {n} pages for {filename}")      # works, but always pays the cost

# Proof the lazy form is actually lazy:
class Expensive:
    def __str__(self):
        print("   >>> __str__ ran! (something forced the format)")
        return "expensive-value"

log.setLevel(logging.INFO)                 # DEBUG is now OFF
log.debug("lazy:   %s", Expensive())       # __str__ NEVER runs
print("   (nothing above? good — the lazy form skipped formatting)")
log.info("eager:  %s", Expensive())        # __str__ runs, because INFO is on
log.setLevel(logging.DEBUG)

# ---------------------------------------------------- 4. exceptions properly
def divide(a, b):
    return a / b

try:
    divide(1, 0)
except ZeroDivisionError:
    # logger.exception() == logger.error(..., exc_info=True).
    # ONLY valid inside an except block; outside it you get "NoneType: None".
    log.exception("divide() failed")

try:
    divide(1, 0)
except ZeroDivisionError as exc:
    # When you have the object and are outside the handler, pass it explicitly:
    log.error("divide() failed again: %s", exc, exc_info=exc)

# -------------------------------------------- 5. stack_info: who called this?
def inner():
    log.warning("something odd here", stack_info=True)

def outer():
    inner()

outer()

# --------------------------------------------------- 6. why print() loses
print("PRINT: no timestamp, no level, no logger name, no file:line, "
      "can't be filtered, can't be routed, can't be turned off in prod.")

# ------------------------------------------------------- 7. the two-check rule
h = logging.getLogger().handlers[0]
print()
print(f"logger effective level : {logging.getLevelName(log.getEffectiveLevel())}")
print(f"handler level          : {logging.getLevelName(h.level)}   (0 = NOTSET = allow all)")
print("A record must pass BOTH to be emitted. This is pitfall #3.")
