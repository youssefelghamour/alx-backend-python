#!/usr/bin/env python3
""" task 1 """
import asyncio
from typing import List


task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """ function that executes wait_random n times
        with the specified max_delay """
    tasks = [task_wait_random(max_delay) for _ in range(n)]
    result = await asyncio.gather(*tasks)
    return sorted(result)
