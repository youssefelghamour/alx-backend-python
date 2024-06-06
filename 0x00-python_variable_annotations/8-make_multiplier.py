#!/usr/bin/env python3
""" module for make_multiplier fnuction """
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """ function that returns another multiplier function """

    def multiplier_function(value: float) -> float:
        """ function that multiplies a float by the multiplier """
        return value * multiplier

    return multiplier_function
