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
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class VersionInfo:
    line_index: int
    version: Version


def version_file_path() -> str:
    """
    Returns the version file path.
    """
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "sla_cli", "__init__.py")


def read_meta_file() -> Dict[str, any]:
    """
    Reads the version file contents.

    :return: The contents of the version file.
    """
    with open(version_file_path()) as fh:
        return fh.readlines()


def increment_micro_version(version_info: VersionInfo):
    """
    Update the micro version by 1.

    :param version: The current version.
    :return: The incremented version.
    """
    version = parse(version_info.version)

    print(version)

    return Version(f"{version.major}.{version.minor}.{version.micro + 1}").__str__()


def write_versioning_file(content: Dict[str, any]) -> None:
    """
    Writes the versioning file out to disk.

    :param content: The content to write to the versioning file.
    """
    with open(version_file_path(), "w") as fh:
        fh.write("".join(content))
        fh.write("\n")


def get_value(value: str) -> str:
    """Get the value of a given configuration line."""
    return (value
            .split("=")[1]
            .strip()
            .replace("'", "")
            .replace('"', ""))


def update_micro_version() -> None:
    """
    Updates the micro version in the release string.
    """
    # Get current version number.
    content = read_meta_file()

    version_info = [VersionInfo(idx, get_value(line)) for idx, line in enumerate(content) if "__version__" in line][0]
    print(version_info)
    version = increment_micro_version(version_info)

    content[version_info.line_index] = f"__version__ = '{version}'"

    # Write new version back to file.
    write_versioning_file(content)


if __name__ == '__main__':
    update_micro_version()
