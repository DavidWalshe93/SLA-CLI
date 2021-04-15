"""
Author:     David Walshe
Date:       07 April 2021
"""
import os

import pytest
import logging

from click.testing import CliRunner
from sla_cli.entry import cli as _cli


def res_dir() -> str:
    """Returns the path to the resource directory."""
    return os.path.join(os.path.dirname(__file__), "res")


def get_resource(*args) -> str:
    """Returns the path to a resource."""
    return os.path.join(res_dir(), *args)


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


@pytest.fixture
def make_metadata(tmpdir) -> callable:
    """Creates a callback to create metadata files."""

    def make(dataset: str) -> str:
        data_dir = tmpdir.mkdir(dataset)
        meta_file = data_dir.join("metadata.csv")
        with open(get_resource("metadata.csv")) as fh:
            meta_file.write(fh.read())

        return str(meta_file)

    return make
