"""This module contains the LightStateChangeEvent type."""


class LightStateChangeEvent(object):
    """The event that gets raised when a light changes state."""

    def __init__(self, is_on=False):
        """Initialize a new instance of LightStateChangeEvent.

        :param bool is_on: Set True if the light is on.
        """
        self.__is_on = is_on

    @property
    def is_on(self):
        """Get a flag indicating whether or not the light is on.

        :returns: True if the light is on.
        :rtype: bool
        """
        return self.__is_on
