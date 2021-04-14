"""
Author:     David Walshe
Date:       07 April 2021
"""

import logging
import os
from functools import wraps
from typing import Dict

import click

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


def default_from_context(key: str):
    """
    Allows for a default option to reference the Click Context obj object for a default value.

    :param key: The name of the value to reference.
    :return: The context as default custom option class.
    """

    class OptionDefaultFromContext(click.Option):

        def get_default(self, ctx):
            self.default = ctx.obj[key]
            return super(OptionDefaultFromContext, self).get_default(ctx)

    return OptionDefaultFromContext
