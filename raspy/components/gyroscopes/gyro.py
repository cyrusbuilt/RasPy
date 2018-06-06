"""This module contains the Gyro base type."""


from raspy.components.component import Component


class Gyro(Component):
    """A single-axis gyroscopes device abstraction component interface."""

    def __init__(self):
        """Initialize a new instance of Gyro."""
        Component.__init__(self)

    @property
    def angular_velocity(self):
        """Get the angular velocity.

        :returns: The angular velocity.
        :rtype: float
        """
        return 0.0

    @property
    def raw_value(self):
        """Get the raw value.

        :returns: The raw value.
        :rtype: float
        """
        return 0.0

    @raw_value.setter
    def raw_value(self, value):
        """Set the raw value.

        :param float value: The raw value.
        """
        pass

    @property
    def offset(self):
        """Get the offset value.

        This is the value the gyro outputs when not rotating.

        :returns: The offset.
        :rtype: float
        """
        return 0.0

    @offset.setter
    def offset(self, value):
        """Set the offset value.

        This is the value the gyro outputs when not rotating.

        :param float value: The offset value.
        """
        pass

    @property
    def angle(self):
        """Get the angular position.

        :returns: The angle.
        :rtype: float
        :raise: raspy.io.io_exception.IOException if an error occurs while
        reading from the Gyro.
        """
        return 0.0

    @angle.setter
    def angle(self, value):
        """Set the angular position.

        :param float value: The angle.
        :raise: raspy.io.io_exception.IOException if an error occurs while
        reading from the Gyro.
        """
        pass

    def recalibrate_offset(self):
        """Recalibrate the offset."""
        raise NotImplementedError("base method recalibrate_offset not implemented.")

    def set_read_trigger(self, trig):
        """Set the read trigger.

        :param int trig: The trigger mod to re-read the gyro value.
        """
        raise NotImplementedError("base method set_read_trigger not implemented.")
