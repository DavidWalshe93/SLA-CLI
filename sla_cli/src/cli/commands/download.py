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

from sla_cli.src.download.isic import IsicMetadataDownloader, IsicImageDownloader

logger = logging.getLogger(__name__)


@dataclass
class DownloadParameters:
    datasets: List[str]
    directory: str
    force: bool
    isic_meta: bool


@click.command(**COMMAND_CONTEXT_SETTINGS, short_help="Downloads available datasets.")
@click.argument("datasets", type=click.STRING, nargs=-1)
@click.option("-d", "--directory", type=click.STRING, default=os.getcwd(), help="The destination directory for the download.")
@click.option("-f", "--force", is_flag=True, help="Force download a dataset, even if it already exists on the filesystem.")
@click.option("--isic-meta", is_flag=True, help="Download the ISIC Archive metadata instead of a dataset.")
@kwargs_to_dataclass(DownloadParameters)
@click.pass_context
def download(ctx: Context, params: DownloadParameters):
    datasets = AccessorFactory.create_datasets()

    removals = []
    for dataset in params.datasets:
        if dataset not in datasets.datasets.names:
            logger.warning(f"'{dataset}' does not exist for download, removing...")
            removals.append(dataset)

    params.datasets = [dataset for dataset in params.datasets if dataset not in removals]

    kwargs = {
        "destination_directory": params.directory,
        "config": ctx.obj,
        "force": params.force,
    }

    # Download only the ISIC metadata.
    if params.isic_meta:
        IsicMetadataDownloader(datasets.datasets["ham10000"].info.download[0], **kwargs)
    else:
        size = sum([datasets.datasets[dataset].info.size for dataset in params.datasets])
        logger.info(f"Total size of requested download: {size} MB.")

        for dataset in params.datasets:
            # Add dataset to kwargs.
            kwargs.update({"dataset_name": convert(dataset=dataset)})

            # Get the downloader object for the given dataset.
            downloader = {
                "bcn_20000": IsicImageDownloader,
                "bcn_2020_challenge": IsicImageDownloader,
                "brisbane_isic_challnge_2020": IsicImageDownloader,
                "dermoscopedia_cc_by": IsicImageDownloader,
                "ham10000": IsicImageDownloader,
                "isic_2020_challenge_mskcc_contribution": IsicImageDownloader,
                "isic_2020_vienna_part_1": IsicImageDownloader,
                "isic_2020_vienna_part_2": IsicImageDownloader,
                "jid_editorial_images_2018": IsicImageDownloader,
                "msk_1": IsicImageDownloader,
                "msk_2": IsicImageDownloader,
                "msk_3": IsicImageDownloader,
                "msk_4": IsicImageDownloader,
                "msk_5": IsicImageDownloader,
                "sonic": IsicImageDownloader,
                "sydney_mia_smdc_2020_isic_challenge_contribution": IsicImageDownloader,
                "uda_1": IsicImageDownloader,
                "uda_2": IsicImageDownloader,
            }.get(
                dataset,
                lambda **kw: logger.warning(f"Dataset '{dataset}' does not exist, skipping...")
            )(datasets.datasets[dataset].info.download[0], **kwargs)

            if downloader is not None:
                # Download the dataset.
                downloader.download()


def convert(dataset: str) -> str:
    """Translates the CLI argument name into the Metadata value."""
    return dict(
        bcn_20000="BCN_20000",
        bcn_2020_challenge="BCN_2020_Challenge",
        brisbane_isic_challenge_2020="Brisbane ISIC Challenge 2020",
        dermoscopedia_cc_by="Dermoscopedia (CC-BY)",
        ham10000="HAM10000",
        isic_2020_challenge_mskcc_contribution="ISIC 2020 Challenge - MSKCC contribution",
        isic_2020_vienna_part_1="ISIC_2020_Vienna_part_1",
        isic_2020_vienna_part_2="ISIC_2020_Vienna_part2",
        jid_editorial_images_2018="2018 JID Editorial Images",
        msk_1="MSK-1",
        msk_2="MSK-2",
        msk_3="MSK-3",
        msk_4="MSK-4",
        msk_5="MSK-5",
        sonic="SONIC",
        sydney_mia_smdc_2020_isic_challenge_contribution="Sydney (MIA / SMDC) 2020 ISIC challenge contribution",
        uda_1="UDA-1",
        uda_2="UDA-2"
    ).get(dataset, None)
