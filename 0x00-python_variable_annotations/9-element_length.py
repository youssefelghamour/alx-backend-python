#!/usr/bin/env python3
""" module for element_length fnuction """
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """ Function that returns a list of tuples """
    return [(i, len(i)) for i in lst]
