import logging

logger =logging.getLogger(__name__)

def fetch_data():
    logger.info("Fetching data from API")
    logger.warning("Slow response detected")