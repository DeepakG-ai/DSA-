r"""
ex07 — structured JSON logs with ZERO dependencies.

This is what you want in a container: one JSON object per line on stdout, and
the platform (Docker / k8s / ECS / CloudWatch / Loki) does the rest.

Run:  .\.venv\Scripts\python.exe docs\logging_notes\examples\ex07_json_logs.py
"""
import datetime as dt
import json
import logging
import sys
import uuid

# Every attribute the stdlib itself puts on a record. Anything NOT in here came
# from your extra={...}, so it belongs in the JSON payload.
_RESERVED = set(
    logging.LogRecord("", 0, "", 0, "", (), None).__dict__
) | {"message", "asctime", "taskName"}


class JsonFormatter(logging.Formatter):
    def __init__(self, service: str = "demo", env: str = "dev"):
        super().__init__()
        self.service = service
        self.env = env

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": dt.datetime.fromtimestamp(record.created, dt.timezone.utc)
                    .isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "service": self.service,
            "env": self.env,
            "module": record.module,
            "line": record.lineno,
            "thread": record.threadName,
        }
        if record.exc_info:
            payload["exc_type"] = record.exc_info[0].__name__
            payload["exc"] = self.formatException(record.exc_info)
        if record.stack_info:
            payload["stack"] = self.formatStack(record.stack_info)

        # everything the caller passed via extra={...}
        for key, value in record.__dict__.items():
            if key not in _RESERVED and not key.startswith("_"):
                payload[key] = value

        # default=str stops "Object of type UUID is not JSON serializable" from
        # taking down your logging. ensure_ascii=False keeps non-English readable.
        return json.dumps(payload, default=str, ensure_ascii=False)


def configure(env="dev"):
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)

    h = logging.StreamHandler(sys.stdout)
    # dev: human-readable. prod: JSON. Branch on whether we're on a terminal.
    if env == "prod" or not sys.stdout.isatty():
        h.setFormatter(JsonFormatter(service="ocr-api", env=env))
    else:
        h.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(name)s — %(message)s"))
    root.addHandler(h)
    root.setLevel(logging.INFO)


configure(env="prod")
log = logging.getLogger("billing")

print("=" * 78)
print("Structured events — note extra={} becomes top-level JSON fields")
print("=" * 78)

log.info("service_started", extra={"port": 8000, "workers": 4})
log.info("card_charged", extra={"user_id": 42, "amount_cents": 999, "currency": "usd"})
log.warning("rate_limited", extra={"user_id": 42, "retry_after_s": 30})

# non-serializable objects survive because of default=str
log.info("job_queued", extra={"job_id": uuid.uuid4(), "at": dt.datetime.now()})

try:
    1 / 0
except ZeroDivisionError:
    log.exception("charge_failed", extra={"user_id": 42, "attempt": 3})

print()
print("=" * 78)
print("Why this beats a formatted sentence")
print("=" * 78)
print("""
   SENTENCE:  logger.info(f"charged user {uid} for {amt}")
              -> to find charges over $5 you write a regex. Every message is a
                 unique string, so aggregators can't group them.

   EVENT:     logger.info("card_charged", extra={"user_id": uid, "amount_cents": amt})
              -> Datadog/Loki/CloudWatch query:  msg:card_charged AND amount_cents>500
                 No regex. Groupable. Alertable. Chartable.

   RESERVED KEYS — this raises KeyError:
       logger.info("hi", extra={"message": "x"})
       KeyError: "Attempt to overwrite 'message' in LogRecord"
   Reserved: message asctime name msg args levelname levelno pathname filename
             module exc_info exc_text stack_info lineno funcName created msecs
             relativeCreated thread threadName processName process taskName
   Namespace yours if in doubt: extra={"app_user_id": 42}

   OFF-THE-SHELF: pip install python-json-logger, then in dictConfig:
       "formatters": {"json": {"()": "pythonjsonlogger.json.JsonFormatter"}}
   Or use structlog (ex09) if you want bind() semantics too.
""")
