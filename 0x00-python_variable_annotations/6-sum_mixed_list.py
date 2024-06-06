#!/usr/bin/env python3
""" module for sum_mixed_list fnuction """
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """ function that sums a list of ints """
    return float(sum(x for x in mxd_lst))
