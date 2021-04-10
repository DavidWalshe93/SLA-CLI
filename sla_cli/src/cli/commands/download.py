"""
Author:     David Walshe
Date:       10 April 2021
"""

import logging
import os
from typing import List
from dataclasses import dataclass, asdict

import click
from click import Context

from sla_cli.src.common.console import init_colorama

from sla_cli.src.cli.context import COMMAND_CONTEXT_SETTINGS
from sla_cli.src.cli.utils import kwargs_to_dataclass
from sla_cli.src.db.accessors import AccessorFactory

from sla_cli.src.download.isic.metadata import IsicMetadataDownloader

logger = logging.getLogger(__name__)


@dataclass
class DownloadParameters:
    datasets: List[str]
    directory: str


@click.command(**COMMAND_CONTEXT_SETTINGS, short_help="Downloads available datasets.")
@click.argument("datasets", type=click.STRING, nargs=-1)
@click.option("-d", "--directory", type=click.STRING, default=os.getcwd(), help="The destination directory for the download.")
@kwargs_to_dataclass(DownloadParameters)
@click.pass_context
def download(ctx: Context, params: DownloadParameters):
    datasets = AccessorFactory.create_datasets()
    for dataset in params.datasets:
        downloader = {
            "isic_meta": IsicMetadataDownloader(datasets.datasets["ham10000"].info.download[0])
        }.get(dataset, lambda **kw: logger.warning(f"Dataset '{dataset}' does not exist, skipping..."))

        downloader.download(destination_directory=params.directory)
