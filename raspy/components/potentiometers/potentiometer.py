"""This module contains the Potentiometer base type."""


from raspy.components.component import Component


class Potentiometer(Component):
    """A digital potentiometer device abstraction component base type."""

    def __init__(self):
        """Initialize a new instance of Potentiometer."""
        Component.__init__(self)

    @property
    def max_value(self):
        """Get the maximum wiper-value supported by the device.

        :returns: The max wiper value.
        :rtype: int
        """
        return 0

    @property
    def is_rheostat(self):
        """Get whether the device is a potentiometer or rheostat.

        :returns: True if this instance is a rheostat.
        :rtype: bool
        """
        return False

    @property
    def current_value(self):
        """Get the wiper's current value.

        :returns: The current value. Values from 0 to max_value are valid.
        Values above or below these boundaries should be corrected quietly.
        :rtype: int
        """
        return 0

    @current_value.setter
    def current_value(self, value):
        """Set the wiper's current value.

        :param int value: The wiper value to set.
        """
        pass

    def increase(self, steps=0):
        """Increase the wiper's value bye the specified number of steps.

        It is not an error if the wiper hits or already hit the upper
        boundary. In such situations, the wiper sticks to the upper boundary
        or doesn't change.
        :param int steps: How many steps to increase. If not specified or
        zero, then defaults to 1. If the current value is equal to the max
        value, then nothing happens. If steps is less than zero, then an
        exception is thrown.
        :raises: raspy.io.io_exception.IOException if communication with the
        device failed.
        """
        raise NotImplementedError("Method increase(steps) not implemented.")

    def decrease(self, steps=0):
        """Decrease the wiper's value by the specified number of steps.

        It is not an error if the wiper hits or already hit the lower
        boundary (0). In such situations, the wiper sticks to the lower
        boundary or doesn't change.

        :param int steps: The number of steps to decrease by. If not
        specified or zero, then defaults to 1.
        :raises: raspy.io.io_exception.IOException if communication with the
        device failed.
        """
        raise NotImplementedError("Method decrease(steps) not implemented.")
