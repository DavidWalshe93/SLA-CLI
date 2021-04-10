"""
Author:     David Walshe
Date:       10 April 2021
"""

import logging

from requests import Session

from sla_cli.src.common.path import Path
from sla_cli.src.download import inject_http_session, Downloader
from sla_cli.src.download.isic.metadata import IsicMetadataDownloader

logger = logging.getLogger(__name__)


def requires_isic_metadata(func):
    """Check if the ISIC metadata is available, if not download it."""

    @wraps(func)
    def requires_isic_metadata_wrapper(obj, *args, **kwargs):
        # Download metadata to DB folder before attempting image download.
        IsicMetadataDownloader(objs.url, destination_directory=Path.db_dir()).download()

        return func(*args, **kwargs)

    return requires_isic_metadata_wrapper


class IsicImageDownloader(Downloader):

    @inject_http_session
    def download(self, session: Session, destination_directory: str, **kwargs):
        pass

    def _get_image_ids(self):
        metadata
