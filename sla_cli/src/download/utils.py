"""
Author:     David Walshe
Date:       10 April 2021
"""

import logging
from functools import wraps

from requests import Session

logger = logging.getLogger(__name__)


def inject_http_session(func):
    """Injects a persistent HTTP session into the wrapped function."""

    @wraps(func)
    def inject_http_session_wrapper(*args, **kwargs):
        with Session() as session:
            return func(*args, session=session, **kwargs)

    return inject_http_session_wrapper
