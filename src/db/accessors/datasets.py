"""
Author:     David Walshe
Date:       08 April 2021
"""

import logging
from functools import wraps
from typing import Union
import re

import pandas as pd
from tabulate import tabulate
from colorama import init, Fore, Back

from src.db.accessors.base import Accessor
import src.db as db

logger = logging.getLogger(__name__)


def init_colorama(func):
    """Initialises colorama before usage."""

    @wraps(func)
    def init_colorama_wrapper(*args, **kwargs):
        init()

        return func(*args, **kwargs)

    return init_colorama_wrapper


class Datasets(Accessor):

    @property
    def datasets(self) -> db.Datasets:
        """Helper reference to access database attribute."""
        return self.db.datasets

    def names(self, tablefmt: str = "simple", output_file: str = None, regex: str = r".*") -> Union[str, None]:
        """
        Returns only the names of the datasets available.

        :param tablefmt: The console output format.
        :param output_file: If specified, the output is redirected to a file instead of to the console.
        :return: If not output_file is specified contents are printed to the screen, else the content
                 saved to the specified file.
        """
        pattern = re.compile(rf"{regex}", re.IGNORECASE | re.MULTILINE)
        names = [[name] for name in list(self.datasets.as_dict.keys()) if bool(pattern.search(name))]

        if output_file:
            df = pd.DataFrame(names, columns=["Dataset Name"])
            df.to_csv(output_file, index=None)
            return f"Saved to '{output_file}'"
        else:
            return tabulate(names, headers=["Dataset Name"], tablefmt=tablefmt, showindex=True)

    def names_and_overall_images(self, tablefmt: str = "simple", output_file: str = None):
        """
        Returns the names of the datasets available and the total number of images within the dataset.

        :param tablefmt: The console output format.
        :param output_file: If specified, the output is redirected to a file instead of to the console.
        :return: If not output_file is specified contents are printed to the screen, else the content
                 saved to the specified file.
        """
        data = [[name, sum(labels.values())] for name, labels in self.datasets.labels.items()]

        if output_file:
            df = pd.DataFrame(data, columns=["Dataset Name", "No. Images"])
            df.to_csv(output_file, index=None)
            return f"Saved to '{output_file}'"
        else:
            return tabulate(data, headers=["Dataset Name", "No. Images"], tablefmt=tablefmt, showindex=True)

    @init_colorama
    def names_and_distribution(self, tablefmt: str = "simple", output_file: str = None) -> str:
        """
        Returns the names and number of each class in each dataset.

        :param tablefmt: The console output format.
        :param output_file: If specified, the output is redirected to a file instead of to the console.
        :return: If not output_file is specified contents are printed to the screen, else the content
                 saved to the specified file.
        """
        data = []
        # Begin to capture each row.
        for dataset, values in self.datasets.labels.items():
            row = [dataset]
            headers = ["Dataset"]
            # For each row capture each dx count.
            for dx, abbrev in self.db.abbrev.items():
                item = values.get(dx, 0)
                # If showing to the console, add some color.
                if output_file is None:
                    color = Fore.RED if item == 0 else Fore.GREEN
                    item = f"{color}{item}{Fore.RESET}"
                # Add the item to the row collector.
                row.append(item)
                headers.append(abbrev)
            # Add the row to the data collector.
            data.append(row)

        if output_file:
            df = pd.DataFrame(data, columns=headers)
            df.to_csv(output_file, index=None)
            return f"Saved to '{output_file}'"
        else:
            return tabulate(data, headers=headers, tablefmt=tablefmt)
