"""
Author:     David Walshe
Date:       08 April 2021
"""

import logging
import re

logger = logging.getLogger(__name__)


def compile_regex(regex) -> re.Pattern:
    """
    Compiles regex patterns to filter results.

    :param regex: The regex to create the pattern with.
    :return: The compiled regex pattern.
    """
    return re.compile(rf"^{regex}", re.IGNORECASE | re.MULTILINE)
