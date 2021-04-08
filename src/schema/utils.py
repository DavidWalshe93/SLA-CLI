"""
Author:     David Walshe
Date:       08 April 2021
"""

import logging
from functools import wraps

from colorama import init

logger = logging.getLogger(__name__)


def init_colorama(func):
    """Initialises colorama before usage."""

    @wraps(func)
    def init_colorama_wrapper(*args, **kwargs):
        init()

        return func(*args, **kwargs)

    return init_colorama_wrapper
