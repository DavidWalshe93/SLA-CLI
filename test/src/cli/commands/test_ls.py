"""
Author:     David Walshe
Date:       07 April 2021
"""

import pytest

from cli import cli


def test_ls_print(cli_runner, dataset_names_print):
    """
    :GIVEN: Nothing.
    :WHEN:  Using the 'ls' command to view the available datasets.
    :THEN:  Verify the correct output is seen in the tests.
    """
    res = cli_runner.invoke(cli, ["ls"])

    assert res.output == dataset_names_print
    assert res.exit_code == 0


@pytest.mark.parametrize("output",
                         [
                             "-o",
                             "--output"
                         ])
def test_ls_save(output, cli_runner, read_actual_csv, dataset_names_csv, tmpdir):
    """
    :GIVEN: Nothing.
    :WHEN:  Using the 'ls' command to view the available datasets.
    :THEN:  Verify the correct output is seen in the tests.
    """
    with tmpdir.as_cwd():
        res = cli_runner.invoke(cli, ["ls", output, "test.csv"])

        actual = read_actual_csv()

        assert actual == dataset_names_csv
        assert res.exit_code == 0


@pytest.mark.parametrize("switch",
                         [
                             "-v",
                             "--verbose"
                         ])
def test_ls_totals_print(switch, cli_runner, dataset_names_totals_print):
    """
    :GIVEN: The verbose switch == '-v/--verbose totals'.
    :WHEN:  Using the 'ls' command to view the available datasets and their totals.
    :THEN:  Verify the correct output is seen in the tests.
    """
    res = cli_runner.invoke(cli, ["ls", switch, "totals"])

    assert res.output == dataset_names_totals_print
    assert res.exit_code == 0


@pytest.mark.parametrize("verbose, output",
                         [
                             ("-v", "-o"),
                             ("-v", "--output"),
                             ("--verbose", "-o"),
                             ("--verbose", "--output"),
                         ])
def test_ls_totals_save(verbose, output, cli_runner, dataset_names_totals_csv, tmpdir):
    """
    :GIVEN: The verbose switch == '-v/--verbose totals'.
    :WHEN:  Using the 'ls' command to view the available datasets and their totals.
    :THEN:  Verify the correct output is seen in the tests.
    """
    import os
    with tmpdir.as_cwd():
        res = cli_runner.invoke(cli, ["ls", verbose, "totals", output, "test.csv"])

        with open("./test.csv") as fh:
            actual = fh.read()

        assert actual == dataset_names_totals_csv
        assert res.exit_code == 0
