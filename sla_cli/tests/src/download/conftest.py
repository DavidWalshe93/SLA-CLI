"""
Author:     David Walshe
Date:       10 April 2021
"""

import pytest
from unittest.mock import MagicMock
from contextlib import contextmanager

from requests import Session

from sla_cli.src.download import DownloaderOptions
from sla_cli.src.common.config import Config, Isic


@pytest.fixture
def session():
    """Returns a requests session object."""
    return Session()


@pytest.fixture
def downloader_options_factory(tmpdir):
    """Returns a DownloaderOptions Object"""

    config = MagicMock(spec=Config)
    config.isic = MagicMock(spec=Isic)
    config.isic.batch_size = 10
    config.isic.max_workers = 5

    def make(**kwargs):
        with tmpdir.as_cwd():
            return DownloaderOptions(
                url=kwargs.get("url", "http://www.fake_url.test"),
                destination_directory=str(tmpdir),
                config=config,
                force=kwargs.get("force", False),
                dataset=kwargs.get("dataset", "fake_dataset"),
                metadata_as_name=kwargs.get("metadata_as_name", False),
                size=kwargs.get("size", False),
                clean=kwargs.get("clean", False),
                skip=kwargs.get("skip", False),
            )

    return make
