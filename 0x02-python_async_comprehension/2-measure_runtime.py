#!/usr/bin/env python3
""" task 2 """
import asyncio
import time


async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """ Function that measures the total runtime of executing
        async_comprehension four times in parallel

        The total runtime is 10 seconds instead of 40 because asyncio.gather
        runs the four async_comprehension coroutines at the same time """
    start_time = time.time()
    asyncio.gather(*(async_comprehension() for _ in range(4)))
    end_time = time.time()
    return end_time - start_time
