"""
Author:     David Walshe
Date:       10 April 2021
"""

import pytest
from unittest.mock import MagicMock
from contextlib import contextmanager

from requests import Session


@pytest.fixture
def session():
    """Returns a requests session object."""
    return Session()
