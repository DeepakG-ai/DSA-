r"""
ex03 — the production pattern: dictConfig, once, at startup.

This is the shape Django / uvicorn / pip / Airflow all use.

Run:  .\.venv\Scripts\python.exe docs\logging_notes\examples\ex03_dictconfig.py
"""
import logging
import logging.config
import os
import sys
from pathlib import Path

OUT = Path(__file__).parent / "_out"
OUT.mkdir(exist_ok=True)            # handlers do NOT create the directory (pitfall #10)


# ─── a filter that DROPS records ──────────────────────────────────────────────
class NoHealthChecks(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return "/health" not in record.getMessage()


# ─── a filter that STAMPS records (returns True always) ───────────────────────
class HostnameFilter(logging.Filter):
    def __init__(self, hostname: str = "local"):
        super().__init__()
        self.hostname = hostname

    def filter(self, record: logging.LogRecord) -> bool:
        record.hostname = self.hostname
        return True


LOGGING = {
    "version": 1,                        # always literally 1 — the schema version
    "disable_existing_loggers": False,   # ALWAYS. True silences every already-imported lib.

    "filters": {
        # "()" is the factory key: instantiate this callable with the remaining kwargs
        "no_health": {"()": f"{__name__}.NoHealthChecks"},
        "hostname":  {"()": f"{__name__}.HostnameFilter", "hostname": os.getenv("HOSTNAME", "dev-box")},
    },

    "formatters": {
        "console": {
            "format": "%(asctime)s.%(msecs)03d %(levelname)-8s %(hostname)s %(name)s — %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            # defaults= (Python 3.10+) supplies fallbacks for fields a record may lack.
            # Without it, a record that skipped HostnameFilter raises at format time.
            "defaults": {"hostname": "-"},
        },
        "detailed": {
            "format": "%(asctime)s %(levelname)-8s %(name)s %(filename)s:%(lineno)d "
                      "[pid=%(process)d tid=%(thread)d] — %(message)s",
        },
    },

    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",     # ext:// resolves a dotted name at config time
            "formatter": "console",
            "filters": ["hostname", "no_health"],
            "level": "DEBUG",
        },
        "errors": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(OUT / "errors.log"),
            "maxBytes": 1_000_000,
            "backupCount": 3,
            "encoding": "utf-8",              # NOT optional on Windows (pitfall #9)
            "formatter": "detailed",
            "level": "ERROR",                 # only failures reach this sink
        },
    },

    # per-logger levels — this is how you quiet noisy libraries from config,
    # with no code change and no import of the library
    "loggers": {
        "demo":              {"level": "DEBUG"},
        "urllib3":           {"level": "WARNING"},
        "botocore":          {"level": "WARNING"},
        "sqlalchemy.engine": {"level": "WARNING"},
    },

    "root": {"handlers": ["stdout", "errors"], "level": os.getenv("LOG_LEVEL", "INFO")},
}

logging.config.dictConfig(LOGGING)


# ─── use it ───────────────────────────────────────────────────────────────────
log = logging.getLogger("demo")
log.debug("demo logger is at DEBUG, so this shows")
log.info("service started, port=%d", 8000)

logging.getLogger("demo.http").info("GET /invoices 200 in 34ms")
logging.getLogger("demo.http").info("GET /health 200 in 1ms   <- dropped by NoHealthChecks")

logging.getLogger("urllib3.connectionpool").debug("chatty — suppressed by config")

try:
    {}["missing"]
except KeyError:
    logging.getLogger("demo.worker").exception("job failed")

print()
print(f"ERROR+ also went to: {OUT / 'errors.log'}")
print((OUT / "errors.log").read_text(encoding="utf-8"))

print("Key points:")
print("  1. dictConfig runs ONCE, at startup.")
print("  2. disable_existing_loggers: False — always.")
print("  3. Handlers attach to ROOT. Modules only do getLogger(__name__).")
print("  4. Sink/level/format changes are CONFIG changes, not code changes.")
