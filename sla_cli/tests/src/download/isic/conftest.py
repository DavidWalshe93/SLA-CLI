"""
Author:     David Walshe
Date:       10 April 2021
"""

import pytest

from sla_cli.src.download.downloader import DownloaderOptions


@pytest.fixture
def sample_isic_records():
    """Returns two isic archive metadata records."""
    return [
        {
            '_id': '5436e3abbae478396759f0cf',
            '_modelType': 'image',
            'created': '2014-10-09T19:36:11.989000+00:00',
            'creator': {'_id': '5450e996bae47865794e4d0d', 'name': 'User 6VSN'},
            'dataset': {'_accessLevel': 0,
                        '_id': '5a2ecc5e1165975c945942a2',
                        'description': 'Moles and melanomas.\n'
                                       'Biopsy-confirmed melanocytic lesions. Both '
                                       'malignant and benign lesions are included.',
                        'license': 'CC-0',
                        'name': 'UDA-1',
                        'updated': '2014-11-10T02:39:56.492000+00:00'},
            'meta': {'acquisition': {'image_type': 'dermoscopic',
                                     'pixelsX': 1022,
                                     'pixelsY': 767},
                     'clinical': {'age_approx': 55,
                                  'anatom_site_general': 'anterior torso',
                                  'benign_malignant': 'benign',
                                  'diagnosis': 'nevus',
                                  'diagnosis_confirm_type': None,
                                  'melanocytic': True,
                                  'sex': 'female'}},
            'name': 'ISIC_0000000',
            'notes': {'reviewed': {'accepted': True,
                                   'time': '2014-11-10T02:39:56.492000+00:00',
                                   'userId': '5436c6e7bae4780a676c8f93'},
                      'tags': ['Challenge 2018: Task 1-2: Training',
                               'Challenge 2019: Training',
                               'Challenge 2016: Training',
                               'Challenge 2017: Training']},
            'updated': '2015-02-23T02:48:17.495000+00:00'
        },
        {
            '_id': '5436e3acbae478396759f0d1',
            '_modelType': 'image',
            'created': '2014-10-09T19:36:12.070000+00:00',
            'creator': {'_id': '5450e996bae47865794e4d0d', 'name': 'User 6VSN'},
            'dataset': {'_accessLevel': 0,
                        '_id': '5a2ecc5e1165975c945942a2',
                        'description': 'Moles and melanomas.\n'
                                       'Biopsy-confirmed melanocytic lesions. Both '
                                       'malignant and benign lesions are included.',
                        'license': 'CC-0',
                        'name': 'UDA-1',
                        'updated': '2014-11-10T02:39:56.492000+00:00'},
            'meta': {'acquisition': {'image_type': 'dermoscopic',
                                     'pixelsX': 1022,
                                     'pixelsY': 767},
                     'clinical': {'age_approx': 30,
                                  'anatom_site_general': 'anterior torso',
                                  'benign_malignant': 'benign',
                                  'diagnosis': 'nevus',
                                  'diagnosis_confirm_type': None,
                                  'melanocytic': True,
                                  'sex': 'female'}},
            'name': 'ISIC_0000001',
            'notes': {'reviewed': {'accepted': True,
                                   'time': '2014-11-10T02:39:56.492000+00:00',
                                   'userId': '5436c6e7bae4780a676c8f93'},
                      'tags': ['Challenge 2018: Task 1-2: Training',
                               'Challenge 2019: Training',
                               'Challenge 2016: Training',
                               'Challenge 2017: Training']},
            'updated': '2015-02-23T02:48:27.455000+00:00'
        }
    ]


@pytest.fixture
def expected_column_names():
    """Expected column names for metadata."""
    return [
        "isic_id",
        "image_name",
        "dataset",
        "description",
        "accepted",
        "created",
        "tags",
        "pixels_x",
        "pixels_y",
        "age",
        "sex",
        "localization",
        "benign_malignant",
        "dx",
        "dx_type",
        "melanocytic"
    ]


@pytest.fixture
def expected_extended_column_names():
    """Expected column names for metadata after year tagging."""
    return [
        "isic_id",
        "image_name",
        "dataset",
        "description",
        "accepted",
        "created",
        "tags",
        "pixels_x",
        "pixels_y",
        "age",
        "sex",
        "localization",
        "benign_malignant",
        "dx",
        "dx_type",
        "melanocytic",
        "2016"
        "2017"
        "2018"
        "2019"
        "2020"
    ]
