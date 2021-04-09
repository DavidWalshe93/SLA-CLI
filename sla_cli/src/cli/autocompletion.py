"""
Author:     David Walshe
Date:       08 April 2021
"""

import logging
from typing import List

from sla_cli.src.db.accessors import AccessorFactory

logger = logging.getLogger(__name__)


def auto_complete_datasets(ctx, args, incomplete) -> List[str]:
    datasets = AccessorFactory.create_datasets()

    return [dataset for dataset in datasets.datasets.names if incomplete in dataset]
