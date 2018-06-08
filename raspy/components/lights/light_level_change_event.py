"""This module contains the LightLevelChangeEvent type."""


class LightLevelChangeEvent(object):
    """The event that fires when when a light level change occurs."""

    def __init__(self, level=0):
        """Initialize a new instance of LightLevelChangeEvent.

        :param int level: The brightness level.
        """
        self.__level = level

    @property
    def level(self):
        """Get the brightness level.

        :returns: The brightness level.
        :rtype: int
        """
        return self.__level
