"""Q38. Write a complete logger_setup.py module that:

creates a logger named "app"
logs to BOTH the console and a file app.log
console shows INFO and above, file records DEBUG and above
format includes timestamp, level, filename, line number, message"""

import logging

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)-8s - %(filename)s:%(lineno)d - %(message)s", #fmt="%(asctime)s - %(levelname)s-%(message)s",
                           datefmt="%Y-%m-%d %H:%M:%S")
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = logging.FileHandler(filename="app.log",encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.debug("DEBUG: it is working")
logger.info("Starting the info")
logger.error("Errors are logged into file")
logger.warning("WARNING: update the pip")
logger.critical("critical error found")
