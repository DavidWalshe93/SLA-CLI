"""
Author:     David Walshe
Date:       14 April 2021
"""

import pytest

import sla_cli.src.cli.converters as sut


@pytest.mark.parametrize("input, expected",
                         [
                             ("ph", "ph2"),
                             ("ham", "ham10000"),
                             ("pa", "pad_ufes_20"),
                             ("ms", "msk_1"),
                             ("ms2", "msk_2"),
                             ("mc", "mclass_d"),
                             ("dermo", "atlas_of_dermoscopy"),
                         ])
def test_match_datasets_cb(input, expected):
    """
    :GIVEN: A partial dataset name.
    :WHEN:  Entering dataset names to a CLI command.
    :THEN:  Verify the correct expected match is returned.
    """
    actual = sut.match_datasets_cb(None, None, [input])

    assert actual[0] == expected
