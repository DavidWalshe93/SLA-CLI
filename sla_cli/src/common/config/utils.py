"""
Author:     David Walshe
Date:       10 April 2021
"""

import logging
from functools import wraps

logger = logging.getLogger(__name__)


def inject_config(func):
    """Parses config from kwargs and adds config to function parameters."""

    @wraps(func)
    def inject_config_wrapper(*args, **kwargs):
        config = kwargs.pop("config")

        return func(*args, config=config, **kwargs)

    return inject_config_wrapper
