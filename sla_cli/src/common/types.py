"""
Author:     David Walshe
Date:       15 April 2021
"""

import logging
from typing import Union

import attr

logger = logging.getLogger(__name__)


@attr.s
class TrainTestSplit:
    train: Union[int, float] = attr.ib()
    validation: Union[int, float] = attr.ib()
    test: Union[int, float] = attr.ib()

    def __attrs_post_init__(self):
        """Validates the contents of the split values."""
        if any([isinstance(item, float) for item in [self.train, self.validation, self.test]]):
            self.validate_floating_point_ratios()
        else:
            self.validate_integer_values()

    def validate_floating_point_ratios(self):
        """Validates that floating point ratios must be equal to 1 when summed."""
        total = sum([self.train, self.validation, self.test])
        if total != 1:
            logger.error(f"When using floating point split values, the sum of values must equal to 1. Got {total}.")
            exit()

    def validate_integer_values(self):
        """Validates integer splits are positive number of 1 or greater."""
        if self.train < 1:
            logger.error(f"Number of training instances must be 1 or more. Got {self.train}.")
            exit()
        if self.test < 1:
            logger.error(f"Number of test instances must be 1 or more. Got {self.test}.")
            exit()
