#!/usr/bin/env python3
""" module for sum_list fnuction """
from typing import List


def sum_list(input_list: List[float]) -> float:
    """ function that sums a list of floats """
    return sum(x for x in input_list)
