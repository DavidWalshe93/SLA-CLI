"""
Author:     David Walshe
Date:       07 April 2021
"""

import logging
from typing import Dict, List
import json

import attr
from attr.validators import instance_of
from tabulate import tabulate

from src.common.path import Path

logger = logging.getLogger(__name__)


@attr.s
class Urls:
    """
    Maps to the available dataset urls in the db file.
    """
    isic: str = attr.ib(instance_of(str))
    dermaquest_dermis: List[str] = attr.ib(instance_of(str))
    ph2: str = attr.ib(instance_of(str))
    mednode: str = attr.ib(instance_of(str))
    pad_ufes_20: str = attr.ib(instance_of(str))


@attr.s
class Datasets:
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

    def names(self, tablefmt: str = "simple"):
        """Returns only the dataset names as a formatted table."""
        names = [[name] for name in list(self.__dict__.keys())]

        return tabulate(names, headers=["Dataset Name"], tablefmt=tablefmt)

    def names_and_overall_images(self, tablefmt: str = "simple"):
        """Returns the names and overall total instance counts of each dataset."""
        data = [[name, sum(images.values())] for name, images in self.__dict__.items()]

        return tabulate(data, headers=["Dataset Name", "No. Images"], tablefmt=tablefmt)


@attr.s
class DB:
    """
    Maps to the db.json file.
    """
    urls: Urls = attr.ib(validator=instance_of(Urls), converter=lambda config: Urls(**config))
    datasets: Datasets = attr.ib(validator=instance_of(Datasets), converter=lambda config: Datasets(**config))

    @staticmethod
    def get_db():
        """
        Factory method to return an instance of the DB object.

        :return: A instance of DB.
        """
        with open(Path.db()) as fh:
            db = json.load(fh)
            return DB(**db)
