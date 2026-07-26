import logging

# WHO is speaking. That is ALL this line does.
# __name__ here is the string "mini_app.ocr"
logger = logging.getLogger(__name__)

# Notice what is NOT in this file:
#   no basicConfig, no FileHandler, no StreamHandler, no format string, no level.
# This module has no idea whether its logs go to the screen, a file, both, or nowhere.
# That is deliberate — the entry point decides.


def extract(doc: str) -> str:
    logger.debug("opening %s", doc)                       # detail, usually off
    logger.info("extracted text from %s", doc)            # normal lifecycle
    if doc.endswith(".tif"):
        logger.warning("%s is a scan — OCR will be slow", doc)
    return f"text-of-{doc}"
