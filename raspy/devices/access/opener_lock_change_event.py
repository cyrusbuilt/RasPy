"""This module contains the OpenerLockChangeEvent type."""


class OpenerLockChangeEvent(object):
    """The event that fires when an opener lock changes state."""

    def __init__(self, locked=False):
        """Initialize a new instance of OpenerLockChangeEvent.

        :param bool locked: Set True if the opener is locked.
        """
        self.__locked = locked

    @property
    def is_locked(self):
        """Get a flag indicating whether or not the opener is locked.

        :returns: True if locked; Otherwise, False.
        :rtype: bool
        """
        return self.__locked
