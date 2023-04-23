#!/usr/bin/env python3
__author__ = "Ashesh Vasalya"
import sys
import logging

""" Example usage:
    from loghandler import LogHandler
    logger = LogHandler().log
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
"""


class CustomFormatter(logging.Formatter):
    """
    Subclass of logging.Formatter that defines ANSI color codes for different log levels.
    originally design:
    https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
    """
    grey = "\x1b[38;20m"
    green = "\x1b[32m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    FORMATS = {
        logging.DEBUG: green + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        """
        Override the format method to use the custom log formats defined above.
        """
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class LogHandler:
    """
    A class that sets up a logger with the given name and adds a console handler that uses the
    CustomFormatter defined above.
    """
    def __init__(self, name=None):
        """
        Initialize a logger with the given name, or default to sys.argv[0].
        """
        self.log = logging.getLogger(name or sys.argv[0])
        self.log.setLevel(logging.DEBUG)

        # create console handler with a higher log level
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.DEBUG)
        consoleHandler.setFormatter(CustomFormatter())
        self.log.addHandler(consoleHandler)
