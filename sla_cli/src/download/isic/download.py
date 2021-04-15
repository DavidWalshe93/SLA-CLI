"""
Author:     David Walshe
Date:       10 April 2021
"""

import logging
import os
from typing import List, Union
import shutil
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from threading import Lock
import urllib.parse
import json
import glob
from zipfile import ZipFile

import pandas as pd
from requests import Session
from alive_progress import alive_bar

from sla_cli.src.common.path import Path
from sla_cli.src.common.config import inject_config, Config
from sla_cli.src.download import inject_http_session, Downloader
from sla_cli.src.download.isic.metadata import IsicMetadataDownloader, requires_isic_metadata

logger = logging.getLogger(__name__)


def make_batches(data: List[any], n: int):
    """
    Yield successive n-sized chunks from data.

    :param data: The data to batch.
    :param n: The number of items per batch.
    :return: A batch of size n taken from data.
    """
    for i in range(0, len(data), n):
        yield data[i:i + n]


@dataclass
class DownloadOptions:
    image_ids: List[str]
    title: str


@dataclass
class ResponseOptions:
    index: int
    download_path: str
    unzip: bool


class IsicImageDownloader(Downloader):
    MAX_BATCH_SIZE = 300

    def __init__(self, *args, **kwargs):
        """
        Downloader class for the ISIC Archive API.
        """
        super().__init__(*args, **kwargs)
        self.metadata: pd.DataFrame = self._get_metadata()
        self.download_path = self._create_download_path(force=self.force)
        self.batch_size = self.options.config.isic.batch_size
        self.max_workers = self.options.config.isic.max_workers

    @requires_isic_metadata
    def _get_metadata(self) -> pd.DataFrame:
        """
        Returns a dataset with the metadata for only the given dataset name.

        :return: A filtered dataframe on the dataset name.
        """
        df = pd.read_csv(Path.isic_metadata())

        df = df[df["dataset"].str.upper() == convert(self.dataset_name)]

        return df

    def _create_download_path(self, force: bool = False) -> Union[str, None]:
        """
        Returns the download path, create it if it does not already exist.

        :param force: Flag to force deletion.
        """
        path = os.path.join(self.destination_directory, self.dataset_name)
        if os.path.exists(path) and force:
            logger.debug(f"'-f/--force' flag set, deleting directory: '{path}'")
            shutil.rmtree(path)
            logger.debug(f"Deletion successful.")
        elif os.path.exists(path) and not force:
            logger.warning(f"{self.dataset_name} already exists at the destination directory '{path}'")
            logger.warning(f"If you wish to re-download the dataset, try 'sla-cli download -f/--force <DATASET>'")
            logger.warning(f"Skipping...")
            return None

            # Make the download path.
        os.mkdir(path)
        logger.info(f"Created the download directory at: '{path}'")

        return path

    @property
    def image_ids(self) -> List[str]:
        """Returns the images ids for the given dataset."""
        return list(self.metadata["isic_id"])

    def download(self, **kwargs):
        """
        Downloads the requested images from the ISIC archive.
        """
        if self.download_path is None:
            return None

        self._download()
        self._verify_download()
        self._move_images()
        self._save_metadata()

    @property
    def _default_download_options(self):
        """Creates and returns the default download options."""
        return DownloadOptions(
            image_ids=self.image_ids,
            title=f"[SLA] - INFO - - - Downloading {self.dataset_name}."
        )

    @inject_http_session
    def _download(self, session: Session, **kwargs):
        """
        Downloads the requested images from the ISIC archive.

        :param session: The HTTP session to the ISIC Archive API.
        """
        options = kwargs.get("options", self._default_download_options)

        batches = list(make_batches(options.image_ids, n=self.batch_size))

        with alive_bar(len(batches), title=options.title, enrich_print=False) as bar:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Create a worker with a batch of image ids to request and download.
                futures_to_request = {executor.submit(self._make_request, session, batch): idx for idx, batch in enumerate(batches)}

                # As the requests complete, process the responses
                for index, future in enumerate(as_completed(futures_to_request)):
                    try:
                        options = ResponseOptions(index, self.download_path, self.unzip)
                        # Process the downloaded batch.
                        self._process_response(future, options)
                        bar()
                    except Exception as e:
                        logger.warning(f"{e.__str__()}")

    def _make_request(self, session: Session, batch: List[str]):
        """
        Request 300 images from the ISIC API.

        :param session: The HTTP session object.
        :param batch: The batch of images to download.
        :return: The HTTP response.
        """
        url = self._make_url(image_ids=batch)

        return session.get(url)

    def _make_url(self, image_ids: List[str]) -> str:
        """
        Creates a request for a series of 300 images.

        :param image_ids: The images to download, as a json list.
        :return: The request URL.
        """
        image_ids = self._preprocess_image_ids(image_ids)
        return f"{self.url}/image/download?include=images&imageIds={image_ids}"

    @staticmethod
    def _preprocess_image_ids(image_ids: list) -> List[str]:
        """
        Converts a python list of image IDs to a json array
        suitable for use with the ISIC API.

        :param image_ids: The image ids to convert.
        :return: The formatted image ids.
        """
        image_ids = json.dumps(str(image_ids))

        # Replace and switch quote notation for the API
        image_ids = image_ids.replace('"', "")
        image_ids = image_ids.replace("'", '"')

        # Quote all url strings.
        image_ids = urllib.parse.quote(image_ids)

        return image_ids

    @staticmethod
    def _process_response(future: Future, options: ResponseOptions):
        """
        Saves the downloaded ISIC images to as ZIP archives and then unpacks them.

        :param future: The future to ask for the result off.
        :param options: The options to handle the response with.
        """
        res = future.result()

        if not res:
            logger.error(f"Download content is empty.")
            raise ValueError("Issue downloading images.")
        else:
            # Save the downloaded data to a zip file.
            archive_file = os.path.join(options.download_path, f"download_{options.index}.zip")
            with open(archive_file, "wb") as stream:
                for chunk in res:
                    stream.write(chunk)

            if options.unzip:
                # Unzip the archive to the save path.
                # Use threading lock to stop deadlocking on filesystem resources.
                with Lock():
                    logger.debug(f"Unzipping {archive_file} to {options.download_path}")
                    IsicImageDownloader._unzip_archive(archive_file, options.download_path)

                    logger.debug(f"Removing {archive_file}.")
                    os.remove(archive_file)

    @staticmethod
    def _unzip_archive(archive: str, download_path: str) -> None:
        """
        Unzip archive and place contents into output directory.

        :param archive: The archive to read data from.
        :param download_path: The path to unpack the archives to.
        """
        with ZipFile(archive, 'r') as zip_ref:
            zip_ref.extractall(download_path)

    @property
    def isic_image_path(self) -> str:
        """Returns the isic image path."""
        return os.path.join(self.download_path, "ISIC-images", convert(self.dataset_name))

    @property
    def isic_images(self) -> List[str]:
        """Returns all the downloaded images, with non-image files removed."""
        return [image.split(".")[0] for image in os.listdir(self.isic_image_path) if not image.endswith(".txt")]

    def _verify_download(self):
        """Verifies all images were correctly downloaded."""
        # Get the metadata and images file names and compare them
        # to see if any images were missed.
        image_names = self.isic_images
        meta_names = list(self.metadata["image_name"])

        missing_images = sorted(list(set(meta_names) ^ set(image_names)))

        if len(missing_images) > 0:
            self._download_missing_images(missing_images)
            self._verify_download()
        else:
            logger.info(f"All '{self.dataset_name}' images were downloaded successfully'")

        return True

    def _download_missing_images(self, missing_images: List[str]):
        """
        Re-download missing images from the initial download.

        :param missing_images: A list of missing image names.
        """
        df = self.metadata
        missing_ids = sorted(list(df[df["image_name"].isin(missing_images)]["isic_id"]))
        options = DownloadOptions(
            image_ids=missing_ids,
            title=f"[SLA] - INFO - - - Re-Downloading {len(missing_ids)} from {self.dataset_name}."
        )
        self._download(options=options)

    @property
    def image_dst_directory(self) -> str:
        return os.path.join(self.download_path, "images")

    def _move_images(self):
        """Gather all images and move them to the root of the download folder."""
        # Move all images to 'images' folder.
        shutil.move(self.isic_image_path, self.image_dst_directory)
        # Delete old parent folder.
        os.rmdir(os.path.join(self.download_path, "ISIC-images"))
        # Remove all .txt files.
        [os.remove(os.path.join(self.image_dst_directory, file)) for file in os.listdir(self.image_dst_directory) if file.endswith(".txt")]

    def _save_metadata(self):
        """Saves the datasets metadata to a file."""
        # Save the metadata name as the dataset name. Handy for opening in excel for review.

        if self.options.metadata_as_name:
            save_name = self.dataset_name.lower().replace(" ", "_").replace("-", "_") + ".csv"
            self.metadata.to_csv(os.path.join(self.download_path, save_name))

        # Save as "metadata.csv", easier to work with for ML input pipelines.
        else:
            self.metadata.to_csv(os.path.join(self.download_path, "metadata.csv"))


def convert(dataset: str) -> str:
    """Translates the CLI argument name into the Metadata value for the ISIC archive."""
    return {
        "bcn_20000": "BCN_20000",
        "bcn_2020_challenge": "BCN_2020_Challenge",
        "brisbane_isic_challenge_2020": "Brisbane ISIC Challenge 2020",
        "dermoscopedia_cc_by": "Dermoscopedia (CC-BY)",
        "ham10000": "HAM10000",
        "isic_2020_challenge_mskcc_contribution": "ISIC 2020 Challenge - MSKCC contribution",
        "isic_2020_vienna_part_1": "ISIC_2020_Vienna_part_1",
        "isic_2020_vienna_part_2": "ISIC_2020_Vienna_part2",
        "jid_editorial_images_2018": "2018 JID Editorial Images",
        "msk_1": "MSK-1",
        "msk_2": "MSK-2",
        "msk_3": "MSK-3",
        "msk_4": "MSK-4",
        "msk_5": "MSK-5",
        "sonic": "SONIC",
        "sydney_mia_smdc_2020_isic_challenge_contribution": "Sydney (MIA / SMDC) 2020 ISIC challenge contribution",
        "uda_1": "UDA-1",
        "uda_2": "UDA-2"
    }.get(dataset, dataset).upper()


def name_converter(name: str) -> str:
    """
    Returns the correct dataset name for datasets begining with numbers.

    :param name: The name of the dataset to convert
    :return: The converted dataset name if required, else passed in name is returned.
    """
    return {
        "jid_editorial_images_2018": "2018 JID Editorial Images"
    }.get(name, name)
