"""
Author:     David Walshe
Date:       07 April 2021
"""

import pytest

from cli import cli


def test_version(cli_runner, caplog):
    result = cli_runner.invoke(cli, ["--version"])

    assert caplog.messages[0] == "Version: 0.0.1"

