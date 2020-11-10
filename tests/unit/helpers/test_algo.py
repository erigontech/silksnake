# -*- coding: utf-8 -*-
"""The unit test for algo module."""

import typing
import pytest

from silksnake.helpers import algo

# pylint: disable=line-too-long,no-self-use,unnecessary-lambda

@pytest.mark.parametrize("lower_bound,upper_bound,predicate,result,should_pass", [
    # Valid test list
    (0, 0, (lambda i: i > 5), 0, True),
    (0, 10, (lambda i: i > 5), 6, True),
    (0, 20, (lambda i: i > 5), 6, True),
    (6, 20, (lambda i: i < 5), 20, True),

    # Invalid test list
    ('0', '0', (lambda i: i > 5), 0, False),
    (0, '0', (lambda i: i > 5), 0, False),
    ('0', 0, (lambda i: i > 5), 0, False),
    ('a', 0, (lambda i: i > 5), 0, False),
])
def test_binary_search(lower_bound: int, upper_bound: int, predicate: typing.Callable[[int], bool], result: int, should_pass: bool):
    """ Unit test for binary_search. """
    if should_pass:
        assert algo.binary_search(lower_bound, upper_bound, predicate) == result
    else:
        with pytest.raises((TypeError)):
            algo.binary_search(lower_bound, upper_bound, predicate)
