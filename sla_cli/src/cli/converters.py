"""
Author:     David Walshe
Date:       14 April 2021
"""

import logging
import warnings
from typing import List, Tuple
from sla_cli.src.common.types import TrainTestSplit

# Suppress fuzzy wuzzy warning for c++ library install.
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from fuzzywuzzy import process

logger = logging.getLogger(__name__)


def train_test_split_cb(ctx, param, value: str) -> TrainTestSplit:
    """
    Converts a string into a TrainTestSplit object.

    :param value: The command line value to split into train/validation/test parameters.
    :return: A TrainTestSplit object.
    """
    train, val, test = [float(item) if float(item) < 1 else int(item) for item in value.split(":")]

    return TrainTestSplit(train=train, validation=val, test=test)


def _matcher(choices: List[str], fuzzy_options: List[str], warning_cb: callable) -> List[str]:
    """
    Helper function to generalise fuzzy matching for different converter callbacks.

    :param choices: The possible choices.
    :param fuzzy_options: The user passed options.
    :param warning_cb: A warning callback to raise a context specific message.
    :return: The matched options.
    """
    # Handles defaults=None or no arguments passed.
    if fuzzy_options is None:
        return None

    # Remove fully matching choices.
    options = [option for option in fuzzy_options if option.lower() in choices]
    # Retain only non-perfect matches for fuzzy matching.
    fuzzy_options = [option for option in fuzzy_options if option not in options]

    # Perform fuzzy match for all non-perfect matches.
    for option in fuzzy_options:
        best_match = process.extractOne(option, choices)
        if best_match[1] != 100:
            warning_cb(option, best_match)

        options.append(best_match[0])

    return options


def match_datasets_cb(ctx, param, fuzzy_options: List[str]) -> List[str]:
    """
    Attempts to correct user spelling mistakes of input datasets.

    :param fuzzy_options: The user inputted datasets.
    :return: The best matched datasets.
    """
    choices = ["atlas_of_dermoscopy",
               "bcn_20000",
               "bcn_2020_challenge",
               "brisbane_isic_challenge_2020",
               "dermofit",
               "dermoscopedia_cc_by",
               "dermis",
               "dermquest",
               "ham10000",
               "isic_2020_challenge_mskcc_contribution",
               "isic_2020_vienna_part_1",
               "isic_2020_vienna_part_2",
               "jid_editorial_images_2018",
               "mclass_d",
               "mclass_nd",
               "mednode",
               "msk_1",
               "msk_2",
               "msk_3",
               "msk_4",
               "msk_5",
               "pad_ufes_20",
               "ph2",
               "sonic",
               "sydney_mia_smdc_2020_isic_challenge_contribution",
               "uda_1",
               "uda_2"]

    def warning_cb(option: str, best_match: Tuple):
        logger.warning(f"Spelling mistake found for dataset '{option}', coercing to best possible match '{best_match[0]}' ({best_match[1]}% sure).")

    return _matcher(choices, fuzzy_options, warning_cb)


def match_dx_cb(ctx, param, fuzzy_options: List[str]) -> List[str]:
    """
    Attempts to correct user spelling mistakes of input diagnosis (dx).

    :param fuzzy_options: The user inputted diagnosis (dx).
    :return: The best matched datasets.
    """
    choices = [
        "nevus",
        "melanoma",
        "actinic keratosis",
        "angiofibroma or fibrous papule",
        "angioma",
        "atypical melanocytic proliferation",
        "basal cell carcinoma",
        "cafe-au-lait macule",
        "dermatofibroma",
        "lentigo NOS",
        "lentigo simplex",
        "lichenoid keratosis",
        "pigmented benign keratosis",
        "scar",
        "seborrheic keratosis",
        "solar lentigo",
        "squamous cell carcinoma",
        "vascular lesion"
    ]

    def warning_cb(option: str, best_match: Tuple):
        logger.warning(f"Spelling mistake found for diagnosis '{option}', coercing to best possible match '{best_match[0]}' ({best_match[1]}% sure).")

    return _matcher(choices, fuzzy_options, warning_cb)
