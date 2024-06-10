#!/usr/bin/env python3
""" task 0 """
import random
import asyncio


async def wait_random(max_delay: int = 10) -> float:
    """ function that waits for a random delay between 0 and max_delay """
    waiting_time = random.uniform(0, max_delay)
    await asyncio.sleep(waiting_time)
    return waiting_time
