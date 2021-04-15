"""
Author:     David Walshe
Date:       14 April 2021
"""
import logging

import pandas as pd
import pytest

from sla_cli.entry import cli

import sla_cli.src.cli.commands.organise as sut


def test_include_exclude_mutually_exclusive(cli_runner, caplog):
    """
    :GIVEN: A include and exclude option input.
    :WHEN:  Looking to include and exclude at the same time.
    :THEN:  Verify an error is raised, flagging the two switches being used at the same time.
    """
    caplog.set_level(logging.CRITICAL)
    res = cli_runner.invoke(cli, ["organise", "-i", "py", "-e", "test"])

    assert res.exit_code == 2
    assert res.output.find("Usage: cli organise [OPTIONS] [DATASETS]...\n"
                           "\n"
                           "Error: '-i/--include' and '-e/--exclude' switches cannot be used together.\n") > -1

    caplog.set_level(logging.INFO)


def test_read_metadata(make_metadata):
    """
    :GIVEN: A metadata file path.
    :WHEN:  Loading the metadata from disk.
    :THEN:  Verify the metafile loaded as expected.
    """
    metadata_file = make_metadata("uda_1")

    actual = sut.read_metadata(metadata_file)

    assert type(actual) == pd.DataFrame
    assert actual.shape[0] == 1000


def test_read_metadata_fail(caplog):
    """
    :GIVEN: A non-existent metadata path.
    :WHEN:  Loading the metadata from disk.
    :THEN:  Verify a SystemExit was raised.
    """
    non_existant_path = "foo/bar/roo"

    with pytest.raises(SystemExit):
        sut.read_metadata(non_existant_path)

    assert caplog.messages[-1] == f"Could not find 'metadata.csv' in {non_existant_path}.\n\nNote: Don't use the --metadata-as-name switch when downloading if using the data for automated processes."


def test_gather_metadata(monkeypatch):
    """
    :GIVEN: A data directory, datasets and what datasets are available on disk. 
    :WHEN:  Gathering various datasets metadata.
    :THEN:  Verify the correct types are returned and no errors were raised.
    """
    available_datasets = ["uda_1", "uda_2"]
    datasets = available_datasets

    monkeypatch.setattr(sut, "read_metadata", lambda _: pd.DataFrame())

    actual = sut.gather_metadata("", datasets, available_datasets)

    assert type(actual) == list
    assert type(actual[0]) == pd.DataFrame


def test_gather_metadata_fail(monkeypatch, caplog):
    """
    :GIVEN: A data directory, datasets and what datasets are available on disk.
    :WHEN:  Gathering various datasets metadata.
    :THEN:  Verify an error is raised due to a dataset not being available on disk.
    """
    available_datasets = ["uda_1", "uda_2"]
    datasets = ["uda_1", "uda_2", "msk_1"]

    monkeypatch.setattr(sut, "read_metadata", lambda _: pd.DataFrame())

    with pytest.raises(SystemExit):
        sut.gather_metadata("", datasets, available_datasets)

    assert caplog.messages[-1] == f"Missing data for 'msk_1', use 'sla-cli download <DATASET>' to continue."
