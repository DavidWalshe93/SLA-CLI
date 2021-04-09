"""
Author:     David Walshe
Date:       08 April 2021
"""

import logging
import os
import json
from typing import Dict

logger = logging.getLogger(__name__)


def version_file_path() -> str:
    """
    Returns the version file path.
    """
    return os.path.join(os.path.dirname(__file__), "../../.versioning.json")


def read_versioning_file() -> Dict[str, any]:
    """
    Reads the version file contents.

    :return: The contents of the version file.
    """
    with open(version_file_path()) as fh:
        return json.load(fh)


def __version__() -> str:
    """Returns the current tool version"""
    return read_versioning_file()["version"]
