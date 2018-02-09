import math
import time

def get_microseconds():
    """Returns a time measurement in micro-seconds, rounded to the next µs"""
    return math.ceil(time.perf_counter() * 1000000)
