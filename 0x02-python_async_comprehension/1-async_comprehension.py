#!/usr/bin/env python3
""" task 1 """
import asyncio
from typing import List


async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """ function that returns a list of 10 random numbers using an async
        comprehensing from async_generator """
    return [number async for number in async_generator()]
