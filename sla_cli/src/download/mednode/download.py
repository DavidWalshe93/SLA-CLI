"""
Author:     David Walshe
Date:       11 April 2021
"""

import logging
import glob
import os
import shutil
from typing import List

import pandas as pd

from sla_cli.src.download import FileDownloader, download_file, unzip_file, move_images

logger = logging.getLogger(__name__)


class MednodeDownloader(FileDownloader):
    __title__ = "MEDNODE"
    __archive_name__ = "mednode.zip"
    __extracted_name__ = "mednode"

    def _download(self):
        """Downloads the mednode dataset as a ZIP archive."""
        download_file(self.url, self.archive_path, self.size)

    def _extract(self):
        """Extracts the PAD_UFES_20 zip archive."""
        unzip_file(self.archive_path, self.extracted_path)

    @property
    def data_path(self) -> str:
        """Returns the path where the dataset images are found."""
        return os.path.join(self.extracted_path, "complete_mednode_dataset")

    def _get_images_paths_for(self, dx: str) -> List[str]:
        """
        Returns the absolute paths for all images in a given diagnosis(dx) folder.

        :param dx: The diagnosis [melanoma/naevus].
        :return: The absolute paths to the given diagnosis images.
        """
        return glob.glob(f"{self.data_path}/{dx.lower()}/*")

    @staticmethod
    def _get_images_names_for(image_paths: List[str]) -> List[str]:
        """
        Gets the names, without extension for the given absolute file paths.

        :param image_paths: The absolute file paths.
        :return: The names of the images without extension
        """

        def get_image_name(path: str) -> str:
            """Returns the image name, without extension from a given path."""
            return path.split(os.sep)[-1].split(".")[0]

        return [get_image_name(path) for path in image_paths]

    @staticmethod
    def _get_dataframe_for(images_names: List[str], dx: str) -> pd.DataFrame:
        """Creates a DataFrame of the given image_name and diagnosis."""
        # Convert name to for naevus -> nevus.
        dx = "nevus" if dx == "naevus" else dx
        return pd.DataFrame(
            {
                "image_name": images_names,
                "dx": [dx for _ in images_names]
            })

    def _format_metadata(self):
        pass

    def _save_metadata(self):
        """Creates metadata from MedNode file structure."""
        # Create a dataframe of [image_name, dx] for each dx.
        dfs = []
        for dx in ["melanoma", "naevus"]:
            images_paths = self._get_images_paths_for(dx)
            images_names = self._get_images_names_for(images_paths)
            df = self._get_dataframe_for(images_names, dx)

            dfs.append(df)

        # Append all dx dataframes
        df = pd.concat(dfs)

        # Save dataframes.
        df.to_csv(self.metadata_path(), index=None)
        # if self.options.metadata_as_name:
        #     df.to_csv(os.path.join(self.extracted_path, f"{self.dataset_name}.csv"), index=None)
        # else:
        #     df.to_csv(os.path.join(self.extracted_path, f"metadata.csv"), index=None)

    def _label_metadata(self):
        """Relabels the data into a common naming convention."""

    def _collect_images(self):
        """Collect all absolute image paths"""
        collector = []
        for dx in ["melanoma", "naevus"]:
            [collector.append(path) for path in self._get_images_paths_for(dx)]

        return collector

    def _convert_images(self):
        pass

    def _move_images(self):
        """Move images to destination path."""
        # Create images destination folder.
        os.makedirs(self.images_path)
        # Move images.
        move_images(self._collect_images(), self.images_path)

    def _clean_up(self):
        """Removed empty files and folders."""
        shutil.rmtree(self.data_path)
