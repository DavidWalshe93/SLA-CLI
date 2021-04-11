# SLA-CLI

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://gitHub.com/DavidWalshe93/SLA-CLI/graphs/commit-activity)
[![Build Status](https://travis-ci.com/DavidWalshe93/SLA-CLI.svg?branch=main)](https://travis-ci.com/DavidWalshe93/SLA-CLI)
[![Coverage Status](https://coveralls.io/repos/github/DavidWalshe93/SLA-CLI/badge.svg)](https://coveralls.io/github/DavidWalshe93/SLA-CLI)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b30557dbc38741c6b3e42f8cf9f91870)](https://app.codacy.com/gh/DavidWalshe93/SLA-CLI?utm_source=github.com&utm_medium=referral&utm_content=DavidWalshe93/SLA-CLI&utm_campaign=Badge_Grade_Settings)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/sla-cli.svg)](https://pypi.python.org/pypi/sla-cli/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/sla-cli.svg)](https://pypi.python.org/pypi/sla-cli/)
[![Downloads](https://pepy.tech/badge/sla-cli)](https://pepy.tech/project/sla-cli)

> A Skin Lesion Acquisition (SLA) CLI tool designed to help source data for skin lesion research.

## Introduction

While working on an academic project in the domain of automatic skin lesion detection it became clear that there was no
easy way to track down datasets cited highly in the literature

This is what motivated the creation of **SDA-CLI**.

**SDA-CLI** is targeted toward academic and medical researchers looking to source lesion dataset quickly to accelerate
their research efforts.

## Features at a Glance

**Available**

-  Dataset summaries and label distribution.
-  Console-based dashboards.

**WIP**

-  Matplotlib integration for data distribution visualisation.
-  Dataset downloading (public datasets only).
-  Metadata extraction on applicable datasets.
-  Data background information sources and links.
-  Preprocessing of datasets for *binary classification*.

## Loading Configurations

There are three ways to load configuration files when using the CLI interface.

1) The first method is using an explicit YAML configuration file like so:

    ```shell
    sla-cli -f/--config-file <FILE_PATH> <COMMAND> ...
    ```

<br>

2) The second method is referencing the **SLA_CLI_CONFIG_FILE** environment variable. Once the variable is set, it will
   auto-reference the environment variables value, which should be a path to the configuration file you wish to load
   into the tool.

<br>

3) The third and final method of loading a configuration with the tool is creating a "*.sla_cli_config.yml*" file in the
   directory you plan to run the tool in. This method is helpful if you wish to check-in your configuration to SCM.

## Commands

The following sub sections discuss the how to use the tool.

The following conventions are used to describe tool usage.

```shell
<NAME>                 ---> Required argument.

[NAME: DEFAULT_VALUE]  ---> Optional argument showing default value. 
```

If unsure of how to use a command, use **-h/--help** on any command to get context on what commands are available and
what they do.

### ls

The **ls** command is to gain quick insight into what data is available.

```shell
sla-cli ls [regex: '.*']              # Shows a list of dataset names available.
sla-cli ls -v totals [regex: '.*']    # Shows a list of dataset names and the number of images it contains.
sla-cli ls -v all [regex: '.*']       # Shows a list of dataset names and a full breakdown of all image label distribution
```

A sample of the **sla-cli ls -v all** output is shown below:

![img.png](docs/img.png)
*Sample output of 'sla-cli ls -v all' command.*