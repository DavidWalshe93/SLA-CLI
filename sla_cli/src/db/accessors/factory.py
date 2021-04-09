"""
Author:     David Walshe
Date:       08 April 2021
"""

import logging

from sla_cli.src.db.accessors import Datasets, Abbreviations

logger = logging.getLogger(__name__)


class AccessorFactory:
    """
    Accessor Factory Class.
    """

    @staticmethod
    def create_datasets() -> Datasets:
        """Returns a dataset object."""
        return Datasets()

    @staticmethod
    def create_abbreviation() -> Abbreviations:
        """Returns an abbreviations object."""
        return Abbreviations()
