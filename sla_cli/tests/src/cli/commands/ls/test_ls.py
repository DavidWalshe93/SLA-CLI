"""
Author:     David Walshe
Date:       07 April 2021
"""

import os
import pytest

from sla_cli.entry import cli

from sla_cli.src.common.path import Path


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
                             "--output-file"
                         ])
def test_ls_save(output, cli_runner, read_actual_csv, dataset_names_csv, tmpdir, caplog):
    """
    :GIVEN: Nothing.
    :WHEN:  Using the 'ls' command to view the available datasets.
    :THEN:  Verify the correct output is saved to disk.
    """
    with tmpdir.as_cwd():
        res = cli_runner.invoke(cli, ["-d", "ls", "-o", "test.csv"])
        print(res.exc_info)

        actual = read_actual_csv()

        assert res.exit_code == 0
        assert actual == dataset_names_csv


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
                             ("-v", "--output-file"),
                             ("--verbose", "-o"),
                             ("--verbose", "--output-file"),
                         ])
def test_ls_totals_save(verbose, output, cli_runner, dataset_names_totals_csv, tmpdir):
    """
    :GIVEN: The verbose switch == '-v/--verbose totals'.
    :WHEN:  Using the 'ls' command to view the available datasets and their totals.
    :THEN:  Verify the correct output is saved to disk.
    """
    import os
    with tmpdir.as_cwd():
        res = cli_runner.invoke(cli, ["ls", verbose, "totals", output, "test.csv"])

        with open("./test.csv") as fh:
            actual = fh.read()

        assert actual == dataset_names_totals_csv
        assert res.exit_code == 0


@pytest.mark.parametrize("switch",
                         [
                             "-v",
                             "--verbose"
                         ])
def test_ls_all_print(switch, cli_runner, dataset_names_all_print):
    """
    :GIVEN: The verbose switch == '-v/--verbose all'.
    :WHEN:  Using the 'ls' command to view the available datasets and all their available data distributions.
    :THEN:  Verify the correct output is seen in the tests.
    """
    res = cli_runner.invoke(cli, ["ls", switch, "all"])

    assert res.output == dataset_names_all_print
    assert res.exit_code == 0


@pytest.mark.parametrize("verbose, output",
                         [
                             ("-v", "-o"),
                             ("-v", "--output-file"),
                             ("--verbose", "-o"),
                             ("--verbose", "--output-file"),
                         ])
def test_ls_all_save(verbose, output, cli_runner, dataset_names_all_csv, tmpdir):
    """
    :GIVEN: The verbose switch == '-v/--verbose all'.
    :WHEN:  Using the 'ls' command to view the available datasets and all their available data distributions.
    :THEN:  Verify the correct output is saved to disk.
    """
    with tmpdir.as_cwd():
        res = cli_runner.invoke(cli, ["ls", verbose, "all", output, "test.csv"])

        with open("./test.csv") as fh:
            actual = fh.read()

        assert actual == dataset_names_all_csv
        assert res.exit_code == 0


def test_ls_legend(cli_runner, legend_print, tmpdir):
    """
    :GIVEN: The '--legend' flag switch.
    :WHEN:  Using the 'ls' command to view the abbreviation legend.
    :THEN:  Verify the correct output is seen on the console.
    """
    res = cli_runner.invoke(cli, ["ls", "--legend"])

    assert res.output == legend_print
    assert res.exit_code == 0


@pytest.mark.parametrize("verbose",
                         [
                             "-v",
                             "--verbose"
                         ])
def test_ls_info(verbose, cli_runner, info_print):
    """
    :GIVEN: The '--legend' flag switch.
    :WHEN:  Using the 'ls' command to view the abbreviation legend.
    :THEN:  Verify the correct output is seen on the console.
    """
    res = cli_runner.invoke(cli, ["ls", verbose, "info"])

    assert res.output == info_print
    assert res.exit_code == 0
