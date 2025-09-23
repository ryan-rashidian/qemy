"""Logging configuration for Qemy."""

import logging

logging.basicConfig(
    level = logging.INFO
)

def get_logger(name: str) -> logging.Logger:
    """Return a logger using the global config."""
    return logging.getLogger(name)

def set_log_level(level: int) -> None:
    """Set global logging level."""
    root = logging.getLogger()
    root.setLevel(level)

