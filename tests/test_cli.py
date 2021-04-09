"""
Author:     David Walshe
Date:       07 April 2021
"""

import pytest

from src.cli import cli

from src.common.versioning import __version__


@pytest.mark.parametrize("switch",
                         [
                             "-v",
                             "--version"
                         ])
def test_version(switch, cli_runner, caplog):
    """
    :GIVEN: Nothing.
    :WHEN:  Checking the version of the tool.
    :THEN:  Check the correct output is observed.
    """
    res = cli_runner.invoke(cli, [switch])

    assert res.output.strip() == f"Version: {__version__()}"
    assert res.exit_code == 0
