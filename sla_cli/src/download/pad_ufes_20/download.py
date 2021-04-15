"""
Author:     David Walshe
Date:       11 April 2021
"""

import logging
import os
import shutil
from zipfile import ZipFile
import glob

import pandas as pd
from requests import Session

from sla_cli.src.download import FileDownloader, download_file, unzip_file

logger = logging.getLogger(__name__)


class PadUfes20Downloader(FileDownloader):
    __title__ = "PAD-UFES-20"
    __archive_name__ = "pad_ufes_20.zip"
    __extracted_name__ = "PAD_UFES_20"

    def _download(self):
        """Downloads the PAD_UFES_20 zip archive."""
        download_file(self.url, self.archive_path, self.size)

    def _extract(self):
        """Extracts the PAD_UFES_20 zip archive."""
        unzip_file(self.archive_path, self.extracted_path)

        # Unzip inner image archives.
        images_dir = os.path.join(self.extracted_path, "images")
        inner_zip_files = [os.path.join(images_dir, archive) for archive in os.listdir(images_dir)]
        for archive in inner_zip_files:
            # Unzip archive
            with ZipFile(archive, "r") as fh:
                fh.extractall(images_dir)

            # Remove archive after extraction.
            os.remove(archive)

    def _format_metadata(self):
        pass

    def _save_metadata(self):
        """Parse the metadata of the PAD-UFES-20 dataset."""
        self.metadata_path = os.path.join(self.extracted_path, "metadata.csv")
        if self.options.metadata_as_name:
            new_path = os.path.join(self.extracted_path, "pad_ufes_20.csv")
            shutil.move(self.metadata_path, new_path)
            self.metadata_path = new_path

    def _collect_images(self):
        """Collects all the absolute image paths from the PAD-UFES-20 extracted archive."""
        # Get the absolute path for all images in the PAD-UFES-20 dataset.
        image_paths = glob.glob(f"{self.images_path}/**/*.png", recursive=True)

        return image_paths

    def _convert_images(self):
        pass

    def _move_images(self):
        """Moves all images to the 'images' directory."""
        for image in self._collect_images():
            # Get the image name.
            image_name = image.split(os.sep)[-1]
            # Move the image to the destination folder.
            shutil.move(image, os.path.join(self.images_path, image_name))

    def _clean_up(self):
        """Clean up any stray files."""
        for i in range(1, 4):
            os.remove(os.path.join(self.images_path, f"imgs_part_{i}"))
