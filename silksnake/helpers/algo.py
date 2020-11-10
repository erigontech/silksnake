# -*- coding: utf-8 -*-
"""Common algorithms."""

from typing import Callable

def binary_search(lower_bound: int, upper_bound: int, predicate: Callable[[int], bool]) -> int:
    """ Search and return the least x in ordered  set S=[lower_bound, upper_bound) for which predicate P(x) is true.
        Predicate P must be assumed s.t. for all x in ordered set S, P(x) implies P(y) for all y > x.
        If no x is found s.t. P(x) is true, return upper_bound + 1.
        @param lower_bound: lower bound of the search
        @param upper_bound: upper bound of the search
        @param predicate: unary function which returns true or false
    """
    index = upper_bound

    while lower_bound < upper_bound:
        mid = lower_bound + (upper_bound - lower_bound) // 2
        if predicate(mid):
            index = upper_bound = mid
        else:
            lower_bound = mid + 1

    return index
