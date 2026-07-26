r"""
ex04 — RotatingFileHandler vs TimedRotatingFileHandler, demonstrated live.

Run:  .\.venv\Scripts\python.exe docs\logging_notes\examples\ex04_rotation.py
"""
import logging
import logging.handlers
import time
from pathlib import Path

OUT = Path(__file__).parent / "_out" / "rotation"
OUT.mkdir(parents=True, exist_ok=True)
for stale in OUT.glob("*"):
    stale.unlink()

FMT = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")


# ══════════════════════════════════ 1. SIZE-BASED ═════════════════════════════
print("=" * 70)
print("1. RotatingFileHandler — roll over at a SIZE limit")
print("=" * 70)

size_log = OUT / "bysize.log"
h = logging.handlers.RotatingFileHandler(
    size_log,
    maxBytes=800,          # tiny, so we can see it roll. Use ~10MB for real.
    backupCount=3,         # keeps bysize.log.1 .2 .3 — total disk = 800 * 4
    encoding="utf-8",      # ALWAYS set this
)
h.setFormatter(FMT)

lg = logging.getLogger("bysize")
lg.setLevel(logging.INFO)
lg.propagate = False
lg.addHandler(h)

for i in range(40):
    lg.info("record number %03d — padding to make the file grow quickly", i)

h.close()

print(f"\nFiles created in {OUT.name}/:")
for p in sorted(OUT.glob("bysize.log*")):
    print(f"   {p.name:20} {p.stat().st_size:>5} bytes")

print("""
   bysize.log    = current (newest)
   bysize.log.1  = previous
   bysize.log.3  = oldest kept; anything older was DELETED

   Total disk used is bounded: maxBytes * (backupCount + 1). Budget it.
   backupCount=0 means "truncate on rollover, keep nothing" — almost never right.
""")


# ══════════════════════════════════ 2. TIME-BASED ═════════════════════════════
print("=" * 70)
print("2. TimedRotatingFileHandler — roll over on a CLOCK boundary")
print("=" * 70)

time_log = OUT / "bytime.log"
th = logging.handlers.TimedRotatingFileHandler(
    time_log,
    when="S",              # SECONDS, only so this demo finishes. Real: "midnight" or "D".
    interval=1,
    backupCount=3,         # here backupCount means RETENTION: 3 intervals of history
    encoding="utf-8",
    utc=True,              # use UTC on servers — avoids DST double/zero rollovers
)
th.setFormatter(FMT)

tl = logging.getLogger("bytime")
tl.setLevel(logging.INFO)
tl.propagate = False
tl.addHandler(th)

for i in range(5):
    tl.info("tick %d", i)
    time.sleep(1.1)

th.close()

print(f"\nFiles created in {OUT.name}/:")
for p in sorted(OUT.glob("bytime.log*")):
    print(f"   {p.name:32} {p.stat().st_size:>5} bytes")

print("""
   The suffix is a TIMESTAMP, not a counter. That's the practical difference:
   'give me Tuesday's logs' is a filename lookup instead of a search.

   Use TimedRotating when the requirement is stated in TIME ("keep 30 days").
   Use Rotating     when the requirement is stated in SIZE ("cap it at 500MB").
""")


# ══════════════════════════════ 3. THE THINGS THAT BITE ═══════════════════════
print("=" * 70)
print("3. What actually goes wrong")
print("=" * 70)
print("""
   a) MULTIPLE PROCESSES  Officially unsupported. Two Gunicorn workers rotating
      the same file interleave lines and race on the rename — you LOSE data.
      Fix: one stream per process (stdout), or SocketHandler to one collector.

   b) EXTERNAL logrotate  After logrotate renames the file, your handler keeps
      writing to the now-unlinked inode. Logs look dead; disk keeps filling.
      Fix: use WatchedFileHandler (Linux), or let Python rotate and disable
      logrotate for that path. Never both.

   c) MISSING DIRECTORY   FileHandler will NOT mkdir. FileNotFoundError at
      startup, usually only in the container. mkdir(parents=True, exist_ok=True)
      before you configure. pip subclasses _open() just to do this.

   d) MISSING encoding    Without encoding="utf-8", Windows uses cp1252 and the
      first non-Latin-1 character raises UnicodeEncodeError mid-request.

   e) IN A CONTAINER      Don't do any of this. Write to stdout and let Docker /
      k8s / ECS collect it. Rotation is the platform's job, not yours.
""")
