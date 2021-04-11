"""
Author:     David Walshe
Date:       10 April 2021
"""

import os
import json

import pandas as pd
import pytest
import httpretty
from httpretty import register_uri

from requests import Session

from sla_cli.src.download.downloader import DownloaderOptions
import sla_cli.src.download.isic.metadata as sut


@pytest.mark.parametrize("limit, offset",
                         [
                             (10, 0),
                             (1000, 0),
                             (10, 100),
                             (10000, 1000),
                         ])
def test_make_request_url(limit: int, offset: int, downloader_options_factory):
    """
    :GIVEN: A limit and offset for a request.
    :WHEN:  Creating a request URL for metadata from the ISIC archive.
    :THEN:  Verify the correct URL structure is created.
    """
    expected_url = "https://isic-archive.com/api/v1"
    downloader_options = downloader_options_factory(url=expected_url)

    expected = f"{expected_url}/image?limit={limit}&offset={offset}&sort=name&sortdir=1&detail=true"

    url_params = sut.UrlParams(limit, offset)

    assert sut.IsicMetadataDownloader(downloader_options)._make_request_url(url_params) == expected


@httpretty.activate
@pytest.mark.parametrize("url, expected",
                         [
                             ("https://isic-archive.com/api/v1/1", {"foo1": "bar1"}),
                             ("https://isic-archive.com/api/v1/2", {"foo2": "bar2"}),
                             ("https://isic-archive.com/api/v1/3", {"foo3": "bar3"})
                         ])
def test_process_request(url, expected, session):
    """
    :GIVEN: A resource API URL.
    :WHEN:  Requesting data from the API URL via GET.
    :THEN:  Verify the correct response and format is returned.
    """
    register_uri(
        httpretty.GET,
        url,
        body=json.dumps(expected)
    )

    actual = sut.IsicMetadataDownloader._process_request(session, url)

    assert actual == expected


def test_merge_record(sample_isic_records, expected_column_names):
    """
    :GIVEN: A list of lists containing ISIC archive metadata records.
    :WHEN:  Converting and merging the records into a pandas DataFrame.
    :THEN:  Verify the conversion happens as expected.
    """
    records = [sample_isic_records]
    actual = sut.IsicMetadataDownloader(None)._merge_records(records)

    assert list(actual.columns) == expected_column_names


def test_add_year_tags():
    """
    :GIVEN: A dataframe containing a 'tags' column.
    :WHEN:  Adding the year columns to a records dataframe.
    :THEN:  Verify the expected year columns are added to the dataframe.
    """
    records = pd.DataFrame(columns=["tags"])

    sut.IsicMetadataDownloader._add_year_tags(records)

    assert list(records.columns) == ["tags", *[str(year) for year in range(2016, 2021)]]


@pytest.mark.parametrize("already_downloaded",
                         [
                             True,
                             False
                         ])
def test_save_records(already_downloaded, downloader_options_factory, tmpdir, monkeypatch):
    """
    :GIVEN: A pandas dataframe.
    :WHEN:  Saving the ISIC metadata to disk.
    :THEN:  Verify that the metadata is saved.
    """
    mock_db_dir = tmpdir.mkdir("db")
    with tmpdir.as_cwd():
        monkeypatch.setattr(sut.Path, "db_dir", lambda: mock_db_dir)
        if already_downloaded:
            mock_db_dir.join("isic_metadata.csv").write("")

        records = pd.DataFrame(columns=["Test"])

        downloader_options = downloader_options_factory()

        sut.IsicMetadataDownloader(downloader_options)._save_records(records)

        assert os.path.exists(os.path.join(str(tmpdir), "isic_metadata.csv")) == True
        assert os.path.exists(os.path.join(str(mock_db_dir), "isic_metadata.csv")) == True
