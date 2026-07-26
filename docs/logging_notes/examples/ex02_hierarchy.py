r"""
ex02 — the logger tree, propagation, and the duplicate-line bug.

Run:  .\.venv\Scripts\python.exe docs\logging_notes\examples\ex02_hierarchy.py
"""
import logging
import sys


def banner(text):
    print(f"\n{'=' * 70}\n{text}\n{'=' * 70}")


def reset_root(fmt="ROOT     | %(name)-20s | %(message)s"):
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
        h.close()
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(logging.Formatter(fmt))
    root.addHandler(h)
    root.setLevel(logging.DEBUG)


# ----------------------------------------------------------- 1. names = a tree
banner("1. getLogger(name) builds a TREE from the dots")

reset_root()
child = logging.getLogger("backend.worker.ocr")

print("   Before the intermediate loggers exist:")
node = child
while node is not None:
    print(f"      {node.name!r:32} parent={getattr(node.parent, 'name', None)!r}")
    node = node.parent

print("""
   Notice 'backend.worker.ocr' says its parent is 'root', skipping two levels.
   Loggers are created LAZILY: 'backend' and 'backend.worker' don't exist as
   objects yet, only as internal PlaceHolder entries. The record still reaches
   root correctly — but any handler you later attach to 'backend' is wired in
   at that moment. Touch them and the chain fills in:""")

logging.getLogger("backend")            # now they exist
logging.getLogger("backend.worker")

print("\n   After:")
node = child
while node is not None:
    print(f"      {node.name!r:32} parent={getattr(node.parent, 'name', None)!r}")
    node = node.parent
print("\n   The root logger's name is 'root'; you ask for it with getLogger('').")

# getLogger is a REGISTRY LOOKUP, not a constructor:
print(f"\n   same object every time? {logging.getLogger('backend') is logging.getLogger('backend')}")


# ------------------------------------------------------------ 2. propagation
banner("2. propagation: a record walks UP the tree to every parent's handlers")

reset_root()
logging.getLogger("backend.worker.ocr").info("one call ->")
print("   ^ emitted by ROOT's handler, even though nothing was attached to the child.")


# --------------------------------------------------- 3. the duplicate-line bug
banner("3. THE BUG: handler on the child AND on root = every line twice")

reset_root()
app = logging.getLogger("app")
own = logging.StreamHandler(sys.stdout)
own.setFormatter(logging.Formatter("CHILD    | %(name)-20s | %(message)s"))
app.addHandler(own)                      # <-- the mistake

app.info("printed twice")
print("   ^ two lines for one call. CHILD's handler, then ROOT's via propagation.")


# ------------------------------------------------------------- 4. three fixes
banner("4. Fix A: propagate = False (stop the walk at this logger)")
app.propagate = False
app.info("printed once now")

banner("4. Fix B (BEST): never addHandler on child loggers — only on root")
app.propagate = True
app.removeHandler(own)
own.close()
app.info("printed once, and root controls the format for everything")


# ------------------------------ 5. parent LEVELS are not rechecked, handlers are
banner("5. Only the ORIGINATING logger's level is checked. Parents' HANDLER levels are.")

reset_root()
noisy = logging.getLogger("noisy")
noisy.setLevel(logging.WARNING)          # level check #1 happens HERE
noisy.info("you will NOT see this")      # dropped at the source
noisy.warning("you WILL see this")

quiet_handler = logging.getLogger().handlers[0]
quiet_handler.setLevel(logging.ERROR)    # level check #2, on the handler
noisy.warning("dropped by the HANDLER's level, not the logger's")
noisy.error("passes both checks")


# ----------------------------------------------- 6. controlling library noise
banner("6. How to quiet a third-party library")

reset_root()
for name in ("urllib3", "botocore", "sqlalchemy.engine"):
    logging.getLogger(name).setLevel(logging.WARNING)
    print(f"   {name:22} -> WARNING")

logging.getLogger("urllib3.connectionpool").debug("chatty debug — suppressed")
logging.getLogger("urllib3.connectionpool").warning("real problem — kept")
print("\n   Note: setting 'urllib3' also covers 'urllib3.connectionpool' — children inherit.")


# ---------------------------------------------------------- 7. the library rule
banner("7. The library rule: NullHandler")

lib = logging.getLogger("mylib")
lib.addHandler(logging.NullHandler())
print("   In mylib/__init__.py:  logging.getLogger(__name__).addHandler(logging.NullHandler())")
print("   -> your library is SILENT until the application configures logging.")
print("   requests, urllib3, boto3, httpx, SQLAlchemy all do exactly this.")
