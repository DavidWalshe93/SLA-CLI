"""
Author:     David Walshe
Date:       10 April 2021
"""

import logging
from abc import ABCMeta, abstractmethod

from requests import Session

logger = logging.getLogger(__name__)


class Downloader(metaclass=ABCMeta):

    def __init__(self, url: str, destination_directory: str):
        """
        Base class for downloaders.

        :param url: The url to the download resource.
        :param destination_directory: The directory to same the download to.
        """
        self.url = url
        self.destination_directory = destination_directory

    @abstractmethod
    def download(self, session: Session, **kwargs):
        pass
