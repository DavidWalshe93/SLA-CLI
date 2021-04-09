"""
Author:     David Walshe
Date:       09 April 2021
"""

import pytest

from src.db.accessors import Datasets


@pytest.fixture
def datasets_obj() -> Datasets:
    """Returns a Datasets object."""
    return Datasets()


def test_dermoscopy_datasets(datasets_obj):
    """
    :GIVEN: A Datasets objects.
    :WHEN:  Getting the dermoscopy datasets.
    :THEN:  Verify only the dermoscopy datasets are returned.
    """
    expected = [
        "atlas_of_dermoscopy",
        "bcn_20000",
        "bcn_2020_challenge",
        "brisbane_isic_challenge_2020",
        "dermofit",
        "dermoscopedia_cc_by",
        "ham10000",
        "isic_2020_challenge_mskcc_contribution",
        "isic_2020_vienna_part_1",
        "isic_2020_vienna_part_2",
        "jid_editorial_images_2018",
        "mclass_d",
        "msk_1",
        "msk_2",
        "msk_3",
        "msk_4",
        "msk_5",
        "ph2",
        "sonic",
        "sydney_mia_smdc_2020_isic_challenge_contribution",
        "uda_1",
        "uda_2"
    ]

    assert datasets_obj.dermoscopy_datasets == expected


def test_camera_datasets(datasets_obj):
    """
    :GIVEN: A Datasets objects.
    :WHEN:  Getting the camera capture datasets.
    :THEN:  Verify only the camera capture datasets are returned.
    """
    expected = [
        "dermis",
        "dermquest",
        "mclass_nd",
        "mednode",
        "pad_ufes_20"
    ]

    assert datasets_obj.camera_datasets == expected


def test_private_dataset(datasets_obj):
    """
    :GIVEN: A Datasets objects.
    :WHEN:  Getting the private datasets.
    :THEN:  Verify only the private datasets are returned.
    """
    expected = [
        "atlas_of_dermoscopy",
        "dermofit"
    ]

    assert datasets_obj.private_datasets == expected


def test_public_dataset(datasets_obj):
    """
    :GIVEN: A Datasets objects.
    :WHEN:  Getting the public datasets.
    :THEN:  Verify only the public datasets are returned.
    """
    expected = [
        "bcn_20000",
        "bcn_2020_challenge",
        "brisbane_isic_challenge_2020",
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
        "uda_2"
    ]

    assert datasets_obj.public_datasets == expected

# def test_private_datasets():
#     expected = [
#         "atlas_of_dermoscopy",
#         "bcn_20000",
#         "bcn_2020_challenge",
#         "brisbane_isic_challenge_2020",
#         "dermofit",
#         "dermoscopedia_cc_by",
#         "dermis",
#         "dermquest",
#         "ham10000",
#         "isic_2020_challenge_mskcc_contribution",
#         "isic_2020_vienna_part_1",
#         "isic_2020_vienna_part_2",
#         "jid_editorial_images_2018",
#         "mclass_d",
#         "mclass_nd",
#         "mednode",
#         "msk_1",
#         "msk_2",
#         "msk_3",
#         "msk_4",
#         "msk_5",
#         "pad_ufes_20",
#         "ph2",
#         "sonic",
#         "sydney_mia_smdc_2020_isic_challenge_contribution",
#         "uda_1",
#         "uda_2"
#     ]
