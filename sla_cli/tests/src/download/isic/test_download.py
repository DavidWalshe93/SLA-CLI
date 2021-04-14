"""
Author:     David Walshe
Date:       11 April 2021
"""
import os

import pandas as pd
import pytest
from unittest.mock import patch

import httpretty
from httpretty import register_uri

import sla_cli.src.download.isic.download as sut


@pytest.fixture
def mock_get_metadata(monkeypatch):
    """Mocks the '_get_metadata' method on IsicImageDownloader."""
    monkeypatch.setattr(sut.IsicImageDownloader, "_get_metadata", lambda x: None)


@pytest.fixture
def metadata_file():
    """Returns a path to a mock metadata file."""
    return os.path.join(os.path.dirname(__file__), "res", "sample.csv")


@pytest.fixture
def metadata(metadata_file: str):
    """Returns a pandas dataframe of metadata."""
    return pd.read_csv(metadata_file)


@pytest.mark.parametrize("data, batch_size, expected",
                         [
                             ([i for i in range(1000)], 200, 5),
                             ([i for i in range(1000)], 100, 10),
                             ([i for i in range(1000)], 500, 2),
                             ([i for i in range(1000)], 1000, 1),
                             ([i for i in range(1000)], 1500, 1),
                         ])
def test_make_batches(data, batch_size, expected):
    """
    :GIVEN: A list of data and a batch size, 'n'.
    :WHEN:  Creating batches from a list of data of size 'n'
    :THEN:  Verify the correct number of batches is created.
    """
    actual = sut.make_batches(data, batch_size)

    assert len(list(actual)) == expected


@pytest.mark.parametrize("dataset, size",
                         [
                             ('BCN_2020_Challenge', 2),
                             ('SONIC', 4),
                             ('ISIC_2020_Vienna_part_1', 1),
                             ('ISIC 2020 Challenge - MSKCC contribution', 6),
                             ('ISIC_2020_Vienna_part2', 1),
                             ('BCN_20000', 5),
                             ('Brisbane ISIC Challenge 2020', 1),
                         ])
def test_get_metadata(dataset, size, metadata_file, downloader_options_factory, monkeypatch):
    """
    :GIVEN: A dataset name.
    :WHEN:  Gathering the metadata for a given dataset.
    :THEN:  Verify that the correct number of instances is returned.
    """
    downloader_options = downloader_options_factory(dataset=dataset)

    # Mock decorator.
    with patch("sla_cli.src.download.isic.metadata._download_isic_metadata", autospec=True) as mock:
        # Mock location to database file.
        monkeypatch.setattr(sut.Path, "isic_metadata", lambda: metadata_file)

        downloader = sut.IsicImageDownloader(downloader_options)

        df = downloader._get_metadata()

        assert df.shape[0] == size

        # Assert function was mocked correctly.
        mock.assert_called_with(downloader)


@pytest.mark.parametrize("dataset",
                         [
                             "ham10000",
                             "uda-1",
                             "bcn_20000",
                             "msk-1",
                         ])
def test_create_download_path(dataset, downloader_options_factory, tmpdir, caplog, mock_get_metadata):
    """
    :GIVEN: A dataset name.
    :WHEN:  Creating the destination directory for downloads.
    :THEN:  Verify the directory is created.
    """
    with tmpdir.as_cwd():
        expected_path = os.path.join(os.getcwd(), dataset)
        assert os.path.exists(expected_path) == False

        downloader_options = downloader_options_factory(dataset=dataset)

        sut.IsicImageDownloader(downloader_options)

        assert os.path.exists(expected_path) == True

        assert caplog.messages[-1] == f"Created the download directory at: '{expected_path}'"


@pytest.mark.parametrize("dataset",
                         [
                             "ham10000",
                             "uda-1",
                             "bcn_20000",
                             "msk-1",
                         ])
def test_create_download_path_already_exists(dataset, downloader_options_factory, tmpdir, caplog, mock_get_metadata):
    """
    :GIVEN: A dataset name.
    :WHEN:  Creating the destination directory for downloads when the destination already exists.
    :THEN:  Verify the the download is skipped.
    """
    with tmpdir.as_cwd():
        expected_path = os.path.join(os.getcwd(), dataset)
        # Make path.
        os.mkdir(expected_path)
        # Ensure path already exists.
        assert os.path.exists(expected_path) == True

        downloader_options = downloader_options_factory(dataset=dataset)

        downloader = sut.IsicImageDownloader(downloader_options)

        assert downloader.download_path == None

        assert caplog.messages[-3] == f"{downloader_options.dataset} already exists at the destination directory '{expected_path}'"
        assert caplog.messages[-2] == f"If you wish to re-download the dataset, try 'sla-cli download -f/--force <DATASET>'"
        assert caplog.messages[-1] == f"Skipping..."


@pytest.mark.parametrize("dataset",
                         [
                             "ham10000",
                             "uda-1",
                             "bcn_20000",
                             "msk-1",
                         ])
def test_create_download_path_already_exists_force(dataset, downloader_options_factory, tmpdir, caplog, mock_get_metadata):
    """
    :GIVEN: A dataset name.
    :WHEN:  Creating the destination directory for downloads when the destination already exists with the force swithc set.
    :THEN:  Verify the destination directory is deleted and recreated.
    """
    with tmpdir.as_cwd():
        expected_path = os.path.join(os.getcwd(), dataset)
        # Make path.
        os.mkdir(expected_path)
        # Ensure path already exists.
        assert os.path.exists(expected_path) == True

        downloader_options = downloader_options_factory(dataset=dataset, force=True)

        downloader = sut.IsicImageDownloader(downloader_options)

        assert downloader.download_path == expected_path

        assert os.path.exists(expected_path) == True

        assert caplog.messages[-3] == f"'-f/--force' flag set, deleting directory: '{expected_path}'"
        assert caplog.messages[-2] == f"Deletion successful."
        assert caplog.messages[-1] == f"Created the download directory at: '{expected_path}'"


def test_image_ids(metadata, downloader_options_factory, mock_get_metadata):
    """
    :GIVEN: A metadata file.
    :WHEN:  Retrieving a list of the metadata 'isic_id' fields.
    :THEN:  Verify the correct number of ids are returned and match the items expected.
    """
    download_options = downloader_options_factory()

    downloader = sut.IsicImageDownloader(download_options)

    downloader.metadata = metadata

    assert len(downloader.image_ids) == 20
    assert downloader.image_ids == list(metadata["isic_id"])

# todo Complete ISIC downloader tests.
