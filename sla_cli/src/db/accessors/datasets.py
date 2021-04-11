"""
Author:     David Walshe
Date:       08 April 2021
"""

import logging
from typing import Union, List, Dict

import pandas as pd
from tabulate import tabulate
from colorama import Fore

from sla_cli.src.db.accessors.base import Accessor
from sla_cli.src.common.regex import compile_regex
from sla_cli.src.common.console import make_header
import sla_cli.src.db as db

logger = logging.getLogger(__name__)


class Datasets(Accessor):

    @property
    def datasets(self) -> db.Datasets:
        """Helper reference to access database attribute."""
        return self.db.datasets

    def __getitem__(self, item):
        """Allows [] indexing of Datasets."""
        return self.datasets[item]

    @property
    def private_datasets(self) -> List[str]:
        """Returns only the private dataset names."""
        return [dataset for dataset, info in self.datasets.info.items() if info["availability"] == "private"]

    @property
    def public_datasets(self) -> List[str]:
        """Returns only the public dataset names."""
        return [dataset for dataset, info in self.datasets.info.items() if info["availability"] == "public"]

    @property
    def dermoscopy_datasets(self) -> List[str]:
        """Returns only the dataset names that are captured using dermoscopy."""
        return [dataset for dataset, info in self.datasets.info.items() if info["capture_method"] == "dermoscopy"]

    @property
    def camera_datasets(self) -> List[str]:
        """Returns only the dataset names that are captured using cameras."""
        return [dataset for dataset, info in self.datasets.info.items() if info["capture_method"] == "camera"]

    def availability_filter(self, key: str, default: Union[List[str], Dict[str, any]]) -> List[str]:
        """
        Runs a filter on the dataset, returning only those meeting the availability criteria passed.

        :param key: The criteria to check for.
        :param default: The default value to return if no criteria matches.
        :return: The output of the resulting.
        """
        return {
            "private": self.private_datasets,
            "public": self.public_datasets
        }.get(key, default)

    def capture_method_filter(self, key: str, default: Union[List[str], Dict[str, any]]) -> List[str]:
        """
        Runs a filter on the dataset, returning only those meeting the capture method criteria passed.

        :param key: The criteria to check for.
        :param default: The default value to return if no criteria matches.
        :return: The output of the resulting.
        """
        return {
            "dermoscopy": self.dermoscopy_datasets,
            "camera": self.camera_datasets
        }.get(key, default)

    def filter_dataset(self, datasets: Union[List[str], Dict[str, any]], *, capture_method: str, availability: str,
                       **kwargs) -> List:
        """
        Filters a dataset bases on it's capture method and availability.

        :param datasets: The datasets to filter.
        :param capture_method: The capture method filter.
        :param availability: The availability filter.
        :return: The remaining datasets, post filter.
        """

        default = list(datasets.keys()) if isinstance(datasets, dict) else datasets

        # Filter on both capture method and availability. Return only the datasets common to both filters.
        overall_filter = list(set(self.availability_filter(availability, default))
                              .intersection(self.capture_method_filter(capture_method, default)))

        # Create the result to meet the same type as the input.
        if isinstance(datasets, dict):
            datasets = {dataset: item for dataset, item in datasets.items() if dataset in overall_filter}
        else:
            datasets = [dataset for dataset in datasets if dataset in overall_filter]

        return datasets

    def names(self, tablefmt: str = "simple", output_file: str = None, regex: str = r".*", **kwargs) -> Union[str, None]:
        """
        Returns only the names of the datasets available.

        :param tablefmt: The console output format.
        :param output_file: If specified, the output is redirected to a file instead of to the console.
        :param regex: Regex search term to filter the return content.
        :return: If not output_file is specified contents are printed to the screen, else the content
                 saved to the specified file.
        """
        pattern = compile_regex(regex)
        datasets = self.filter_dataset(list(self.datasets.as_dict.keys()), **kwargs)
        names = [[name] for name in datasets if bool(pattern.search(name))]

        if output_file:
            df = pd.DataFrame(names, columns=["Dataset Name"])
            df.to_csv(output_file, index=None)
            return f"Saved to '{output_file}'"
        else:
            return tabulate(names, headers=["Dataset Name"], tablefmt=tablefmt, showindex=True)

    def names_and_overall_images(self, tablefmt: str = "simple", output_file: str = None, regex: str = r".*", **kwargs):
        """
        Returns the names of the datasets available and the total number of images within the dataset.

        :param tablefmt: The console output format.
        :param output_file: If specified, the output is redirected to a file instead of to the console.
        :param regex: Regex search term to filter the return content.
        :return: If not output_file is specified contents are printed to the screen, else the content
                 saved to the specified file.
        """
        pattern = compile_regex(regex)
        datasets = self.filter_dataset(self.datasets.labels, **kwargs)
        data = [[name, sum(labels.values())] for name, labels in datasets.items() if bool(pattern.search(name))]

        if output_file:
            df = pd.DataFrame(data, columns=["Dataset Name", "No. Images"])
            df.to_csv(output_file, index=None)
            return f"Saved to '{output_file}'"
        else:
            return tabulate(data, headers=["Dataset Name", "No. Images"], tablefmt=tablefmt, showindex=True)

    def names_and_distribution(self, tablefmt: str = "simple", output_file: str = None, regex: str = r".*",
                               **kwargs) -> str:
        """
        Returns the names and number of each class in each dataset.

        :param tablefmt: The console output format.
        :param output_file: If specified, the output is redirected to a file instead of to the console.
        :param regex: Regex search term to filter the return content.
        :return: If not output_file is specified contents are printed to the screen, else the content
                 saved to the specified file.
        """
        pattern = compile_regex(regex)
        datasets = self.filter_dataset(self.datasets.labels, **kwargs)
        dataset_labels = {dataset: labels for dataset, labels in datasets.items() if bool(pattern.search(dataset))}

        data, headers = [], []
        # Begin to capture each row.
        for dataset, values in dataset_labels.items():
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
            return tabulate(data, headers=headers, tablefmt=tablefmt, showindex=True)

    def names_information(self, regex: str = r".*", **kwargs) -> str:
        """
        Shows information on each dataset.

        :param regex: The regex filter to limit datasets to.
        :return: The formated information on each dataset.
        """
        pattern = compile_regex(regex)
        datasets = self.filter_dataset(self.datasets.info, **kwargs)
        dataset_info = {dataset: info for dataset, info in datasets.items() if bool(pattern.search(dataset))}

        collector = []
        for dataset, info in dataset_info.items():
            collector.append(make_header(f"{dataset}"))
            collector.append(info.__str__())

        return "\n".join(collector)
