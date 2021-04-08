"""
Author:     David Walshe
Date:       08 April 2021
"""

import os
import logging
from packaging.version import parse, Version
import json
from typing import Dict

logger = logging.getLogger(__name__)


def read_versioning_file(file_path: str) -> Dict[str, any]:
    """
    Reads the version file contents.

    :param file_path: The path to the version file.
    :return: The contents of the version file.
    """
    with open(file_path) as fh:
        return json.load(fh)


def write_versioning_file(file_path: str, content: Dict[str, any]) -> None:
    """
    Writes the versioning file out to disk.

    :param file_path: The path to the version file.
    :param content: The content to write to the versioning file.
    """
    with open(file_path, "w") as fh:
        return json.dump(content, fh, indent=4)


def update_micro_version() -> None:
    """
    Updates the micro version in the release string.
    """
    # Create the path to the version file.
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".versioning.json")

    # Get current version number.
    content = read_versioning_file(file_path)

    # Update version.
    version = parse(content["version"])
    content["version"] = Version(f"{version.major}.{version.minor}.{version.micro + 1}").__str__()

    # Write new version back to file.
    write_versioning_file(file_path, content)


print(update_micro_version())
