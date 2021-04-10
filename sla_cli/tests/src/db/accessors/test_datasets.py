"""
Author:     David Walshe
Date:       09 April 2021
"""

import pytest

from sla_cli.src.db.accessors import Datasets


@pytest.fixture
def datasets_obj() -> Datasets:
    """Returns a Datasets object."""
    return Datasets()


@pytest.fixture
def dataset_names() -> callable:
    """Returns a callable that can return all dataset names in list or dict format."""

    def get(as_dict: bool = False):
        data = [
            "atlas_of_dermoscopy",
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
            "uda_2"
        ]

        return {name: [] for name in data} if as_dict else data

    return get


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


# ======================================================================================================================
# Test filtering functionality
# ======================================================================================================================

def dermoscopy_public(as_dict: bool = False):
    """Returns a list or dict of public dermoscopy datasets."""
    data = ['bcn_20000',
            'bcn_2020_challenge',
            'brisbane_isic_challenge_2020',
            'dermoscopedia_cc_by',
            'ham10000',
            'isic_2020_challenge_mskcc_contribution',
            'isic_2020_vienna_part_1',
            'isic_2020_vienna_part_2',
            'jid_editorial_images_2018',
            'mclass_d',
            'msk_1',
            'msk_2',
            'msk_3',
            'msk_4',
            'msk_5',
            'ph2',
            'sonic',
            'sydney_mia_smdc_2020_isic_challenge_contribution',
            'uda_1',
            'uda_2']

    return {name: [] for name in data} if as_dict else data


def dermoscopy_private(as_dict: bool = False):
    """Returns a list or dict of private dermoscopy datasets."""
    data = ['atlas_of_dermoscopy', 'dermofit']

    return {name: [] for name in data} if as_dict else data


def camera_public(as_dict: bool = False):
    """Returns a list or dict of public camera datasets."""
    data = ['dermis', 'dermquest', 'mclass_nd', 'mednode', 'pad_ufes_20']

    return {name: [] for name in data} if as_dict else data


def camera_private(as_dict: bool = False):
    """Returns a list or dict of private camera datasets."""
    data = []

    return {} if as_dict else data


@pytest.mark.parametrize("capture_method, availability, expected",
                         [
                             ("camera", "public", camera_public()),
                             ("camera", "private", camera_private()),
                             ("dermoscopy", "public", dermoscopy_public()),
                             ("dermoscopy", "private", dermoscopy_private()),
                         ])
def test_filter_dataset_with_list(capture_method, availability, expected, datasets_obj, dataset_names):
    """
    :GIVEN: The capture method, availability and expected output.
    :WHEN:  Filtering the dataset output by the capture method and availability.
    :THEN:  Verify the correct output is returned for the given capture method and availability.s
    """
    assert datasets_obj.filter_dataset(dataset_names(as_dict=False),
                                       capture_method=capture_method,
                                       availability=availability) == expected


@pytest.mark.parametrize("capture_method, availability, expected",
                         [
                             ("camera", "public", camera_public(as_dict=True)),
                             ("camera", "private", camera_private(as_dict=True)),
                             ("dermoscopy", "public", dermoscopy_public(as_dict=True)),
                             ("dermoscopy", "private", dermoscopy_private(as_dict=True)),
                         ])
def test_filter_dataset_with_dict(capture_method, availability, expected, datasets_obj, dataset_names):
    """
    :GIVEN: The capture method, availability and expected output.
    :WHEN:  Filtering the dataset output by the capture method and availability.
    :THEN:  Verify the correct output is returned for the given capture method and availability.s
    """
    assert datasets_obj.filter_dataset(dataset_names(as_dict=True),
                                       capture_method=capture_method,
                                       availability=availability) == expected
