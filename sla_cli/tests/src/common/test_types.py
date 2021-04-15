"""
Author:     David Walshe
Date:       15 April 2021
"""

import pytest

import sla_cli.src.common.types as sut


@pytest.mark.parametrize("train, val, test",
                         [
                             (0.5, 0.25, 0.25),
                             (0.8, 0.1, 0.1),
                             (0.1, 0.0, 0.9),
                             (100, 0, 9),
                             (10000, 0, 100),
                             (1, 0, 1),
                         ])
def test_train_test_split(train, val, test):
    """
    :GIVEN: train/val/test values.
    :WHEN:  Creating a TrainTestSplit object.
    :THEN:  Verify the objects are created properly.
    """
    actual = sut.TrainTestSplit(train=train, validation=val, test=test)

    assert actual.train == train
    assert actual.validation == val
    assert actual.test == test


@pytest.mark.parametrize("train, val, test",
                         [
                             (0.5, 0.35, 0.25),
                             (0.8, 0.3, 0.1),
                             (0.1, 0.0, 0.1),
                         ])
def test_train_test_split_fail_float(train, val, test, caplog):
    """
    :GIVEN: train/val/test values.
    :WHEN:  Creating a TrainTestSplit object.
    :THEN:  Verify the objects are created properly.
    """
    expected = sum([train, val, test])

    with pytest.raises(SystemExit):
        sut.TrainTestSplit(train=train, validation=val, test=test)

    assert caplog.messages[-1] == f"When using floating point split values, the sum of values must equal to 1. Got {expected}."


@pytest.mark.parametrize("train, val, test",
                         [
                             (0, 1, 1),
                             (0, 1, 0),
                             (1, 1, 0),
                         ])
def test_train_test_split_fail_int_train(train, val, test, caplog):
    """
    :GIVEN: train/val/test values.
    :WHEN:  Creating a TrainTestSplit object.
    :THEN:  Verify the objects are created properly.
    """
    expected = sum([train, val, test])

    with pytest.raises(SystemExit):
        sut.TrainTestSplit(train=train, validation=val, test=test)

    if train == 0:
        assert caplog.messages[-1] == f"Number of training instances must be 1 or more. Got {train}."
    else:
        assert caplog.messages[-1] == f"Number of test instances must be 1 or more. Got {test}."

