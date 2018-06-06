"""This module contains the AxisGyroscope type."""


from raspy.argument_null_exception import ArgumentNullException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.illegal_argument_exception import IllegalArgumentException
from raspy.components.gyroscopes import gyro_trigger_mode
from raspy.components.gyroscopes.gyro import Gyro
from raspy.components.gyroscopes.multi_axis_gyro import MultiAxisGyro


class AxisGyroscope(Gyro):
    """A generic gyroscope device abstraction component."""

    def __init__(self, mag, deg_per_sec_factor=None):
        """Initialize a new instance of AxisGyroscope.

        :param raspy.components.gyroscopes.mutli_axis_gyro.MultiAxisGyro mag: The
        multi-axis gyro to read from.
        :param float deg_per_sec_factor: The degrees-per-second factor value.
        """
        Gyro.__init__(self)

        if mag is None:
            raise ArgumentNullException("'mag' param cannot be None.")

        if not isinstance(mag, MultiAxisGyro):
            msg = "'mag' param must be an instance of "
            msg += "raspy.components.gyroscopes.multi_axis_gyro.MultiAxisGyro."
            raise IllegalArgumentException(msg)

        self.__multiAxisGyro = mag
        self.__trigger = gyro_trigger_mode.READ_NOT_TRIGGERED
        self.__value = 0.0
        self.__offset = 0.0
        self.__angle = 0.0
        self.__degPerSecondFactor = 0
        self.__factorSet = False

        if deg_per_sec_factor:
            if isinstance(deg_per_sec_factor, float):
                self.__degPerSecondFactor = deg_per_sec_factor
                self.__factorSet = True

    def dispose(self):
        """Dispose managed resources.

        Performs application-defined tasks associated with freeing, releasing,
        or resetting resources.
        """
        if self.is_disposed:
            return

        if self.__multiAxisGyro is not None:
            self.__multiAxisGyro.dispose()
            self.__multiAxisGyro = None

        self.__trigger = None
        self.__value = None
        self.__offset = None
        self.__angle = None
        self.__degPerSecondFactor = None
        self.__factorSet = False
        Gyro.dispose(self)

    def read_and_update_angle(self):
        """Read and update the angle.

        :returns: The angular velocity of the gyro.
        :rtype: float

        :raise: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.

        :raises: raspy.io.io_exception.IOException if unable to write to the
        gyro.
        """
        if self.is_disposed:
            raise ObjectDisposedException("AxisGyroscope")

        self.__multiAxisGyro.read_gyro()
        angular_velocity = (((self.__value - self.__offset) / 40) * 40)
        if self.__factorSet:
            angular_velocity /= self.__degPerSecondFactor

        delta = self.__multiAxisGyro.time_delta
        self.__angle = (self.__angle + angular_velocity * delta / 1000)
        return angular_velocity

    @property
    def raw_value(self):
        """Get the raw value.

        :returns: The raw value.
        :rtype: float
        """
        if self.__trigger == gyro_trigger_mode.GET_RAW_VALUE_TRIGGER_READ:
            self.read_and_update_angle()
        return self.__value

    @raw_value.setter
    def raw_value(self, value):
        """Set the raw value.

        :param float value: The raw value.
        """
        if value is None:
            value = 0

        self.__value = value

    @property
    def offset(self):
        """Get the offset value.

        This is the value the gyro outputs when not rotating.

        :returns: The offset.
        :rtype: float
        """
        return self.__offset

    @offset.setter
    def offset(self, value):
        """Set the offset value.

        This is the value the gyro outputs when not rotating.

        :param float value: The offset value.
        """
        if value is None:
            value = 0.0

        self.__value = value

    @property
    def angle(self):
        """Get the angular position.

        :returns: The angle.
        :rtype: float
        :raise: raspy.io.io_exception.IOException if an error occurs while
        reading from the Gyro.
        """
        if self.__trigger == gyro_trigger_mode.GET_ANGLE_TRIGGER_READ:
            self.read_and_update_angle()
        return self.__angle

    @angle.setter
    def angle(self, value):
        """Set the angular position.

        :param float value: The angle.
        :raise: raspy.io.io_exception.IOException if an error occurs while
        reading from the Gyro.
        """
        if value is None:
            value = 0.0

        self.__angle = value

    @property
    def angular_velocity(self):
        """Get the angular velocity.

        :returns: The angular velocity.
        :rtype: float
        """
        trig = gyro_trigger_mode.GET_ANGULAR_VELOCITY_TRIGGER_READ
        if self.__trigger == trig:
            self.read_and_update_angle()

        adjusted = (self.__angle - self.__offset)
        if self.__factorSet:
            return adjusted / self.__degPerSecondFactor
        return adjusted

    def set_read_trigger(self, trig):
        """Set the read trigger.

        :param int trig: The trigger mod to re-read the gyro value.
        """
        if trig is None:
            trig = gyro_trigger_mode.READ_NOT_TRIGGERED
        self.__trigger = trig

    def recalibrate_offset(self):
        """Recalibrate the offset."""
        if self.is_disposed:
            raise ObjectDisposedException("AxisGyroscope")

        self.__multiAxisGyro.recalibrate_offset()
