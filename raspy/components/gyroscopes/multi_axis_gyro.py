"""This component contains the Multi-Axis Gyro base type."""


from raspy.components.component import Component


class MultiAxisGyro(Component):
    """A multi-axis gyroscopes device abstraction component interface."""

    def __init__(self):
        """Initialize a new instance of MultiAxisGyro."""
        Component.__init__(self)

    @property
    def time_delta(self):
        """Get the time difference (delta) since the last loop.

        :returns: The time delta.
        :rtype: float
        """
        return 0.0

    def init(self, trig_axis, trig_mode):
        """Initialize the gyro.

        :param raspy.components.gyroscopes.gyro.Gyro trig_axis: The gyro that
        represents the single axis responsible for the triggering of updates.

        :param int trig_mode: The gyro update trigger mode.

        :returns: A reference to the specified triggering axis, which may or
        may not have been modified.

        :raise: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.

        :raises: raspy.io.io_exception.IOException if unable to write to the
        gyro.
        """
        return None

    def enable(self):
        """Enable the gyro.

        :raise: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.

        :raises: raspy.io.io_exception.IOException if unable to write to the
        gyro.
        """
        raise NotImplementedError("method enable() not implemented.")

    def disable(self):
        """Disable the gyro.

        :raise: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.

        :raises: raspy.io.io_exception.IOException if unable to write to the
        gyro.
        """
        raise NotImplementedError("method disable() not implemented.")

    def read_gyro(self):
        """Read the gyro and store the value internally.

        :raise: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.

        :raises: raspy.io.io_exception.IOException if unable to write to the
        gyro.
        """
        raise NotImplementedError("method read_gyro() not implemented.")

    def recalibrate_offset(self):
        """Recalibrate the offset.

        :raise: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.

        :raises: raspy.io.io_exception.IOException if unable to write to the
        gyro.
        """
        raise NotImplementedError("method recalibrate_offset() not implemented.")
