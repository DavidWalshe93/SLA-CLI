"""
Author:     David Walshe
Date:       07 April 2021
"""

import logging
import os
from functools import wraps
from typing import Dict

logger = logging.getLogger(__name__)


def kwargs_to_dataclass(data_class):
    """
    Converts a click commands option arguments into a python dataclass

    :param data_class: A dataclass reference to create and inject as the command's param object.
    """

    def _kwargs_to_dataclass(func: callable):
        @wraps(func)
        def _kwargs_to_dataclass_wrapper(*args, **kwargs):
            command_args = data_class(**kwargs)

            return func(*args, command_args)

        return _kwargs_to_dataclass_wrapper

    return _kwargs_to_dataclass
