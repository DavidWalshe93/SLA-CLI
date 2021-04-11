"""
Author:     David Walshe
Date:       10 April 2021
"""

import pytest

import yaml

import sla_cli.src.common.config as sut


@pytest.fixture
def config() -> dict:
    """Returns the config."""
    return {
        "py": "test",
        "test": "py",
    }


@pytest.fixture
def config_file(config, tmpdir):
    """Creates a test configuration."""
    config_file = tmpdir.join(".sla_cli_config.yml")
    with open(config_file, "w") as fh:
        yaml.safe_dump(config, fh)

        return config_file.__str__()


def test_read_explicit_file(config_file, config, tmpdir):
    """
    :GIVEN: A configuration file path.
    :WHEN:  Loading an explicit config file.
    :THEN:  Verify the correct file is loaded.
    """
    assert sut.Config._read_explicit_file(config_file) == config


def test_read_cwd_file(config_file, config, tmpdir):
    """
    :GIVEN: Nothing.
    :WHEN:  Loading the config file from the cwd.
    :THEN:  Verify the correct file is loaded.
    """
    with tmpdir.as_cwd():
        assert sut.Config._read_cwd_file() == config


def test_environment_variable(config_file, config, monkeypatch):
    """
    :GIVEN: Nothing.
    :WHEN:  Loading the config file from an environment variable.
    :THEN:  Verify the correct file is loaded.
    """
    monkeypatch.setenv("SLA_CLI_CONFIG_FILE", config_file)
    assert sut.Config._read_environment_variable() == config
