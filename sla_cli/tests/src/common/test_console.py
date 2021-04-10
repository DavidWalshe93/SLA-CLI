"""
Author:     David Walshe
Date:       09 April 2021
"""

import pytest

import sla_cli.src.common.console as sut


@pytest.mark.parametrize("title, char",
                         [
                             ("Header1", "="),
                             ("Header2", "*"),
                             ("Header3", "="),
                             ("Header4", "-"),
                         ])
def test_make_header(title, char):
    """
    :GIVEN: A title string and format character.
    :WHEN:  Creating a console header.
    :THEN:  Verify the header format is created as expected
    """
    expected = f"{char * 100}\n" \
               f"{title}\n" \
               f"{char * 100}"

    # Default for char.
    if char == "=":
        actual = sut.make_header(title)
    else:
        actual = sut.make_header(title, char)

    assert actual == expected
