"""
Author:     David Walshe
Date:       14 April 2021
"""

import logging
import warnings
from typing import List

# Suppress fuzzy wuzzy warning for c++ library install.
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from fuzzywuzzy import process

logger = logging.getLogger(__name__)


def match_datasets_cb(ctx, param, fuzzy_datasets: List[str]) -> List[str]:
    """
    Attempts to correct user spelling mistakes of input datasets.

    :param ctx: The Click context.
    :param param: The command parameter information.
    :param fuzzy_datasets: The user inputted datasets.
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

    # Handles defaults=None or no arguments passed.
    if fuzzy_datasets is None:
        return None

    # Remove fully matching choices.
    datasets = [dataset for dataset in fuzzy_datasets if dataset.lower() in choices]
    # Retain only non-perfect matches for fuzzy matching.
    fuzzy_datasets = [dataset for dataset in fuzzy_datasets if dataset not in datasets]

    # Perform fuzzy match for all non-perfect matches.
    for dataset in fuzzy_datasets:
        best_match = process.extractOne(dataset, choices)
        if best_match[1] != 100:
            logger.warning(f"Spelling mistake found for dataset '{dataset}', coercing to best possible match '{best_match[0]}' ({best_match[1]}% sure).")

        datasets.append(best_match[0])

    return datasets
