"""This module provides the base type Implemented by classes that represent DS1620 sensors."""


from raspy.disposable import Disposable


class DS1620Interface(Disposable):
    """Implemented by classes that represent DS1620 sensors."""

    def __init__(self):
        """Initialize a new instance of raspy.sensors.ds1620_interface.DS1620Interface."""
        super(Disposable, self).__init__()

    @property
    def clock_pin(self):
        """Get the clock pin.

        :returns: The clock pin.
        :rtype: raspy.io.gpio.Gpio
        """
        return None

    @property
    def data_pin(self):
        """Get the data pin.

        :returns: The data pin.
        :rtype: raspy.io.gpio.Gpio
        """
        return None

    @property
    def reset_pin(self):
        """Get the reset pin.

        :returns: The reset pin.
        :rtype: raspy.io.gpio.Gpio
        """
        return None

    def get_temperature(self):
        """Send commands to get the temperature from the sensor.

        :returns: The temperature with half-degree granularity.
        :rtype: long
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        return 0
