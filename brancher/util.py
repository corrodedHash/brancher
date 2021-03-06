"""Contains helper functions"""
import math
import random


def log_weight_random(start: int, end: int, base: float = 2) -> int:
    """Returns a random int, with logarithmic probability distribution"""
    assert start < end
    randrange_end = math.ceil(base ** ((end + 1 - start)) - 1)
    randint = random.randint(1, randrange_end)
    result = min(int(math.floor(math.log(randint + start, base))), end)
    result = start + end - result
    return result
