"""
Author:     David Walshe
Date:       07 April 2021
"""

import logging

import click

from src.cli.config import GROUP_CONTEXT_SETTINGS

logger = logging.getLogger(__name__)


@click.group(**GROUP_CONTEXT_SETTINGS)
def cli(**kwargs):
    """
    Base SL-CLI command.
    """
    pass


# ==================================================
# Add CLI groups
# ==================================================
groups = [

]

for group in groups:
    cli.add_command(group)

# ==================================================
# Add CLI commands
# ==================================================
commands = [
]

for command in commands:
    cli.add_command(command)

if __name__ == '__main__':
    cli()
