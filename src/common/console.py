"""
Author:     David Walshe
Date:       09 April 2021
"""

import logging

logger = logging.getLogger(__name__)


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
