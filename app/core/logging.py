"""Logging configuration module."""

import logging
import sys


def setup_logging(level: int = logging.INFO) -> None:
    """Configure the root logger for the application.

    Args:
        level: Logging level (e.g., logging.INFO, logging.DEBUG).
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
