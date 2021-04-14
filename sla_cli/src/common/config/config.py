"""
Author:     David Walshe
Date:       10 April 2021
"""

import logging
import os
from typing import Dict, Union
from functools import wraps

import attr
from attr.validators import instance_of
import yaml

from sla_cli.src.common.config.validators import is_between, greater_than

logger = logging.getLogger(__name__)


@attr.s
class Isic:
    """Maps the 'isic' options in the config file."""
    batch_size: int = attr.ib(validator=[instance_of(int), is_between(0, 300)], default=300)
    max_workers: int = attr.ib(validator=[instance_of(int), greater_than(0)], default=5)


def flag_if_empty(func):
    """Flags if the returned configuration is empty."""

    @wraps(func)
    def flag_if_empty_wrapper(*args, **kwargs):
        res = func(*args, **kwargs)

        if res is None:
            logger.debug(f"[CONFIG] - Configuration file exists but is empty, continuing to look for valid configurations files...")

        return res

    return flag_if_empty_wrapper


@attr.s
class Config:
    isic: Isic = attr.ib(validator=instance_of(Isic), converter=lambda config: Isic(**config))
    data_directory: str = attr.ib(validator=instance_of(str), default=os.getcwd())
    unzip: bool = attr.ib(validator=instance_of(bool), default=True)
    convert: str = attr.ib(validator=instance_of(str), converter=lambda x: x.lower(), default="original")

    def __getitem__(self, item):
        """Allows [] indexing"""
        return self.__getattribute__(item)

    @staticmethod
    def load(config_file: str = None):
        """
        Factory method to load the configuration from.

        :param config_file: The configuration file to load if specified.
        :return:
        """
        config_kwargs = None

        # Read user argument first.
        if config_file is None:
            config_kwargs = Config._read_explicit_file(config_file)

        # Environment variable loading.
        if config_kwargs is None:
            config_kwargs = Config._read_environment_variable()

        # Current working directory.
        if config_kwargs is None:
            config_kwargs = Config._read_cwd_file()

        # Default
        if config_kwargs is None:
            logger.debug(f"[CONFIG] - No valid file configuration found, loading defaults.")
            config_kwargs = Config._defaults()

        return Config(**config_kwargs)

    @staticmethod
    def _defaults():
        """Returns the Configuration defaults."""
        return {
            "isic": {}
        }

    @staticmethod
    def _read_explicit_file(config_file: str) -> Union[Dict[str, any], None]:
        """
        Reads the configuration file from an explicit file path passed by the user.

        :param config_file: The path to load the config from.
        :return: The loaded config if the path existed, else None.
        """
        if config_file is not None and os.path.exists(config_file):
            logger.debug(f"[CONFIG] - Loading config from [ARG]: '{config_file}'.")
            return Config._read(config_file)

        return None

    @staticmethod
    def _read_environment_variable() -> Union[Dict[str, any], None]:
        """
        Reads the configuration file from the environment variable:

            SLA_CLI_CONFIG_FILE

        :return: The loaded config if the env path existed, else None.
        """
        config_file = os.environ.get("SLA_CLI_CONFIG_FILE", None)
        if config_file is not None and os.path.exists(config_file):
            logger.debug(f"[CONFIG] - Loading config from [ENV]: '{config_file}'.")
            return Config._read(config_file)

        return None

    @staticmethod
    def _read_cwd_file() -> Union[Dict[str, any], None]:
        """
        Reads the configuration file from the current working directory file:

            .sla_cli_config.yml

        :return: The loaded config if the file path existed, else None.
        """
        config_file = os.path.join(os.getcwd(), ".sla_cli_config.yml")
        if config_file is not None and os.path.exists(config_file):
            logger.debug(f"[CONFIG] - Loading config from [CWD]: '{config_file}'.")
            return Config._read(config_file)

        return None

    @staticmethod
    @flag_if_empty
    def _read(config_file: str) -> Union[Dict[str, any], None]:
        """
        YAML configuration reader function.

        Loads the configuration from the config file passed in.

        :param config_file: The configuration file to read.
        :return: The loaded configuration file or None if the file does not exist.
        """
        try:
            with open(config_file) as fh:
                return yaml.safe_load(fh)
        except FileNotFoundError as e:
            logger.error(f"{e.args[0]}")
        except yaml.YAMLError as e:
            logger.error(f"{e.args[0]}")

        return None
