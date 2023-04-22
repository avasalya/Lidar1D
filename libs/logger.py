import logging


class CustomFormatter(logging.Formatter):
    """
    A custom formatter for logging that provides color-coded output based on the log level.

    Attributes:
    -----------
    grey : str
        ANSI escape code for grey color.
    green : str
        ANSI escape code for green color.
    yellow : str
        ANSI escape code for yellow color.
    red : str
        ANSI escape code for red color.
    bold_red : str
        ANSI escape code for bold red color.
    reset : str
        ANSI escape code for resetting the color.
    format : str
        The format string for the log messages.

    Methods:
    --------
    format(record: logging.LogRecord) -> str:
        Formats the log message and applies the appropriate color based on the log level.
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
        Formats the log message and applies the appropriate color based on the log level.

        Parameters:
        -----------
        record : logging.LogRecord
            The LogRecord object containing the log message and its properties.

        Returns:
        --------
        str
            The formatted log message with appropriate color codes.
        """
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
