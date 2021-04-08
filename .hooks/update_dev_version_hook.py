"""
Author:     David Walshe
Date:       08 April 2021

Git Hook to update the micro version of the tool each time a push is made.
"""

import os
import logging
from packaging.version import parse, Version
import json
from typing import Dict

logger = logging.getLogger(__name__)


def version_file_path() -> str:
    """
    Returns the version file path.
    """
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), ".versioning.json")


def read_versioning_file() -> Dict[str, any]:
    """
    Reads the version file contents.

    :return: The contents of the version file.
    """
    with open(version_file_path()) as fh:
        return json.load(fh)


def write_versioning_file(content: Dict[str, any]) -> None:
    """
    Writes the versioning file out to disk.

    :param content: The content to write to the versioning file.
    """
    with open(version_file_path(), "w") as fh:
        return json.dump(content, fh, indent=4)


def update_micro_version() -> None:
    """
    Updates the micro version in the release string.
    """
    # Get current version number.
    content = read_versioning_file()

    # Update version.
    version = parse(content["version"])
    content["version"] = Version(f"{version.major}.{version.minor}.{version.micro + 1}").__str__()

    # Write new version back to file.
    write_versioning_file(content)


if __name__ == '__main__':
    update_micro_version()
