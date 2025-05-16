import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name):
    """
    Configure and return a logger with console and file handlers.
    Args:
        name: str, the logger name (usually __name__).
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    if logger.handlers:  # Avoid duplicate handlers
        return logger

    logger.setLevel(logging.INFO)

    # Formatter for logs
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler with rotation (max 5MB, keep 3 backups)
    log_file = 'crawler.log'
    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger