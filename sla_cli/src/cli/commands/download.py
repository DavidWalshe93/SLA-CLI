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

from sla_cli.src.cli.context import COMMAND_CONTEXT_SETTINGS
from sla_cli.src.cli.utils import kwargs_to_dataclass, default_from_context
from sla_cli.src.db.accessors import AccessorFactory
from sla_cli.src.download import Downloader, DownloaderOptions, DummyDownloader

from sla_cli.src.download.isic import IsicMetadataDownloader, IsicImageDownloader
from sla_cli.src.download.ph2 import Ph2Downloader
from sla_cli.src.download.pad_ufes_20 import PadUfes20Downloader
from sla_cli.src.download.mednode import MednodeDownloader

logger = logging.getLogger(__name__)


@dataclass
class DownloadParameters:
    datasets: List[str]
    directory: str
    force: bool
    clean: bool
    skip: bool
    metadata_as_name: bool
    isic_meta: bool


@click.command(**COMMAND_CONTEXT_SETTINGS, short_help="Downloads available datasets.")
@click.argument("datasets", type=click.STRING, nargs=-1)
@click.option("-d", "--directory", type=click.STRING, cls=default_from_context("data_directory"), help="The destination directory for the downloaded content. Default is the current work directory.")
@click.option("-f", "--force", type=click.BOOL, is_flag=True, help="Force download a dataset, even if it already exists on the filesystem.")
@click.option("-c", "--clean", type=click.BOOL, is_flag=True, help="Remove archive files directly after extraction.")
@click.option("-s", "--skip", type=click.BOOL, is_flag=True, help="Skip the download phase, useful for running builds on previously downloaded archives.")
@click.option("--isic-meta", type=click.BOOL, is_flag=True, help="Download the ISIC Archive metadata instead of a dataset.")
@click.option("--metadata-as-name", type=click.BOOL, is_flag=True, help="Saves the dataset metadata as the dataset name. Helpful for viewing in excel, not optimal for ML pipelines.")
@kwargs_to_dataclass(DownloadParameters)
@click.pass_context
def download(ctx: Context, params: DownloadParameters):
    datasets = AccessorFactory.create_datasets()

    # Remove datasets that dont exist in the tool before continuing.
    keep = []
    for dataset in params.datasets:
        if dataset in datasets.datasets.names:
            keep.append(dataset)
        else:
            logger.warning(f"'{dataset}' does not exist for download, removing...")

    params.datasets = keep

    options = DownloaderOptions(
        destination_directory=params.directory,
        config=ctx.obj,
        force=params.force,
        metadata_as_name=params.metadata_as_name,
        clean=params.clean,
        skip=params.skip
    )

    # Download only the ISIC metadata.
    if params.isic_meta:
        options.url = datasets.datasets["ham10000"].info.download[0]
        IsicMetadataDownloader(options=options)
    else:
        size = sum([datasets.datasets[dataset].info.size for dataset in params.datasets])
        logger.info(f"Total size of requested download: {size} MB.")

        for dataset in params.datasets:
            # Get the downloader object for the given dataset.
            downloader = downloader_factory(dataset)

            # Add dataset to options.
            options.dataset = dataset
            options.url = datasets.datasets[dataset].info.download[0]
            options.size = datasets.datasets[dataset].info.size

            # Download the dataset.
            downloader = downloader(options=options)

            downloader.download()


def downloader_factory(dataset) -> Downloader:
    """
    Creates a downloader depending on the dataset name based.

    :param dataset: The dataset name to create a downloader for.
    :return: A Downloader object suited for the specified dataset.
    """
    return {
        "bcn_20000": IsicImageDownloader,
        "bcn_2020_challenge": IsicImageDownloader,
        "brisbane_isic_challnge_2020": IsicImageDownloader,
        "dermoscopedia_cc_by": IsicImageDownloader,
        "ham10000": IsicImageDownloader,
        "isic_2020_challenge_mskcc_contribution": IsicImageDownloader,
        "isic_2020_vienna_part_1": IsicImageDownloader,
        "isic_2020_vienna_part_2": IsicImageDownloader,
        "jid_editorial_images_2018": IsicImageDownloader,
        "mednode": MednodeDownloader,
        "msk_1": IsicImageDownloader,
        "msk_2": IsicImageDownloader,
        "msk_3": IsicImageDownloader,
        "msk_4": IsicImageDownloader,
        "msk_5": IsicImageDownloader,
        "pad_ufes_20": PadUfes20Downloader,
        "ph2": Ph2Downloader,
        "sonic": IsicImageDownloader,
        "sydney_mia_smdc_2020_isic_challenge_contribution": IsicImageDownloader,
        "uda_1": IsicImageDownloader,
        "uda_2": IsicImageDownloader,
    }.get(
        dataset,
        DummyDownloader
    )



