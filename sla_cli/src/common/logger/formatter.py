"""
Author:     David Walshe
Date:       10 April 2021
"""

import logging
from colorama import Fore

logger = logging.getLogger(__name__)


class ColorFormatter(logging.Formatter):
    """Adds colored output to logger."""

    # log output format.
    format = "[SLA] - %(levelname)-8s - %(message)-8s"

    FORMATS = {
        logging.DEBUG: Fore.CYAN + format + Fore.RESET,
        logging.INFO: format,
        logging.WARNING: Fore.YELLOW + format + Fore.RESET,
        logging.ERROR: Fore.RED + format + Fore.RESET,
    }

    def format(self, record):
        """
        Formats the log record before returning it to the caller.

        :param record: The record to colorize.
        :return: The colur formatted record.
        """
        log_format = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_format)

        return formatter.format(record)
