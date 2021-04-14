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

from sla_cli.src.cli.context import COMMAND_CONTEXT_SETTINGS
from sla_cli.src.cli.utils import kwargs_to_dataclass

logger = logging.getLogger(__name__)


@dataclass
class OrganiseParameters:
    datasets: List[str]


@click.command(**COMMAND_CONTEXT_SETTINGS, short_help="Organises datasets into train/validation/splits.")
@click.argument("datasets", type=click.STRING, nargs=-1)
# @click.option("-d", "--directory", type=click.STRING, default=os.getcwd(), help="The destination directory for the download.")
# @click.option("-f", "--force", is_flag=True, help="Force download a dataset, even if it already exists on the filesystem.")
# @click.option("-c", "--clean", is_flag=True, help="Remove archive files directly after extraction.")
# @click.option("-s", "--skip", is_flag=True, help="Skip the download phase, useful for running builds on previously downloaded archives.")
# @click.option("--isic-meta", is_flag=True, help="Download the ISIC Archive metadata instead of a dataset.")
# @click.option("--metadata-as-name", is_flag=True, help="Saves the dataset metadata as the dataset name. Helpful for viewing in excel, not optimal for ML pipelines.")
@kwargs_to_dataclass(OrganiseParameters)
@click.pass_context
def organise(ctx: Context, params: OrganiseParameters):
    pass