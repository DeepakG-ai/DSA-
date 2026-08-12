import requests
import logging
import time

logging.basicConfig(
    filename="app.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

def call_api(url, timeout=10, delay=2, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            content = requests.get(url, timeout=timeout)
            content.raise_for_status()
            return content.text
        except requests.exceptions.RequestException as e:
            logger.error("Attempt %d failed: %s", attempt, e)
            if attempt < max_retries:
                time.sleep(delay)
            else:
                raise

print(call_api("https://requests.readthedocs.io/en/latest/user/quickstart/"))