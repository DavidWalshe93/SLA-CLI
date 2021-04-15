"""
Author:     David Walshe
Date:       09 April 2021
"""

import logging
from functools import wraps

import colorama
from alive_progress import config_handler

logger = logging.getLogger(__name__)


def init_colorama(func):
    """Initialises colorama before usage."""

    @wraps(func)
    def init_colorama_wrapper(*args, **kwargs):
        colorama.init()

        return func(*args, **kwargs)

    return init_colorama_wrapper


def init_progress_bars(func):
    """Initialises the progress bar configuration."""

    @wraps(func)
    def init_progress_bars_wrapper(*args, **kwargs):
        config_handler.set_global(
            title_length=40,
            spinner="classic",
            unknown="classic",
            bar="classic"
        )

        return func(*args, **kwargs)

    return init_progress_bars_wrapper


def make_header(title: str, char: str = "=") -> str:
    """
    Returns a uniform header format to use in the CLI output.

    :param title: The title string to insert in the string.
    :param char: The character to make the header with.
    :return: A formatted header string.
    """
    br = f"{char}" * 100

    return f"{br}\n" \
           f"{title}\n" \
           f"{br}"
