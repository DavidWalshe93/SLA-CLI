"""
Author:     David Walshe
Date:       07 April 2021
"""

import pytest

from sla_cli import cli


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
    cli_runner.invoke(cli, [switch])

    assert caplog.messages[0] == "Version: 0.0.1"
