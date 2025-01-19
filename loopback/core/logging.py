import logging
from logging import config
import sys

logger = logging.getLogger("uvicorn.access")


def setup_logging() -> None:
    logger.propagate = False
    logger.handlers = []
    logger.addHandler(logging.FileHandler("access.log"))