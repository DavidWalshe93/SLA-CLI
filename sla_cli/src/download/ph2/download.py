"""
Author:     David Walshe
Date:       11 April 2021
"""

import logging
import os
import shutil
import glob
from typing import List

import pandas as pd
import patoolib
from requests import Session
from alive_progress import alive_bar

from sla_cli.src.download import FileDownloader, DownloaderOptions, download_file, inject_http_session

logger = logging.getLogger(__name__)


class Ph2Downloader(FileDownloader):
    __archive_name__ = "ph2.rar"
    __extracted_name__ = "PH2"

    def download(self, session: Session = None):
        """Downloads and formats the PH2 dataset."""
        # Check to see if the dataset already exists.
        if self._does_not_exist_or_forced():
            with alive_bar(None, "[SLA] - INFO - - - Acquiring PH2 Dataset", unknown="stars") as bar:
                self.update_progress(bar, "Downloading dataset.")
                self._download()

                self.update_progress(bar, "Extracting archive.")
                self._extract()

                self.update_progress(bar, "Parsing metadata.")
                self._parse_metadata()

                self.update_progress(bar, "Collecting images.")
                self._collect_images()

                self.update_progress(bar, "Moving images.")
                self._move_images()

                self.update_progress(bar, "Cleaning up.")
                self._clean_up()

    def _download(self):
        """
        Downloads the PH2 dataset as a RAR archive.

        :param session: The HTTP session for the download.
        """
        download_file(self.url, self.archive_path)

    def _extract(self):
        """
        Extracts the downloaded archive.
        """
        try:
            patoolib.extract_archive(self.archive_path, outdir=self.extracted_path, verbosity=-1)
        except Exception as err:
            logger.error(f"You may have to install a 3rd-party application to unpack '.rar' files.")
            logger.error(f"The development team used '7-zip' on Windows 10 OS, which worked as expected.")
            logger.error(f"Look at the patoolib documentation for help on this for your platform.")
            logger.error(f"")
            logger.error(f"Patoolib Documentation: http://wummel.github.io/patool/")
            raise err

        # Clean-up
        os.remove(self.archive_path)

    def _parse_metadata(self):
        """
        Moves the metadata as is to the extracted directory.
        """
        metadata_file = os.path.join(self.extracted_path, "PH2Dataset", "PH2_dataset.xlsx")

        if self.options.metadata_as_name:
            self.metadata_path = os.path.join(self.extracted_path, f"{self.dataset_name}.xlsx")
        else:
            self.metadata_path = os.path.join(self.extracted_path, f"ph2.xlsx")

        shutil.move(metadata_file, self.metadata_path)

    @property
    def _image_ids(self):
        """Returns the image names of the PH2 dataset."""
        return list(pd.read_csv(self.metadata_path, header=12)["Image Name"])

    def _collect_images(self) -> List[str]:
        """
        Collects all the absolute image paths from the PH2 extracted archive.
        """
        # Get the root path for images.
        root_path = os.path.join(self.extracted_path, "PH2Dataset", "PH2 Dataset images")

        # Get the absolute path for all images in the PH2 dataset.
        image_paths = glob.glob(f"{root_path}/**/*_Dermoscopic_Image/*.bmp", recursive=True)

        return image_paths

    def _convert_images(self):
        pass

    def _move_images(self):
        """Moves the images from the extracted archive layout to the 'images' folder."""
        # Create the destination.
        os.makedirs(self._images_path)

        for image in self._collect_images():
            # Get the image name.
            image_name = image.split(os.sep)[-1]
            # Move the image to the destination folder.
            shutil.move(image, os.path.join(self._images_path, image_name))

    def _clean_up(self):
        """Clean up any stray files."""
        shutil.rmtree(os.path.join(self.extracted_path, "PH2Dataset"))
