import logging

logger = logging.getLogger(__name__)

def connection():
    logger.info("Connecting to db")
    logger.error("Connection failed")