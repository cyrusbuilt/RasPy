"""This module provides core utilities."""


import time


def sleep(ms):
    """Sleep for the specified milliseconds.

    :param int, long ms: The time in milliseconds.
    """
    if ms <= 0:
        ms = 1

    time.sleep(ms / 1000.0)


def sleep_microseconds(micros):
    """Block the current thread for the specified milliseconds.

    :param int, long micros: The amount of time in microseconds.
    """
    if micros <= 0:
        micros = 1

    time.sleep(micros / 1000000.0)
