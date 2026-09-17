from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from .config import app_dir


def configure_logging() -> logging.Logger:
    logger = logging.getLogger("mactrix")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(
        app_dir() / "mactrix.log",
        maxBytes=512_000,
        backupCount=3,
        encoding="utf-8",
    )
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    logger.addHandler(handler)
    return logger
