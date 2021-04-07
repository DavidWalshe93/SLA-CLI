"""
Author:     David Walshe
Date:       07 April 2021
"""

import logging
from dataclasses import dataclass

import click

from src.cli.context import COMMAND_CONTEXT_SETTINGS
from src.cli.utils import kwargs_to_dataclass
from src.schema.db import DB

logger = logging.getLogger(__name__)


@dataclass
class LsParameters:
    pass


@click.command(**COMMAND_CONTEXT_SETTINGS, short_help="Lists the available datasets.")
@kwargs_to_dataclass(LsParameters)
def ls(params: LsParameters):
    """
    Shows the tools available datasets.
    """
    print(DB.get_db().datasets.names())
