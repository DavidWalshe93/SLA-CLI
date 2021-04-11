"""
Author:     David Walshe
Date:       10 April 2021
"""

import logging
from functools import wraps

import requests
from requests import Session

logger = logging.getLogger(__name__)


def inject_http_session(func):
    """Injects a persistent HTTP session into the wrapped function."""

    @wraps(func)
    def inject_http_session_wrapper(*args, **kwargs):
        with Session() as session:
            return func(*args, session=session, **kwargs)

    return inject_http_session_wrapper


def download_file(url, destination_path: str):
    """
    Downloads a given dataset archive found at a URL endpoint.

    :param url: The URL to download the resource from.
    :param destination_path: The destination path for the download archive.
    """
    # Download the file.
    res = requests.get(url)

    # Create save file and write out dataset content.
    with open(destination_path, "wb") as fh:
        fh.write(res.content)

    return destination_path
