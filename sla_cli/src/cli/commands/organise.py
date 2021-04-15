"""
Author:     David Walshe
Date:       14 April 2021
"""

import logging
import logging
import os
from typing import List, Union, Tuple
from dataclasses import dataclass, asdict
import hashlib

import click
import pandas as pd
from click import Context
from click.exceptions import BadOptionUsage

from sla_cli.src.cli.context import COMMAND_CONTEXT_SETTINGS
from sla_cli.src.cli.utils import kwargs_to_dataclass, default_from_context
from sla_cli.src.cli.converters import match_datasets_cb, match_dx_cb, train_test_split_cb
from sla_cli.src.common.types import TrainTestSplit

logger = logging.getLogger(__name__)


@dataclass
class OrganiseParameters:
    datasets: List[str]
    directory: str
    include: List[str]
    exclude: List[str]
    method: str
    fixed_test_set: str
    fixed_train_set: str
    split: TrainTestSplit
    stratify: bool


def read_ids_cb(ctx, param, file_path: str) -> List[str]:
    """
    Reads a csv file and returns the content of the id row.

    :param file_path: The file path to read the csv from.
    :return: A list of IDs.
    """
    if file_path is None:
        return None
    try:
        return list(pd.read_csv(file_path)["id"])
    except Exception as err:
        raise click.BadParameter(f"Cannot read 'ids' from file '{file_path}'.", ctx, param)


def method_cb(ctx, param, method) -> str:
    """Returns the type of method used for capture as seen in the metadata."""
    return {
        "biopsy": "histopathology",
        "single": "single image expert consensus",
        "serial": "serial imaging showing no change",
        "confocal": "confocal microscopy with consensus dermoscopy",
    }.get(method, "all")


@click.command(**COMMAND_CONTEXT_SETTINGS, short_help="Organises datasets into train/validation/splits.")
@click.argument("datasets", type=click.STRING, callback=match_datasets_cb, nargs=-1)
@click.option("-d", "--directory", type=click.STRING, cls=default_from_context("data_directory"), help="The destination directory for the downloaded content. Default is the current work directory.")
@click.option("-i", "--include", type=click.STRING, multiple=True, default=None, callback=match_dx_cb,
              help="Used to exclude specific classes in the data. Option in mutually exclusive to '-e/--exclude'.")
@click.option("-e", "--exclude", type=click.STRING, multiple=True, default=None, callback=match_dx_cb,
              help="Used to include specific classes in the data. Option in mutually exclusive to '-i/--include'.")
@click.option("-m", "--method", type=click.Choice(["biopsy", "confocal", "serial", "single", "all"], case_sensitive=False),
              default="all", callback=method_cb, help="The method by which the lesion diagnosis was reached. Defaults to 'all'.")
@click.option("--fixed-test-set", type=click.STRING, default=None, callback=read_ids_cb, help="Specifies a fixed test set provided as a a csv with an 'id' field.")
@click.option("--fixed-train-set", type=click.STRING, default=None, callback=read_ids_cb, help="Specifies a fixed training set provided as a a csv with an 'id' field.")
@click.option("-s", "--split", type=click.STRING, default=".7:.15:.15", metavar="<TRAIN>:<VAL>:<TEST>", callback=train_test_split_cb,
              help="Specifies the dataset split ratio. Inputted as TRAIN:VAL:TEST. "
                   "\n\nFloating-point values will provide ratio splits, sum of which must = 1."
                   "\n\nInteger values provide the number of instances for each split."
                   "\n\nDefaults to train=70%, val=15%, test=15%."
                   "\n\nTRAIN and TEST values are ignored if --fixed-test-set/--fixed-train-set is specified.")
@click.option("--stratify", is_flag=True, help="If using split with floating point numbers, this will enable stratification on the 'dx' field.")
@kwargs_to_dataclass(OrganiseParameters)
@click.pass_context
def organise(ctx: Context, params: OrganiseParameters):
    if all([params.include, params.exclude]):
        raise BadOptionUsage("include", f"'-i/--include' and '-e/--exclude' switches cannot be used together.")

    # Filter archive files and an exclusion list.
    available_datasets = [dataset for dataset in os.listdir(params.directory) if dataset.find(".") == -1]

    metadata = gather_metadata(params.directory, params.datasets, available_datasets)

    if len(metadata) == 0:
        logger.error(f"No metadata available for datasets provided.")
        exit()

    df = metadata.pop()
    for meta in metadata:
        df = df.append(meta, sort=False)

    df = keep_includes(params.include, df)
    df = remove_excludes(params.exclude, df)
    df = keep_dx_type(params.method, df)

    # train_df, val_df, test_df = None, None, None

    logger.info(f"Total instances found after filtering: {df.shape[0]}")

    df, test_df = extract_fixed_set(params.fixed_test_set, df, "test_set")
    df, train_df = extract_fixed_set(params.fixed_train_set, df, "train_set")

    print("test", test_df.shape[0])
    print("train", train_df)
    print(df.shape[0])


def gather_metadata(data_directory: str, datasets: List[str], available_datasets: List[str]) -> List[pd.DataFrame]:
    """
    Reads metadata for multiple different datasets and concatenates them together.

    :param data_directory: The user specified directory that contains data.
    :param datasets: The datasets to gather metadata for.
    :param available_datasets: The available datasets on disk.
    :return: A list of dataframes containing metadata.
    """
    metadata = []
    for dataset in datasets:
        # If datasets are missing, flag it to the user and exit.
        if dataset not in available_datasets:
            logger.error(f"Missing data for '{dataset}', use 'sla-cli download <DATASET>' to continue.")
            exit()
        # Add datasets to metadata
        else:
            path = os.path.join(data_directory, dataset, "metadata.csv")
            metadata.append(read_metadata(path))

    return metadata


def read_metadata(path: str) -> pd.DataFrame:
    """
    Reads a metadata file as a pandas dataframe.

    :param path: The path to read the data from.
    :return: The metadata as a pandas dataframe.
    :raises SystemExit: If the metadata file does not exist.
    """
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        logger.error(f"Could not find 'metadata.csv' in {path}.\n\nNote: Don't use the --metadata-as-name switch when downloading if using the data for automated processes.")
        exit()


def keep_includes(includes: List[str], metadata: pd.DataFrame) -> pd.DataFrame:
    if not includes:
        return metadata

    return metadata[metadata["dx"].isin(includes)]


def remove_excludes(excludes: List[str], metadata: pd.DataFrame) -> pd.DataFrame:
    if not excludes:
        return metadata

    return metadata[~metadata["dx"].isin(excludes)]


def keep_dx_type(dx_type: str, metadata: pd.DataFrame) -> pd.DataFrame:
    if dx_type == "all":
        return metadata

    return metadata[metadata["dx_type"] == dx_type]


def extract_fixed_set(fixed_set: List[str], df: pd.DataFrame, set_type: str) -> Tuple[pd.DataFrame, Union[pd.DataFrame, None]]:
    if set_type not in ["test_set", "train_set"]:
        raise ValueError(f"'set_type' needs to be one of ['test_set', 'train_set'], got {set_type}")

    caption = '--fixed-test-set' if set_type == "test_set" else "--fixed-train-set"

    fixed_df = None
    if fixed_set:
        # fixme Need to add a way of referencing all datasets uniformly i.e. Global ID.
        fixed_df = df[df["image_name"].isin(fixed_set)]
        if fixed_df.shape[0] != len(fixed_set):
            logger.warning(f"The number of instances prescribed in the '{caption}' was not found in the datasets passed")
            logger.warning(f"'{len(fixed_set)}' instances were requested but only '{fixed_df.shape[0]}' were found.")
        df = df[~df["image_name"].isin(fixed_set)]

    return df, fixed_df
