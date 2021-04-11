"""
Author:     David Walshe
Date:       10 April 2021
"""

import logging
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from functools import wraps

from requests import Session

from sla_cli.src.common.config import Config
from sla_cli.src.download.utils import inject_http_session

logger = logging.getLogger(__name__)


@dataclass
class DownloaderOptions:
    """Common options for a Downloader class."""
    destination_directory: str
    config: Config
    force: bool
    metadata_as_name: bool
    url: str = ""
    dataset: str = ""



class Downloader(metaclass=ABCMeta):

    def __init__(self, options: DownloaderOptions):
        """
        Base class for downloaders.

        :param url: The url to the download resource.
        :param destination_directory: The directory to same the download to.
        """
        self.options = options

    @abstractmethod
    def download(self, session: Session):
        pass

    @property
    def url(self) -> str:
        return self.options.url

    @property
    def dataset_name(self) -> str:
        return self.options.dataset.upper()

    @property
    def destination_directory(self) -> str:
        return self.options.destination_directory

    @property
    def force(self) -> bool:
        return self.options.force

    @property
    def unzip(self) -> bool:
        return self.options.config.unzip

    @property
    def convert(self) -> str:
        return self.options.config.convert

    @property
    def config(self) -> Config:
        return self.options.config


class DummyDownloader(Downloader):

    @inject_http_session
    def download(self, session: Session, **kwargs):
        logger.warning(f"No downloader suitable for dataset '{self.dataset_name}', skipping...")
