"""
Author:     David Walshe
Date:       10 April 2021
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
class DownloadParameters:
    pass


@click.command(**COMMAND_CONTEXT_SETTINGS, short_help="Downloads available datasets.")
@kwargs_to_dataclass(DownloadParameters)
@init_colorama
def download(params: DownloadParameters):
    print("I am here")
