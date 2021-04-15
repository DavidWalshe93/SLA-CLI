"""
Author:     David Walshe
Date:       10 April 2021
"""

import logging
import os
from functools import wraps
import math
from zipfile import ZipFile
import shutil
from typing import List

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
    with alive_bar(total=math.ceil(size), title=f"[SLA] - INFO - - - Downloading {size} MB", manual=True) as bar:
        # Download the file.
        res = requests.get(url, stream=True)

        # Throw an error for bad status codes
        res.raise_for_status()

        # Create save file and write out dataset content as data arrives.
        with open(destination_path, "wb") as fh:
            for KB, block in enumerate(res.iter_content(1024), start=1):
                fh.write(block)
                # Update progress for every MB downloaded.
                MB, remainder = divmod(KB, 1024)
                if remainder == 0:
                    bar(MB / size)

        # Show progress bar as completed.
        bar(1.0)

        return destination_path


def unzip_file(archive_path: str, extracted_path: str):
    """
    Unzips a ZIP file to a extract destination.

    :param archive_path: The archive path.
    :param extracted_path: The path to extract to.
    """
    with ZipFile(archive_path, "r") as fh:
        fh.extractall(extracted_path)


def move_images(image_paths: List[str], dst_path: str):
    """Moves images to a destination folder."""
    for image in image_paths:
        # Get the image name.
        image_name = image.split(os.sep)[-1]
        # Move the image to the destination folder.
        shutil.move(image, os.path.join(dst_path, image_name))
