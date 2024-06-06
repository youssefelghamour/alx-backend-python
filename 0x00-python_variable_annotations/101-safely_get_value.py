#!/usr/bin/env python3
""" module for safely_get_value fnuction """
from typing import Dict, Any, TypeVar, Union


T = TypeVar('T')


def safely_get_value(dct: Dict[Any, Any], key: Any, default: T = None) -> Union[Any, T]:
    """ function that gets a value from a dictionary"""
    if key in dct:
        return dct[key]
    else:
        return default
