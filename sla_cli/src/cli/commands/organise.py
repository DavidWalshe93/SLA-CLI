"""
Author:     David Walshe
Date:       14 April 2021
"""

import logging
import logging
import os
from typing import List
from dataclasses import dataclass, asdict
import hashlib

import click
from click import Context
from click.exceptions import BadOptionUsage

from sla_cli.src.cli.context import COMMAND_CONTEXT_SETTINGS
from sla_cli.src.cli.utils import kwargs_to_dataclass, default_from_context
from sla_cli.src.cli.converters import match_datasets_cb

logger = logging.getLogger(__name__)


@dataclass
class OrganiseParameters:
    datasets: List[str]
    directory: str
    include: List[str]
    exclude: List[str]


@click.command(**COMMAND_CONTEXT_SETTINGS, short_help="Organises datasets into train/validation/splits.")
@click.argument("datasets", type=click.STRING, callback=match_datasets_cb, nargs=-1)
@click.option("-d", "--directory", type=click.STRING, cls=default_from_context("data_directory"), help="The destination directory for the downloaded content. Default is the current work directory.")
@click.option("-i", "--include", type=click.STRING, multiple=True, default=None, help="Used to exclude specific classes in the data. Option in mutually exclusive to '-e/--exclude'.")
@click.option("-e", "--exclude", type=click.STRING, multiple=True, default=None, help="Used to include specific classes in the data. Option in mutually exclusive to '-i/--include'.")
@kwargs_to_dataclass(OrganiseParameters)
@click.pass_context
def organise(ctx: Context, params: OrganiseParameters):
    if all([params.include, params.exclude]):
        raise BadOptionUsage("include", f"'-i/--include' and '-e/--exclude' switches cannot be used together.")

