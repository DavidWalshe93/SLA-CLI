"""
Author:     David Walshe
Date:       10 April 2021
"""

import logging
from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)


class Downloader(metaclass=ABCMeta):

    def __init__(self, url: str):
        """
        Base class for downloaders.

        :param url: The url to the download resource.
        """
        self.url = url

    @abstractmethod
    def download(self):
        pass
