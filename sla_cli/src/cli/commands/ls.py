"""
Author:     David Walshe
Date:       07 April 2021
"""

import logging
from dataclasses import dataclass, asdict

import click

from sla_cli.src.common.console import init_colorama

from sla_cli.src.cli.context import COMMAND_CONTEXT_SETTINGS
from sla_cli.src.cli.utils import kwargs_to_dataclass
from sla_cli.src.db.accessors import AccessorFactory

logger = logging.getLogger(__name__)


@dataclass
class LsParameters:
    verbose: str
    output_file: str
    legend: bool
    tablefmt: str
    capture_method: str
    availability: str
    regex: str = ".*"


@click.command(**COMMAND_CONTEXT_SETTINGS, short_help="Lists the available datasets.")
@click.argument("regex", type=click.STRING, nargs=1, default=r".*")
@click.option("-v", "--verbose", type=click.Choice(["totals", "all", "info"], case_sensitive=False), default=None, help="The level of verbosity of the output.")
@click.option("-o", "--output-file", type=str, default=None, help="Saves the output to the file path specified, if unused contents are printed to the console.")
@click.option("-t", "--tablefmt", default="simple", help="Any format available for tabulate, details at: 'https://github.com/astanin/python-tabulate#table-format'")
@click.option("-c", "--capture-method", type=click.Choice(["all", "dermoscopy", "camera"], case_sensitive=False), default="all", help="Filters the results by the capture method used in the dataset.")
@click.option("-a", "--availability", type=click.Choice(["all", "private", "public"], case_sensitive=False), default="all", help="The availability of the dataset.")
@click.option("--legend", is_flag=True, help="Shows the abbreviation legend for each diagnosis.")
@kwargs_to_dataclass(LsParameters)
def ls(params: LsParameters):
    """
    Shows the available datasets in various forms of verbosity.
    """
    if params.legend:
        abbrev = AccessorFactory.create_abbreviation()
        print(abbrev.abbreviations(tablefmt=params.tablefmt))

    else:
        datasets = AccessorFactory.create_datasets()
        func = {
            "totals": datasets.names_and_overall_images,
            "all": datasets.names_and_distribution,
            "info": datasets.names_information
        }.get(params.verbose, datasets.names)

        print(func(**asdict(params)))
