"""
Author:     David Walshe
Date:       07 April 2021
"""

import pytest

from cli import cli


def test_ls(cli_runner, dataset_names):
    """
    :GIVEN: Nothing.
    :WHEN:  Using the 'ls' command to view the available datasets.
    :THEN:  Verify the correct output is seen in the tests.
    """
    res = cli_runner.invoke(cli, ["ls"])

    assert res.output == dataset_names
    assert res.exit_code == 0


@pytest.mark.parametrize("switch",
                         [
                             "-v",
                             "--verbose"
                         ])
def test_ls(switch, cli_runner, dataset_names_totals):
    """
    :GIVEN: The verbose switch == '-v/--verbose totals'.
    :WHEN:  Using the 'ls' command to view the available datasets and their totals.
    :THEN:  Verify the correct output is seen in the tests.
    """
    res = cli_runner.invoke(cli, ["ls", switch, "totals"])

    assert res.output == dataset_names_totals
    assert res.exit_code == 0

