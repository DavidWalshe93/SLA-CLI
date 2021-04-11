"""
Author:     David Walshe
Date:       07 April 2021
"""

import pytest
import logging

from click.testing import CliRunner
from sla_cli.entry import cli as _cli


@pytest.fixture(autouse=True)
def set_log_level(caplog):
    """Set the log level for the test session."""
    caplog.set_level(logging.DEBUG)


@pytest.fixture
def cli_runner() -> CliRunner:
    """Returns a Click CLI Runner object."""
    return CliRunner()


@pytest.fixture
def cli() -> callable:
    """Returns the root CLI callable command."""
    return _cli
