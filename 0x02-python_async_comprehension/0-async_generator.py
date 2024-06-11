#!/usr/bin/env python3
""" task 0 """
import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """ function that generates a 10 random numbers between 0 & 10 """
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
