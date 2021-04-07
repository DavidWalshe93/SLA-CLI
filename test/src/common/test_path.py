"""
Author:     David Walshe
Date:       07 April 2021
"""

import pytest
import os


import src.common.path as sut


def test_root_dir():

    expected = os.path.dirname(os.getcwd())

    assert sut.Path.root_dir() == expected