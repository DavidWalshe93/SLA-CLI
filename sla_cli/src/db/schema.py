"""
Author:     David Walshe
Date:       07 April 2021
"""

import logging
from typing import Dict, List, Union
import json

import attr
from attr.validators import instance_of
from colorama import Fore

from sla_cli.src.common.path import Path

logger = logging.getLogger(__name__)


@attr.s
class Schema:
    pass


@attr.s
class Info(Schema):
    """
    Maps the meta information of a dataset object.
    """
    availability: str = attr.ib(validator=instance_of(str))
    capture_method: str = attr.ib(validator=instance_of(str))
    size: float = attr.ib(validator=instance_of(float), converter=lambda size: round(float(size), 2))
    references: Union[List[str]] = attr.ib(validator=instance_of(list))
    download: Union[List[str], None] = attr.ib(default=[""], converter=lambda config: [] if config is None else config)

    def __getitem__(self, item):
        """Allows for [] indexing."""
        return self.__getattribute__(item)

    def __str__(self):
        indent = "\n       - "
        return f"   Availability:   {Fore.LIGHTGREEN_EX if self.availability.lower() == 'public' else Fore.LIGHTRED_EX}{self.availability}{Fore.RESET}\n" \
               f"   Capture method: {Fore.LIGHTCYAN_EX if self.capture_method.lower() == 'dermoscopy' else Fore.LIGHTYELLOW_EX}{self.capture_method}{Fore.RESET}\n" \
               f"   Size:           {'--' if self.size < 0 else round(self.size, 2)} MB\n" \
               f"   References:\n" \
               f"       - {indent.join(self.references)}\n" \
               f"   Data source URL:\n" \
               f"       - {indent.join(self.download)}"


@attr.s
class Dataset(Schema):
    """
    Maps to an individual dataset.
    """
    info: Info = attr.ib(validator=instance_of(Info), converter=lambda config: Info(**config))
    labels: Dict[str, int] = attr.ib(validator=instance_of(dict))


@attr.s
class Datasets(Schema):
    """
    Maps to the available dataset statistics in the db file.
    """
    atlas_of_dermoscopy: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    bcn_20000: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    bcn_2020_challenge: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    brisbane_isic_challenge_2020: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    dermofit: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    dermoscopedia_cc_by: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    dermis: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    dermquest: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    ham10000: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    isic_2020_challenge_mskcc_contribution: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    isic_2020_vienna_part_1: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    isic_2020_vienna_part_2: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    jid_editorial_images_2018: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    mclass_d: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    mclass_nd: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    mednode: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    msk_1: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    msk_2: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    msk_3: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    msk_4: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    msk_5: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    pad_ufes_20: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    ph2: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    sonic: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    sydney_mia_smdc_2020_isic_challenge_contribution: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    uda_1: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))
    uda_2: Dataset = attr.ib(validator=instance_of(Dataset), converter=lambda config: Dataset(**config))

    @property
    def as_dict(self):
        """Returns all scalar and collect objects for this class that are Dataset objects."""
        return {key: value for key, value in self.__dict__.items() if isinstance(value, Dataset)}

    @property
    def labels(self):
        """Retrieves all the label entries for dataset objects."""
        return {key: value.labels for key, value in self.as_dict.items()}

    @property
    def info(self):
        """Retrieves all the info entries for the dataset objects."""
        return {key: value.info for key, value in self.as_dict.items()}

    @property
    def names(self):
        """Returns a list of all dataset names."""
        return list(self.as_dict.keys())

    def __getitem__(self, item) -> Dataset:
        """Allows [] indexing of attributes."""
        return self.__getattribute__(item)


@attr.s
class DB(Schema):
    """
    Maps to the db.json file.
    """
    datasets: Datasets = attr.ib(validator=instance_of(Datasets), converter=lambda config: Datasets(**config))
    abbrev: Dict[str, str] = attr.ib(validator=instance_of(dict))

    @staticmethod
    def get_db():
        """
        Factory method to return an instance of the DB object.

        :return: A instance of DB.
        """
        with open(Path.db()) as fh:
            db = json.load(fh)
            return DB(**db)
