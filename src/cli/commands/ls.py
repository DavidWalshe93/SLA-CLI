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
    output: str
    legend: bool
    tablefmt: str


@click.command(**COMMAND_CONTEXT_SETTINGS, short_help="Lists the available datasets.")
@click.option("-v", "--verbose", type=click.Choice(["totals", "all"], case_sensitive=False), default=None, help="The level of verbosity of the output.")
@click.option("-o", "--output", type=str, default=None, help="Saves the output to the file path specified, if unused contents are printed to the console.")
@click.option("-t", "--tablefmt", default="simple", help="Any format available for tabulate, 'https://github.com/astanin/python-tabulate#table-format'")
@click.option("--legend", is_flag=True, help="Shows the abbreviation legend for each diagnosis.")
@kwargs_to_dataclass(LsParameters)
def ls(params: LsParameters):
    """
    Shows the available datasets in various forms of verbosity.
    """
    db = DB.get_db()

    if params.legend:
        print(db.datasets.abbreviations(tablefmt=params.tablefmt))
    else:
        func = {

            "totals": db.datasets.names_and_overall_images,
            "all": db.datasets.names_and_distribution,

        }.get(params.verbose, db.datasets.names)

        print(func(tablefmt=params.tablefmt, output_file=params.output))
