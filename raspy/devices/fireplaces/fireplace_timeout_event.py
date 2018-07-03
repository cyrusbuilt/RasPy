"""This module contains the FireplaceTimeoutEvent type."""


class FireplaceTimeoutEvent(object):
    """The event that gets fired when a fireplace timeout occurs."""

    def __init__(self, handled=False):
        """Initialize a new instance of FireplaceTimeoutEvent.

        :param bool handled: Set True if handled.
        """
        self.__handled = handled

    @property
    def is_handled(self):
        """Get a flag indicating whether this event was handled.

        :returns: True if handled; Otherwise, False.
        :rtype: bool
        """
        return self.__handled
