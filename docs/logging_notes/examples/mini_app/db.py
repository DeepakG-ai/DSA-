import logging

logger = logging.getLogger(__name__)      # "mini_app.db"


def save(doc: str, text: str) -> None:
    logger.debug("connecting to database")
    logger.info("saved %s (%d chars)", doc, len(text))
    if doc == "invoice_002.tif":
        try:
            raise ValueError("duplicate primary key")
        except ValueError:
            logger.exception("could not save %s", doc)
