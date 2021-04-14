"""
Author:     David Walshe
Date:       14 April 2021
"""

import pytest

from sla_cli.entry import cli


def test_include_exclude_mutually_exclusive(cli_runner, caplog):
    """
    :GIVEN: A include and exclude option input.
    :WHEN:  Looking to include and exclude at the same time.
    :THEN:  Verify an error is raised, flagging the two switches being used at the same time.
    """
    res = cli_runner.invoke(cli, ["organise", "-i", "py", "-e", "test"])

    assert res.exit_code == 2
    assert res.output == "Usage: cli organise [OPTIONS] [DATASETS]...\n" \
                         "\n" \
                         "Error: '-i/--include' and '-e/--exclude' switches cannot be used together.\n"
