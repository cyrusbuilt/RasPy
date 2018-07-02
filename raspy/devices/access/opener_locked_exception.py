"""This module contains the OpenerLockedException type."""


class OpenerLockedException(Exception):
    """Opener locked exception.

    This is the exception that is thrown when an opener device attempts to
    open a door that is locked.
    """

    def __init__(self, device_name):
        """Initialize a new instance of OpenerLockedException.

        :param str device_name: The name of the device that is locked.
        """
        msg = device_name + " is locked and cannot be opened."
        Exception.__init__(self, msg)
