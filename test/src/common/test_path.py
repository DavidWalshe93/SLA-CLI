"""
Author:     David Walshe
Date:       07 April 2021
"""

import pytest
import os


import src.common.path as sut


def test_root_dir():
    """
    :GIVEN: Nothing.
    :WHEN:  Getting the project root path.
    :THEN:  Verify if the expected path is returned.
    """
    expected = os.path.dirname(os.getcwd())

    assert sut.Path.root_dir() == expected
    

def test_db():
    """
    :GIVEN: Nothing.
    :WHEN:  Getting the path to the DB JSON file.
    :THEN:  Verify the correct path is returned.
    """
    expected = os.path.join(os.path.dirname(os.getcwd()), "db.json")

    assert sut.Path.db() == expected