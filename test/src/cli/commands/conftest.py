"""
Author:     David Walshe
Date:       07 April 2021
"""

import os
import pytest


@pytest.fixture
def read_actual_csv() -> callable:
    """
    Function to read the actual output content of a ls command and
    returns the content as a string.
    """

    def read() -> str:
        with open("test.csv") as fh:
            return fh.read()

    return read


def resource_loader(resource: str) -> str:
    """Loads a resource from the resource folder."""
    with open(os.path.join(os.path.dirname(__file__), "res", resource)) as fh:
        return fh.read()


@pytest.fixture
def dataset_names_print():
    """Returns the expected dataset names included in the tool."""
    return resource_loader("dataset_names_print.txt")


@pytest.fixture
def dataset_names_csv():
    """Returns the expected dataset names included in the tool."""
    return resource_loader("dataset_names.csv")


@pytest.fixture
def dataset_names_totals_print():
    """Returns the number of images for each dataset"""
    return resource_loader("dataset_names_totals_print.txt")


@pytest.fixture
def dataset_names_totals_csv():
    """Returns the number of images for each dataset"""
    return resource_loader("dataset_names_totals.csv")


@pytest.fixture
def dataset_names_all_print():
    """Returns the distribution of images for each dataset"""
    return resource_loader("dataset_names_all_print.txt")


@pytest.fixture
def dataset_names_all_csv():
    """Returns the distribution of images for each dataset"""
    return resource_loader("dataset_names_all.csv")


@pytest.fixture
def legend_print():
    """Returns the distribution of images for each dataset"""
    return resource_loader("legend_print.txt")
