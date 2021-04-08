"""
Author:     David Walshe
Date:       08 April 2021
"""

import logging

from src.db.accessors import Datasets, Abbreviations

logger = logging.getLogger(__name__)


class AccessorFactory:
    """
    Accessor Factory Class.
    """

    @property
    def datasets(self) -> Datasets:
        return Datasets()

    @property
    def abbrev(self) -> Abbreviations:
        return Abbreviations()
