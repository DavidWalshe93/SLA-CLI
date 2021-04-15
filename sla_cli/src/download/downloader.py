"""
Author:     David Walshe
Date:       10 April 2021
"""

import logging
import os
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from functools import wraps
import shutil

from alive_progress import alive_bar
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
    clean: bool
    skip: bool
    metadata_as_name: bool
    url: str = ""
    dataset: str = ""
    size: float = 0


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
        return self.options.dataset.lower()

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

    @property
    def size(self) -> float:
        return self.options.size

    @property
    def skip_download(self) -> bool:
        return self.options.skip

    @property
    def clean(self) -> bool:
        return self.options.clean


def unknown_progress(title: str) -> callable:
    """
    Returns a pre-made progress bar context manager.

    :param title: The title of the progress bar.
    :param type: The type of spinner to use in the progress bar.
    :return: A progress bar context manager.
    """
    return alive_bar(None, f"[SLA] - INFO - - - {title}", unknown="stars")


class FileDownloader(Downloader, metaclass=ABCMeta):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def download(self, session: Session = None):
        """Downloads and formats a file based dataset."""

        def dont_skip_download():
            return not self.skip_download

        def archive_path_does_not_exist():
            return not os.path.exists(self.archive_path)

        # Check to see if the dataset already exists.
        if self._does_not_exist_or_forced():
            if dont_skip_download() or archive_path_does_not_exist():
                self._download()
            else:
                logger.info(f"Download skipped.")

            with unknown_progress(f"Extracting"):
                self._extract()

            # Clean-up archive file if -c/--clean is used.
            if self.clean:
                logger.info(f"Removing archive file.")
                os.remove(self.archive_path)

            with unknown_progress(f"Parsing metadata"):
                self._save_metadata()

            with unknown_progress(f"Moving images"):
                self._move_images()

            with unknown_progress(f"Cleaning up"):
                self._clean_up()

    @property
    def archive_path(self):
        """Returns the archive save path for the given dataset."""
        return os.path.join(self.destination_directory, self.__archive_name__)

    @property
    def extracted_path(self):
        """Returns the archive save path for the given dataset."""
        return os.path.join(self.destination_directory, self.__extracted_name__)

    def metadata_path(self, fmt: str = "csv"):
        """
        Returns the destination path to the metadata file.

        :param fmt: The output format for the metadata.
        """
        if self.options.metadata_as_name:
            save_name = self.dataset_name.lower().replace(" ", "_").replace("-", "_") + f".{fmt}"
            return os.path.join(self.extracted_path, f"{save_name}")
        else:
            return os.path.join(self.extracted_path, f"metadata.{fmt}")

    def _does_not_exist_or_forced(self) -> bool:
        """
        Checks if the given dataset already exists in the destination folder.

        If it does then unless -f/--force is set, skip the download.

        If -f/--force is set, delete the current contents and re-download.
        """
        if os.path.exists(self.extracted_path) and self.force:
            logger.debug(f"'-f/--force' flag set, deleting directory: '{self.extracted_path}'")
            shutil.rmtree(self.extracted_path)
            logger.debug(f"Deletion successful.")
        elif os.path.exists(self.extracted_path) and not self.force:
            logger.warning(f"{self.dataset_name} already exists at the destination directory '{self.extracted_path}'")
            logger.warning(f"If you wish to re-download the dataset, try 'sla-cli download -f/--force <DATASET>'")
            logger.warning(f"Skipping...")
            return False

        return True

    @abstractmethod
    def _download(self):
        pass

    @abstractmethod
    def _extract(self):
        pass

    @abstractmethod
    def _format_metadata(self):
        pass

    @abstractmethod
    def _save_metadata(self):
        pass

    @abstractmethod
    def _collect_images(self):
        pass

    @abstractmethod
    def _convert_images(self):
        pass

    @property
    def images_path(self):
        """Returns the destination folder for images."""
        return os.path.join(self.extracted_path, "images")

    @abstractmethod
    def _move_images(self):
        pass

    @abstractmethod
    def _clean_up(self):
        pass


class DummyDownloader(Downloader):
    """
    Dummy downloader to handle non implemented datasets gracefully.
    """

    @inject_http_session
    def download(self, session: Session, **kwargs):
        logger.warning(f"No downloader suitable for dataset '{self.dataset_name}', skipping...")
