"""
Author:     David Walshe
Date:       07 April 2021
"""

import logging
import os

logger = logging.getLogger(__name__)


class Path:

    @staticmethod
    def root_dir():
        """Returns the root project path."""
        current_dir = os.path.dirname(__file__)

        for i in range(2):
            current_dir = os.path.dirname(current_dir)

        return current_dir
