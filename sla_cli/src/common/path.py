"""
Author:     David Walshe
Date:       07 April 2021
"""

import logging
import os

logger = logging.getLogger(__name__)


class Path:

    @staticmethod
    def project_root() -> str:
        """Returns the root project path."""
        current_dir = os.path.dirname(__file__)

        for _ in range(2):
            current_dir = os.path.dirname(current_dir)

        return current_dir

    @staticmethod
    def src_root() -> str:
        """Returns the src root path."""
        return os.path.join(Path.project_root(), "src")

    @staticmethod
    def db_dir() -> str:
        """Returns the path to the DB file."""
        return os.path.join(Path.project_root(), "db")

    @staticmethod
    def db() -> str:
        """Returns the path to the DB file."""
        return os.path.join(Path.db_dir(), "db.json")

    @staticmethod
    def isic_metadata() -> str:
        """Returns the path to the ISIC metadata CSV file."""
        return os.path.join(Path.db_dir(), "isic_metadata.csv")
