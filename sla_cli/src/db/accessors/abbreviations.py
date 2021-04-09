"""
Author:     David Walshe
Date:       08 April 2021
"""

import logging

from tabulate import tabulate

from sla_cli.src.db.accessors.base import Accessor

logger = logging.getLogger(__name__)


class Abbreviations(Accessor):

    def abbreviations(self, tablefmt: str = "simple") -> str:
        """Returns the abbreviation table."""
        return tabulate([(abbrev, dataset) for dataset, abbrev in self.db.abbrev.items()], headers=["Abbrev.", "Diagnosis"], tablefmt=tablefmt)
