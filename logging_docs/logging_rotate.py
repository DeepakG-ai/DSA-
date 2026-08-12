"""Q39. Write the setup for a rotating log file: max size 5 MB, keep the last 3 backup files. (Hint: logging.handlers.RotatingFileHandler.) Explain what happens to app.log when it reaches 5 MB — what files exist afterwards?"""

import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

rotating_handler = RotatingFileHandler(
    filename="app.log",
    maxBytes=5 * 1024 * 1024,   # 5 MB
    backupCount=3                # keep last 3 backups
)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
rotating_handler.setFormatter(formatter)

logger.addHandler(rotating_handler)

logger.info("Application started")
logger.error("Something went wrong")

#first app creates app.log file, "a" append the logs till reaches to 5mb. then after that it will create new file called app.log.1. and add those log into that file. new fresh app.log file has been created.

"""## Setup code

```python
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

rotating_handler = RotatingFileHandler(
    filename="app.log",
    maxBytes=5 * 1024 * 1024,   # 5 MB
    backupCount=3                # keep last 3 backups
)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
rotating_handler.setFormatter(formatter)

logger.addHandler(rotating_handler)

logger.info("Application started")
logger.error("Something went wrong")
```



## What happens when app.log hits 5 MB

The moment `app.log` reaches (or is about to exceed) `maxBytes`, `RotatingFileHandler` performs a **rollover**: it closes the current file, shifts every existing backup file's number up by one, renames the full `app.log` to `app.log.1`, and opens a brand-new empty `app.log` to keep writing to. [runebook](https://runebook.dev/en/docs/python/library/logging.handlers/logging.handlers.RotatingFileHandler)

## File state at each rotation stage

| Stage | Files that exist |
|---|---|
| Before any rotation | `app.log` (growing) |
| After 1st rotation (app.log hits 5MB) | `app.log` (new, empty) + `app.log.1` (the old full one) |
| After 2nd rotation | `app.log` (new) + `app.log.1` (previous "new") + `app.log.2` (oldest) |
| After 3rd rotation | `app.log` (new) + `app.log.1` + `app.log.2` + `app.log.3` |
| After 4th rotation | `app.log` (new) + `app.log.1` + `app.log.2` + `app.log.3` — **the old `app.log.3` is deleted** to make room |

 [docs.python](https://docs.python.it/html/lib/node289.html)

## The renaming mechanic explained

Because `backupCount=3`, you'll never have more than 3 backup files plus the active `app.log` — 4 files total, always. On every rotation: [runebook](https://runebook.dev/en/docs/python/library/logging.handlers/logging.handlers.RotatingFileHandler)

- `app.log.2` → renamed to `app.log.3`
- `app.log.1` → renamed to `app.log.2`
- `app.log` (just-filled) → renamed to `app.log.1`
- A fresh empty `app.log` is created to receive new log messages

If a rotation would push the count beyond `backupCount`, the **oldest** file (`app.log.3` in this case) is simply deleted before the shift happens. [docs.python](https://docs.python.it/html/lib/node289.html)

## Key detail: `app.log` is always the "live" file

`app.log` itself never becomes a numbered backup permanently — it's always the file currently being written to. Higher numbers mean older data (`app.log.1` is more recent than `app.log.2`, which is more recent than `app.log.3`). This is why you set `backupCount=3` — it caps total disk usage at roughly `4 × 5MB = 20MB` for this logger, no matter how long the app runs. [conding-note.tistory](https://conding-note.tistory.com/94)

## One practical gotcha worth knowing

`RotatingFileHandler` checks the file size **only when a new log message is about to be written** — it's not monitoring the file continuously in the background. So the file may briefly exceed 5 MB by the size of one final log line before rotation triggers on the *next* write call. [stackoverflow](https://stackoverflow.com/questions/24505145/how-to-limit-log-file-size-in-python)"""