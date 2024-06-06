#!/usr/bin/env python3
""" module for element_length fnuction """
from typing import Sequence, Union, Any


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """ function that returns the first element of a sequence """
    if lst:
        return lst[0]
    else:
        return None
