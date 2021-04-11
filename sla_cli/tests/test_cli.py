"""
Author:     David Walshe
Date:       07 April 2021
"""

import pytest

from sla_cli.entry import cli

from sla_cli.src.common.versioning import get_version


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

    assert res.output.split("-")[-1].strip() == f"Version: {get_version()}"
    assert res.exit_code == 0
