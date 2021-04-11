"""
Author:     David Walshe
Date:       10 April 2021
"""

import logging
from functools import wraps
import math

from alive_progress import alive_bar
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


def download_file(url, destination_path: str, size: float):
    """
    Downloads a given dataset archive found at a URL endpoint.

    :param url: The URL to download the resource from.
    :param destination_path: The destination path for the download archive.
    :param size: The size of the download.
    """
    with alive_bar(total=math.ceil(size), title=f"[SLA] - INFO - - - Downloading {size} MB") as bar:
        # Download the file.
        res = requests.get(url, stream=True)

        # Throw an error for bad status codes
        res.raise_for_status()

        # Create save file and write out dataset content as data arrives.
        with open(destination_path, "wb") as fh:
            for kb, block in enumerate(res.iter_content(1024), start=1):
                fh.write(block)
                if (kb / 10) % 1024 == 0:
                    bar()

        return destination_path
