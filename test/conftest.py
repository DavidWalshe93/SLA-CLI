"""
Author:     David Walshe
Date:       07 April 2021
"""

import pytest

from click.testing import CliRunner


def cli_runner() -> CliRunner:
    """Returns a Click CLI Runner object."""
    return CliRunner()
