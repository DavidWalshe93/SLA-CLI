"""
Author:     David Walshe
Date:       07 April 2021
"""

import logging
from typing import Dict, List, Union
import json

import attr
from attr.validators import instance_of
from tabulate import tabulate

import pandas as pd

from colorama import Fore

from src.common.path import Path
from src.schema.utils import init_colorama

logger = logging.getLogger(__name__)


@attr.s
class Schema:
    pass


@attr.s
class Urls(Schema):
    """
    Maps to the available dataset urls in the db file.
    """
    isic: str = attr.ib(instance_of(str))
    dermaquest_dermis: List[str] = attr.ib(instance_of(str))
    ph2: str = attr.ib(instance_of(str))
    mednode: str = attr.ib(instance_of(str))
    pad_ufes_20: str = attr.ib(instance_of(str))


@attr.s
class Datasets(Schema):
    """
    Maps to the available dataset statistics in the db file.
    """
    atlas_of_dermoscopy: Dict[str, int] = attr.ib(instance_of(dict))
    bcn_20000: Dict[str, int] = attr.ib(instance_of(dict))
    bcn_2020_challenge: Dict[str, int] = attr.ib(instance_of(dict))
    brisbane_isic_challenge_2020: Dict[str, int] = attr.ib(instance_of(dict))
    dermofit: Dict[str, int] = attr.ib(instance_of(dict))
    dermoscopedia_cc_by: Dict[str, int] = attr.ib(instance_of(dict))
    dermis: Dict[str, int] = attr.ib(instance_of(dict))
    dermquest: Dict[str, int] = attr.ib(instance_of(dict))
    ham10000: Dict[str, int] = attr.ib(instance_of(dict))
    isic_2020_challenge_mskcc_contribution: Dict[str, int] = attr.ib(instance_of(dict))
    isic_2020_vienna_part_1: Dict[str, int] = attr.ib(instance_of(dict))
    isic_2020_vienna_part_2: Dict[str, int] = attr.ib(instance_of(dict))
    jid_editorial_images_2018: Dict[str, int] = attr.ib(instance_of(dict))
    mclass_d: Dict[str, int] = attr.ib(instance_of(dict))
    mclass_nd: Dict[str, int] = attr.ib(instance_of(dict))
    mednode: Dict[str, int] = attr.ib(instance_of(dict))
    msk_1: Dict[str, int] = attr.ib(instance_of(dict))
    msk_2: Dict[str, int] = attr.ib(instance_of(dict))
    msk_3: Dict[str, int] = attr.ib(instance_of(dict))
    msk_4: Dict[str, int] = attr.ib(instance_of(dict))
    msk_5: Dict[str, int] = attr.ib(instance_of(dict))
    pad_ufes_20: Dict[str, int] = attr.ib(instance_of(dict))
    ph2: Dict[str, int] = attr.ib(instance_of(dict))
    sonic: Dict[str, int] = attr.ib(instance_of(dict))
    sydney_mia_smdc_2020_isic_challenge_contribution: Dict[str, int] = attr.ib(instance_of(dict))
    uda_1: Dict[str, int] = attr.ib(instance_of(dict))
    uda_2: Dict[str, int] = attr.ib(instance_of(dict))
    # Populated after initialisation.
    db = attr.ib(default=None)

    def names(self, tablefmt: str = "simple", output_file: str = None) -> Union[str, None]:
        """
        Returns only the names of the datasets available.

        :param tablefmt: The console output format.
        :param output_file: If specified, the output is redirected to a file instead of to the console.
        :return: If not output_file is specified contents are printed to the screen, else the content
                 saved to the specified file.
        """
        names = [[name] for name in list(self.as_dict().keys())]

        if output_file:
            df = pd.DataFrame(names, columns=["Dataset Name"])
            df.to_csv(output_file, index=None)
            return f"Saved to '{output_file}'"
        else:
            return tabulate(names, headers=["Dataset Name"], tablefmt=tablefmt)

    def names_and_overall_images(self, tablefmt: str = "simple", output_file: str = None):
        """
        Returns the names of the datasets available and the total number of images within the dataset.

        :param tablefmt: The console output format.
        :param output_file: If specified, the output is redirected to a file instead of to the console.
        :return: If not output_file is specified contents are printed to the screen, else the content
                 saved to the specified file.
        """
        data = [[name, sum(images.values())] for name, images in self.as_dict().items()]

        if output_file:
            df = pd.DataFrame(data, columns=["Dataset Name", "No. Images"])
            df.to_csv(output_file, index=None)
            return f"Saved to '{output_file}'"
        else:
            return tabulate(data, headers=["Dataset Name", "No. Images"], tablefmt=tablefmt)

    @init_colorama
    def names_and_distribution(self, tablefmt: str = "simple", output_file: str = None) -> str:
        """Returns the names and totals of each class in each dataset."""
        data = []
        # Begin to capture each row.
        for dataset, values in self.as_dict().items():
            row = [dataset]
            headers = ["Dataset"]
            # For each row capture each dx count.
            for dx, abbrev in self.db.abbrev.items():
                item = values.get(dx, 0)
                # If showing to the console, add some color.
                if output_file is None:
                    color = Fore.RED if item == 0 else Fore.GREEN
                    item = f"{color}{item}{Fore.RESET}"
                # Add the item to the row collector.
                row.append(item)
                headers.append(abbrev)
            # Add the row to the data collector.
            data.append(row)

        if output_file:
            df = pd.DataFrame(data, columns=headers)
            df.to_csv(output_file, index=None)
            return f"Saved to '{output_file}'"
        else:
            return tabulate(data, headers=headers, tablefmt=tablefmt)

    def abbreviations(self, tablefmt: str = "simple") -> str:
        """Returns the abbreviation table."""
        return tabulate([(abbrev, dataset) for dataset, abbrev in self.db.abbrev.items()], headers=["Abbrev.", "Diagnosis"], tablefmt=tablefmt)

    def as_dict(self):
        """Returns all scalar and collect objects for this class, objects are removed."""
        return {key: value for key, value in self.__dict__.items() if not isinstance(value, Schema)}


@attr.s
class DB(Schema):
    """
    Maps to the db.json file.
    """
    urls: Urls = attr.ib(validator=instance_of(Urls), converter=lambda config: Urls(**config))
    datasets: Datasets = attr.ib(validator=instance_of(Datasets), converter=lambda config: Datasets(**config))
    abbrev: Dict[str, str] = attr.ib(validator=instance_of(dict))

    def __attrs_post_init__(self):
        """Adds DB reference to children."""
        self.datasets.db = self

    @staticmethod
    def get_db():
        """
        Factory method to return an instance of the DB object.

        :return: A instance of DB.
        """
        with open(Path.db()) as fh:
            db = json.load(fh)
            return DB(**db)
