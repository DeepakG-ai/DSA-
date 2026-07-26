r"""
ex10 — HOW getLogger() IN ONE FILE CONNECTS TO basicConfig() IN ANOTHER.

mini_app/ocr.py and mini_app/db.py only do:   logger = logging.getLogger(__name__)
This file does all the configuring. Watch how they find each other.

Run:  .\.venv\Scripts\python.exe docs\logging_notes\examples\ex10_two_files.py
"""
import logging
import sys
from pathlib import Path

from mini_app import db, ocr

OUT = Path(__file__).parent / "_out"
OUT.mkdir(exist_ok=True)
LOGFILE = OUT / "mini_app.log"
LOGFILE.unlink(missing_ok=True)


def banner(t):
    print(f"\n{'=' * 74}\n{t}\n{'=' * 74}")


def run_the_app():
    """The business logic. Identical in every phase below."""
    for doc in ("invoice_001.pdf", "invoice_002.tif"):
        text = ocr.extract(doc)
        db.save(doc, text)


# ══════════════════════════════════════════════════════════════════════════════
banner("PHASE 1 — getLogger() alone, NO configuration anywhere")
# ══════════════════════════════════════════════════════════════════════════════

run_the_app()

print("""
   ^ Almost nothing. Only the WARNING and ERROR leaked out, in ugly raw form.

   Why: a logger created by getLogger() has NO HANDLER of its own. It has
   nowhere to write. The default root level is WARNING, so info/debug were
   dropped, and the two survivors hit a bare-bones emergency fallback.

   getLogger() alone = the modules can SPEAK, but nobody is LISTENING.
""")


# ══════════════════════════════════════════════════════════════════════════════
banner("PHASE 2 — the SAME modules, unchanged, + basicConfig() here")
# ══════════════════════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-8s | %(name)-14s | %(message)s",
    stream=sys.stdout,      # default is sys.STDERR — pinned here so this demo reads in order
    force=True,             # without force=True this whole call is a NO-OP if root
)                           # already has a handler. Pitfall #5.

run_the_app()

print("""
   ^ Everything appears, tagged with the module it came from.

   I did not touch ocr.py or db.py. So HOW did they connect?
""")


# ══════════════════════════════════════════════════════════════════════════════
banner("THE ANSWER — one global registry, shared by the whole process")
# ══════════════════════════════════════════════════════════════════════════════

a = logging.getLogger("mini_app.ocr")     # asked for here, in main
b = ocr.logger                            # created over there, in ocr.py

print(f"   logging.getLogger('mini_app.ocr')  is  ocr.logger   ->  {a is b}")
print("""
   THE SAME OBJECT. getLogger() is not a constructor — it is a LOOKUP in one
   dictionary that lives inside the logging module itself. Every file that asks
   for the same name gets the same object back. That dictionary is how two
   files that never import each other end up talking about the same logger.

   Now the second half — the chain upward:""")

node = ocr.logger
while node:
    kind = "ROOT" if node.parent is None else "logger"
    print(f"      {kind:6} {node.name!r:16} handlers={node.handlers}")
    node = node.parent

print("""
   ocr.logger has handlers=[]  — empty. It cannot write anywhere.
   root       has handlers=[StreamHandler]  — because basicConfig put it there.

   So a record flows:   mini_app.ocr  ->  mini_app  ->  root  ->  its handler

   THAT is the connection. Not an import. Not a variable you pass around.
   Just: everyone is a child of root, and root is where the handler lives.
""")


# ══════════════════════════════════════════════════════════════════════════════
banner("PHASE 3 — WHY YOU NEED StreamHandler *AND* FileHandler")
# ══════════════════════════════════════════════════════════════════════════════

console = logging.StreamHandler(sys.stdout)            # destination 1: your screen
console.setLevel(logging.WARNING)                      # ...but only the important stuff
console.setFormatter(logging.Formatter(
    "CONSOLE >> %(levelname)-8s %(message)s"))

filehand = logging.FileHandler(LOGFILE, encoding="utf-8")   # destination 2: the file
filehand.setLevel(logging.DEBUG)                            # ...and EVERYTHING goes here
filehand.setFormatter(logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)-14s | %(message)s"))

root = logging.getLogger()
for h in list(root.handlers):
    root.removeHandler(h)
root.addHandler(console)
root.addHandler(filehand)
root.setLevel(logging.DEBUG)          # let everything through; handlers decide

run_the_app()

print(f"""
   ^ On screen you got ONLY the warning and the error. Quiet. Readable.

   Meanwhile {LOGFILE.name} received all of this:""")
print("   " + "-" * 68)
for line in LOGFILE.read_text(encoding="utf-8").splitlines():
    print("   " + line)
print("   " + "-" * 68)

print("""
   ONE logger.info() call. TWO destinations. DIFFERENT amounts of detail.

   WHY BOTH:
     StreamHandler (console) — for you, RIGHT NOW, while it runs. You are
       watching, so you want it quiet: warnings and errors only. It vanishes
       when you close the terminal. Useless tomorrow.

     FileHandler (file) — for you LATER, after the crash. Nobody is reading it
       live, so it can be exhaustive: every debug line, timestamps, module names.
       It survives. It is what you open when a customer says "it broke at 3am".

   This is why a handler has its OWN setLevel(). One logger.info() call, and
   each destination independently decides whether it cares. That is the whole
   reason the Logger / Handler split exists.

   And this is exactly what basicConfig CANNOT do:
       basicConfig(filename="app.log")   -> file only, console SILENT
       basicConfig()                     -> console only, no file
   One call, one handler, one destination. The moment you want two, you build
   the handlers yourself — or you use dictConfig (ex03).
""")
