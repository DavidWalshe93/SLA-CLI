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
    verbose: str
    tablefmt: str


@click.command(**COMMAND_CONTEXT_SETTINGS, short_help="Lists the available datasets.")
@click.option("-v", "--verbose", type=click.Choice(["totals"], case_sensitive=False), default=None, help="The level of verbosity of the output.")
@click.option("-t", "--tablefmt", default="simple", help="Any format available for tabulate, 'https://github.com/astanin/python-tabulate#table-format'")
@kwargs_to_dataclass(LsParameters)
def ls(params: LsParameters):
    """
    Shows the available datasets in various forms of verbosity.
    """
    func = {

        "totals": DB.get_db().datasets.names_and_overall_images

    }.get(params.verbose, DB.get_db().datasets.names)

    print(func(tablefmt=params.tablefmt))
