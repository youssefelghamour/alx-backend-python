#!/usr/bin/env python3
""" module for to_kv fnuction """
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """ function that makes a tuple of key(string), value(float) """
    x: Tuple[str, float] = (k, float(v**2))
    return x
