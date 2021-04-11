"""
Author:     David Walshe
Date:       10 April 2021
"""

import logging

logger = logging.getLogger(__name__)


def is_between(lower: float = 0.0, upper: float = 1.0):
    """Checks if value is a between a lower and higher limit."""

    def _is_between(obj, attribute, value):
        if value < lower or value > upper:
            raise ValueError(f"'{attribute.name}' in '{type(obj).__name__}' must be between {lower} and {upper}.")

    return _is_between


def greater_than(limit: float):
    """Checks if a value is greater than a set limit."""

    def _is_greater(obj, attribute, value):
        if value <= limit:
            raise ValueError(f"'{attribute.name}' in '{type(obj).__name__}' must be greater than {limit}.")

    return _is_greater


def one_of(options):
    """Checks if a value is one of several options."""

    def _one_of(obj, attribute, value):
        if value not in options:
            raise ValueError(f"'{attribute.name}' in '{type(obj).__name__}' must be one of '{[str(option).lower() for option in options]}'.")

    return _one_of
