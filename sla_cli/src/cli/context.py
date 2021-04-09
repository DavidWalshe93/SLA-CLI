"""
Author:     David Walshe
Date:       07 April 2021
"""

import logging

logger = logging.getLogger(__name__)

# ===========================================================
# Click Context Options
# ===========================================================
COMMAND_CONTEXT_SETTINGS = {
    "context_settings": {
        "help_option_names": ["-h", "--help"],
        "max_content_width": 200
    }
}

GROUP_CONTEXT_SETTINGS = {
    **COMMAND_CONTEXT_SETTINGS,
    "invoke_without_command": True
}
