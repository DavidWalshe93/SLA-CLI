"""
Author:     David Walshe
Date:       07 April 2021
"""

import logging
from dataclasses import dataclass

import click
from click import Context

from src.common.logger.init_logger import init_logger
from src.cli.context import GROUP_CONTEXT_SETTINGS
from src.cli.utils import kwargs_to_dataclass

# from setup import __version__

# Commands
from src.cli.commands.ls import ls

logger = logging.getLogger(__name__)

__version__ = "0.0.1"


@dataclass
class CliParameters:
    version: bool = False


@click.group(**GROUP_CONTEXT_SETTINGS)
@click.option("-v", "--version", is_flag=True, help="Show the current version of the tool.")
@kwargs_to_dataclass(CliParameters)
@click.pass_context
def cli(ctx: Context, params: CliParameters):
    """
    Base SL-CLI command.
    """
    init_logger()
    if not ctx.invoked_subcommand:
        if params.version:
            print(f"Version: {__version__}")


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
    ls
]

for command in commands:
    cli.add_command(command)

if __name__ == '__main__':
    cli()
