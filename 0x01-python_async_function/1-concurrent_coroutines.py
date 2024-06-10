#!/usr/bin/env python3
""" task 1 """
import random
import asyncio
from typing import List


wait_random = __import__('0-basic_async_syntax.py').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """ function that executes wait_random n times
        with the specified max_delay """
    result = await asyncio.gather(*(wait_random(max_delay) for _ in range(n)))
    return sorted(result)
