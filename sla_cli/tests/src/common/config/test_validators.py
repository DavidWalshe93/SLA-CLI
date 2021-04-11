"""
Author:     David Walshe
Date:       11 April 2021
"""

import pytest
from unittest.mock import MagicMock

import sla_cli.src.common.config.validators as sut


@pytest.mark.parametrize("lower, upper, value, raises",
                         [
                             (0, 1, 1, False),
                             (0, 1, 0, False),
                             (0, 1, 1.0000001, True),
                             (0, 1, 1.5, True),
                             (10, 1, 5, True),
                             (-10, -9, -9.5, False),
                         ])
def test_is_between(lower, upper, value, raises):
    """
    :GIVEN: A lower, upper limit and a value.
    :WHEN:  CHecking if the value is between the upper and lower limit.
    :THEN:  Verify the correct responses is returned for the given inputs.
    """
    mock = MagicMock()
    mock.name = "MOCK"

    # Check if the operation raises when expected.
    if raises:
        with pytest.raises(ValueError) as exec_info:
            sut.is_between(lower, upper)(mock, mock, value)

        assert exec_info.value.args[0] == f"'MOCK' in 'MagicMock' must be between {lower} and {upper}."

    # Check if the validator passes when expected.
    else:
        sut.is_between(lower, upper)(mock, mock, value)


@pytest.mark.parametrize("limit, value, raises",
                         [
                             (0, 1, False),
                             (0, 0.00001, False),
                             (0, 0, True),
                             (0, -0, True),
                             (10, 1, True),
                             (-10, -9, False),
                         ])
def test_is_greater_than(limit, value, raises):
    """
    :GIVEN: A lower limit and a value.
    :WHEN:  Checking if the value is greater than the lower limit.
    :THEN:  Verify the correct responses is returned for the given inputs.
    """
    mock = MagicMock()
    mock.name = "MOCK"

    # Check if the operation raises when expected.
    if raises:
        with pytest.raises(ValueError) as exec_info:
            sut.greater_than(limit)(mock, mock, value)

        assert exec_info.value.args[0] == f"'MOCK' in 'MagicMock' must be greater than {limit}."

    # Check if the validator passes when expected.
    else:
        sut.greater_than(limit)(mock, mock, value)


@pytest.mark.parametrize("options, value, raises",
                         [
                             ([0, 1, 2], 1, False),
                             ([0, 1, 2], 3, True),
                             (["0", "1", "2"], "1", False),
                             (["0", "1", "2"], "3", True),
                             ([0, 1, 2], 1.00001, True),
                         ])
def test_one_of(options, value, raises):
    """
    :GIVEN: A list of options and a value.
    :WHEN:  Checking if the values is in the list of options.
    :THEN:  Verify the expected outcome for the option being in the list or not.
    """
    print([option for option in options])
    mock = MagicMock()
    mock.name = "MOCK"

    # Check if the operation raises when expected.
    if raises:
        with pytest.raises(ValueError) as exec_info:
            sut.one_of(options)(mock, mock, value)

        assert exec_info.value.args[0] == f"'MOCK' in 'MagicMock' must be one of '{[str(option).lower() for option in options]}'."

    # Check if the validator passes when expected.
    else:
        sut.one_of(options)(mock, mock, value)