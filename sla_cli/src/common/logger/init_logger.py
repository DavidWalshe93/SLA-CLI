"""
Author:     David Walshe
Date:       07 April 2021
"""

import os
import yaml
import logging
import logging.config
from functools import wraps

logger = logging.getLogger(__name__)


def init_logger(func):
    """Initialised the logger from a configuration file."""

    @wraps(func)
    def init_logger_wrapper(*args, debug: bool = False, **kwargs):
        # Get the logger config in the same directory as this file.
        config_file_path = os.path.join(os.path.dirname(__file__), "logger_config.yml")

        with open(config_file_path, "r") as fh:
            config = yaml.safe_load(fh.read())

            if debug:
                config["handlers"]["console"]["level"] = "DEBUG"

            logging.config.dictConfig(config)

        return func(*args, **kwargs)

    return init_logger_wrapper
