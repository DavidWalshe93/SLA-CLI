"""
Author:     David Walshe
Date:       07 April 2021
"""

import os
import pytest


def resource_loader(resource: str) -> str:
    """Loads a resource from the resource folder."""
    with open(os.path.join(os.path.dirname(__file__), "res", resource)) as fh:
        return fh.read()


@pytest.fixture
def dataset_names():
    """Returns the expected dataset names included in the tool."""
    return resource_loader("dataset_names.txt")


@pytest.fixture
def dataset_names_totals():
    """Returns the number of images for each dataset"""
    return resource_loader("dataset_names_totals.txt")
