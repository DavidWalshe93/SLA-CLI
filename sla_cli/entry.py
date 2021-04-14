"""
Author:     David Walshe
Date:       07 April 2021
"""

import os
import sys

import logging
from dataclasses import dataclass

import click
from click import Context

if __name__ == '__main__':
    # Update PYTHONPATH for project imports.
    current_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(current_path)
    sys.path.append(parent_path)

from sla_cli.src.common.logger.init_logger import init_logger
from sla_cli.src.common.versioning import get_version
from sla_cli.src.common.console import init_colorama, init_progress_bars
from sla_cli.src.common.config import Config

from sla_cli.src.cli.context import GROUP_CONTEXT_SETTINGS
from sla_cli.src.cli.utils import kwargs_to_dataclass

# Commands
from sla_cli.src.cli.commands.ls import ls
from sla_cli.src.cli.commands.download import download
from sla_cli.src.cli.commands.organise import organise

logger = logging.getLogger(__name__)


@dataclass
class CliParameters:
    version: bool = False
    debug: bool = False
    config_file: Config = None


@click.group(**GROUP_CONTEXT_SETTINGS)
@click.option("-v", "--version", is_flag=True, help="Show the current version of the tool.")
@click.option("-d", "--debug", is_flag=True, help="Runs the tool in debug mode.")
@click.option("-f", "--config-file", type=click.STRING, help="Explicitly load a file configuration from a given path.")
@init_colorama
@init_progress_bars
@init_logger
@kwargs_to_dataclass(CliParameters)
@click.pass_context
def cli(ctx: Context, params: CliParameters):
    """
    Base SL-CLI command.
    """
    logger.debug(f"Running in debug mode.")
    ctx.obj = Config.load(config_file=params.config_file)

    if not ctx.invoked_subcommand:
        if params.version:
            logger.info(f"Version: {get_version()}")


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
    ls,
    download,
    organise
]

for command in commands:
    cli.add_command(command)

if __name__ == '__main__':
    cli()
