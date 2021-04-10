"""
Author:     David Walshe
Date:       09 April 2021
"""

import logging
import codecs
import os

from .path import Path

logger = logging.getLogger(__name__)


def read_init():
    with codecs.open(os.path.join(Path.project_root(), "__init__.py"), 'r') as fh:
        return fh.read()


def get_version():
    for line in read_init().splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
