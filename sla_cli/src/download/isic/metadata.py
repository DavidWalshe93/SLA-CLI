"""
Author:     David Walshe
Date:       10 April 2021
"""

import logging
import os
from typing import Tuple, Dict, List
from dataclasses import dataclass
from itertools import chain
from collections import OrderedDict
import json
from pprint import pprint
from functools import wraps

import pandas as pd
from requests import Session
from alive_progress import alive_bar

from sla_cli.src.download import Downloader
from sla_cli.src.download.utils import inject_http_session
from sla_cli.src.common.path import Path

logger = logging.getLogger(__name__)


def _download_isic_metadata(obj) -> None:
    """
    Downloads the ISIC Archive metadata if it doesnt already exist to the
    'db' path.

    :param obj: The Downloader object.
    """
    # Download metadata to DB folder before attempting image download.
    meta_downloader = IsicMetadataDownloader(obj.options)
    if not os.path.exists(Path.isic_metadata()):
        logger.info(f"Could not find ISIC metadata locally which is required to download ISIC datasets.")
        logger.info(f"Downloading ISIC metadata first, followed by images.")
        meta_downloader.download()
    else:
        logger.debug(f"Found local ISIC metadata file at: '{Path.isic_metadata()}'.")


def requires_isic_metadata(func):
    """
    Decorator to checks if the ISIC metadata is available locally.

    If it is not available, it downloads it to the db directory for local referencing before downloading
    ISIC image datasets.
    """

    @wraps(func)
    def requires_isic_metadata_wrapper(obj, *args, **kwargs):
        """
        :param obj: The IsicImageDownload object.
        """
        _download_isic_metadata(obj)

        return func(obj, *args, **kwargs)

    return requires_isic_metadata_wrapper


@dataclass
class UrlParams:
    """
    :param limit: The limit ot the number of records per request.
    :param offset: The record offset from the start of the records.
    """
    limit: int
    offset: int


class IsicMetadataDownloader(Downloader):

    @inject_http_session
    def download(self, session: Session, **kwargs) -> None:
        """
        Downloads all the ISIC Archive metadata from the ISIC archive API and saves it as a CSV file.

        :param session: The HTTP session to make all GET request for data with, auto-supplied via decorator.
        """
        limit = 5000
        offset = 0

        responses = []
        records = 0
        with alive_bar(0, title="Downloading ISIC metadata records", unknown="stars") as bar:
            while True:
                # Make the request URL.
                url = self._make_request_url(UrlParams(limit=limit, offset=offset))

                # Make the request and update the progress bar.
                data = self._process_request(session, url)
                responses.append(data)
                records += len(data)

                # Update the offset for the next request.
                offset += limit

                # Update progress bar for user.
                bar()
                bar.text(f"{records} records downloaded.")

                # Break once all data is retrieved.
                if limit != len(data):
                    break

        records = self._merge_records(responses=responses)
        records = self._add_year_tags(records=records)

        self._save_records(records=records)

    def _make_request_url(self, params: UrlParams) -> str:
        """
        Returns a URL to make a request from the ISIC archive off.

        :param params: The URL parameters to create the URL with.
        :return: A URL to make a request off.
        """
        return f"{self.url}/image?limit={params.limit}&offset={params.offset}&sort=name&sortdir=1&detail=true"

    @staticmethod
    def _process_request(session: Session, url: str) -> List[Dict[str, any]]:
        """
        Makes a GET request to the ISIC archive for metadata.

        :param session: The HTTP session.
        :param url: The URL to request data from.
        :return: The response data.
        """
        # Make request and capture response.
        res = session.get(url)

        # Convert response to JSON.
        return json.loads(str(res.content, encoding="utf8"))

    def _merge_records(self, responses: List[List[Dict[str, any]]]) -> pd.DataFrame:
        """
        Merges the record responses into a single pandas dataframe to save.

        :param responses: The responses holding the data of the ISIC archive metadata.
        :return: The merged responses as a pandas dataframe.
        """
        # Merge all responses into a single list from a list of lists.
        metadata = chain.from_iterable(responses)
        metadata = map(self._process_metadata, metadata)

        return pd.DataFrame(metadata)

    @staticmethod
    def _process_metadata(data: dict) -> OrderedDict:
        """
        Processes the raw metadata of the API response into a CSV friendly format.

        :return: A dictionary with all relative information on the image.
        """
        try:
            return OrderedDict(
                isic_id=data["_id"],
                image_name=data["name"],
                dataset=data["dataset"]["name"],
                description=data["dataset"]["description"],
                accepted=data["notes"]["reviewed"]["accepted"],
                created=data["created"].split("T")[0],
                tags=data["notes"]["tags"],
                pixels_x=data["meta"]["acquisition"]["pixelsX"],
                pixels_y=data["meta"]["acquisition"]["pixelsY"],
                age=data["meta"]["clinical"].get("age_approx", None),
                sex=data["meta"]["clinical"].get("sex", None),
                localization=data["meta"]["clinical"].get("anatom_site_general", None),
                benign_malignant=data["meta"]["clinical"].get("benign_malignant", None),
                dx=data["meta"]["clinical"].get("diagnosis", None),
                dx_type=data["meta"]["clinical"].get("diagnosis_confirm_type", None),
                melanocytic=data["meta"]["clinical"].get("melanocytic", None),
            )
        except Exception as e:
            pprint(data)
            raise e

    @staticmethod
    def _add_year_tags(records: pd.DataFrame) -> pd.DataFrame:
        """
        Expands records competition tags to their own columns.

        :param records: The dataframe of records to add columns to
        :return: The dataset with additional year tags.
        """
        # Add columns to tag if a dataset was used in any ISIC competitions.
        for i in range(2016, 2021):
            records[f"{i}"] = records["tags"].str.contains(f"{i}")

        return records

    def _save_records(self, records: pd.DataFrame) -> None:
        """
        Saves the downloaded ISIC records to CSV format.

        :param records: The records to expand.
        """
        # Save dataset to user defined location.
        output_path = os.path.join(self.destination_directory, "isic_metadata.csv")
        records.to_csv(output_path, index=False)

        if not os.path.exists(Path.isic_metadata()):
            # Save the isic_metadata to the DB folder on first download to
            # prevent re-downloading for every Dataset request.
            records.to_csv(Path.isic_metadata(), index=False)
