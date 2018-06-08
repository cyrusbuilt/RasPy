"""This module contains the DimmableLight base type."""


import threading
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.lights import light


class DimmableLight(light.Light):
    """Base class for dimmable light component abstractions."""

    def __init__(self):
        """Initialize a new instance of DimmableLight."""
        light.Light.__init__(self)

    def on_light_level_changed(self, lce):
        """Fire the light level changed event.

        :param raspy.components.lights.light_level_change_event.LightLevelChangeEvent lce:
        The level change event object.
        """
        if self.is_disposed:
            raise ObjectDisposedException("DimmableLight")

        _t = threading.Thread(target=self.emit,
                              name="levelChangeThread",
                              args=(light.EVENT_LEVEL_CHANGED, lce))
        _t.daemon = True
        _t.start()

    @property
    def level(self):
        """Get the brightness level.

        :returns: The brightness level.
        :rtype: int
        """
        return 0

    @level.setter
    def level(self, lev):
        """Set the brightness level.

        :param int lev: The brightness level.
        :raises: IndexError if the specified level is less than min_level or
        greater than max_level.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        pass

    @property
    def min_level(self):
        """Get the minimum brightness level.

        :returns: The minimum brightness level.
        :rtype: int
        """
        return 0

    @property
    def max_level(self):
        """Get the maximum brightness level.

        :returns: The maximum brightness level.
        :rtype: int
        """
        return 0

    def get_level_percentage(self, lev=0):
        """Get the current brightness level percentage.

        :param int lev: The brightness level.
        :returns: The brightness percentage level.
        :rtype: int
        """
        if lev is None or lev == 0:
            lev = self.level

        minimum = min(self.min_level, self.max_level)
        maximum = max(self.min_level, self.max_level)
        rng = maximum - minimum
        return (lev * 100) / rng

    @property
    def is_on(self):
        """Get a value indicating whether or not the light is on.

        :returns: True if the light is on.
        :rtype: bool
        """
        return self.level > self.min_level

    @property
    def is_off(self):
        """Get a value indicating whether or not the light is off.

        :returns: True if the light is off.
        :rtype: bool
        """
        return not self.level <= self.min_level

    def turn_on(self):
        """Turn the light on.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        self.level = self.max_level

    def turn_off(self):
        """Turn the light off.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        self.level = self.min_level
