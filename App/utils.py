import datetime
import time

import netaddr


def ipv4_to_int(ip: str) -> int:
    return int(netaddr.IPAddress(ip))


def timed(func):
    """
    records approximate durations of function calls
    """

    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        print(f'{func.__name__:<30} started')
        result = func(*args, **kwargs)
        duration = f'{func.__name__:<30} finished in {(datetime.datetime.now() - start).microseconds / 1000:.2f} ms'
        print(duration)
        return result

    return wrapper
