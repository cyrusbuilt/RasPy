"""This module contains the ADXL345 type."""


import itertools
from raspy import board_revision
from raspy.argument_null_exception import ArgumentNullException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.gyroscopes import gyro_trigger_mode
from raspy.components.gyroscopes.axis_gyroscope import AxisGyroscope
from raspy.components.gyroscopes.multi_axis_gyro import MultiAxisGyro
from raspy.io.io_exception import IOException
from raspy.io.i2c.i2c_bus import I2CBus
from raspy.pi_system import core_utils
from raspy.pi_system import system_info


CALIBRATION_READS = 50
CALIBRATION_SKIPS = 5

ADXL345_ADDR = 0x53
"""The default physical bus address of the ADXL345."""


class ADXL345(MultiAxisGyro):
    """A device abstraction component for an Analog Devices ADXL345.

    The ADXL345 is a high resolution 3-axis accelerometer.
    """

    def __init__(self, device=None, bus_addr=0):
        """Initialize a new instance of the ADXL345.

        :param raspy.io.i2c.i2c_interface.I2CInterface device: The I2C device
        that represents the physical connection to the gyro. If None, then it
        is assumed that the host is a revision 2 or higher board and a default
        :py:class:`raspy.io.i2c.i2c_bus.I2CBus` using the rev 2 I2C bus path
        will be used instead.
        :param int bus_addr: The bus address of the device.
        :raises: raspy.io.io_exception.IOException if the specified device
        instance has been disposed.
        """
        MultiAxisGyro.__init__(self)
        if device is None:
            device = I2CBus(board_revision.REV2)

        self.__device = device
        if not self.__device.is_open:
            self.__device.open()

        self.__x = AxisGyroscope(self, 20)
        self.__y = AxisGyroscope(self, 20)
        self.__z = AxisGyroscope(self, 20)

        self.__aX = AxisGyroscope(self, 20)
        self.__aY = AxisGyroscope(self, 20)
        self.__aZ = AxisGyroscope(self, 20)

        self.__address = ADXL345_ADDR
        if bus_addr and isinstance(bus_addr, int):
            self.__address = bus_addr

        self.__timeDelta = 0
        self.__lastRead = 0

    def dispose(self):
        """Dispose managed resources.

        Performs application-defined tasks associated with freeing, releasing,
        or resetting resources.
        """
        if self.is_disposed:
            return

        if self.__device is not None:
            self.__device.dispose()
            self.__device = None

        if self.__aX is not None:
            self.__aX.dispose()
            self.__aX = None

        if self.__aY is not None:
            self.__aY.dispose()
            self.__aY = None

        if self.__aZ is not None:
            self.__aZ.dispose()
            self.__aZ = None

        if self.__x is not None:
            self.__x.dispose()
            self.__x = None

        if self.__y is not None:
            self.__y.dispose()
            self.__y = None

        if self.__z is not None:
            self.__z.dispose()
            self.__z = None

        self.__address = None
        self.__timeDelta = 0
        self.__lastRead = 0
        MultiAxisGyro.dispose(self)

    @property
    def time_delta(self):
        """Get the time difference (delta) since the last loop.

        :returns: The time delta.
        :rtype: float
        """
        return self.__timeDelta

    @property
    def x(self):
        """Get a reference to the X-axis.

        :returns: The X-axis.
        :rtype: raspy.components.gyroscopes.axis_gyroscope.AxisGyroscope
        """
        return self.__x

    @property
    def y(self):
        """Get a reference to the Y-axis.

        :returns: The Y-axis.
        :rtype: raspy.components.gyroscopes.axis_gyroscope.AxisGyroscope
        """
        return self.__y

    @property
    def z(self):
        """Get a reference to the Z-axis.

        :returns: The Z-axis.
        :rtype: raspy.components.gyroscopes.axis_gyroscope.AxisGyroscope
        """
        return self.__z

    @property
    def a_x(self):
        """Get a reference to the X-axis implementation.

        :returns: The X-axis implementation.
        :rtype: raspy.components.gyroscopes.axis_gyroscope.AxisGyroscope
        """
        return self.__aX

    @property
    def a_y(self):
        """Get a reference to the Y-axis implementation.

        :returns: The Y-axis implementation.
        :rtype: raspy.components.gyroscopes.axis_gyroscope.AxisGyroscope
        """
        return self.__aY

    @property
    def a_z(self):
        """Get a reference to the Z-axis implementation.

        :returns: The Z-axis implementation.
        :rtype: raspy.components.gyroscopes.axis_gyroscope.AxisGyroscope
        """
        return self.__aZ

    def enable(self):
        """Enable the gyro.

        :raise: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.

        :raises: raspy.io.io_exception.IOException if unable to write to the
        gyro.
        """
        if self.is_disposed:
            raise ObjectDisposedException("ADXL345")

        packet = [0x31, 0x0B]
        self.__device.write_bytes(self.__address, packet)

    def disable(self):
        """Disable the gyro.

        :raise: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.

        :raises: raspy.io.io_exception.IOException if unable to write to the
        gyro.
        """
        if self.is_disposed:
            raise ObjectDisposedException("ADXL345")

        # TODO how to disable?

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
        if trig_axis is None:
            msg = "trig_axis param cannot be None. Bust be of type "
            msg += "raspy.components.gyroscopes.gyro.Gyro."
            raise ArgumentNullException(msg)

        if trig_mode is None:
            trig_mode = gyro_trigger_mode.READ_NOT_TRIGGERED

        self.enable()
        if trig_axis == self.a_x:
            self.a_x.set_read_trigger(trig_mode)
        else:
            self.a_x.set_read_trigger(gyro_trigger_mode.READ_NOT_TRIGGERED)

        if trig_axis == self.a_y:
            self.a_y.set_read_trigger(trig_mode)
        else:
            self.a_y.set_read_trigger(gyro_trigger_mode.READ_NOT_TRIGGERED)

        if trig_axis == self.a_z:
            self.a_z.set_read_trigger(trig_mode)
        else:
            self.a_z.set_read_trigger(gyro_trigger_mode.READ_NOT_TRIGGERED)

        return trig_axis

    def read_gyro(self):
        """Read the gyro and store the value internally.

        :raise: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.

        :raises: raspy.io.io_exception.IOException if unable to write to the
        gyro.
        """
        if self.is_disposed:
            raise ObjectDisposedException("ADXL345")

        now = system_info.get_current_time_millis()
        self.__timeDelta = now - self.__lastRead
        self.__lastRead = now

        self.__device.write_byte(self.__address, 0x00)
        core_utils.sleep(10)
        data = self.__device.read_bytes(self.__address, 6)
        if len(data) != 6:
            msg = "Couldn't read compass data; Return buffer size: "
            msg += str(len(data))
            raise IOException(msg)

        self.a_x.raw_value = ((data[0] & 0xff) << 8) + (data[1] & 0xff)
        self.a_y.raw_value = ((data[2] & 0xff) << 8) + (data[3] & 0xff)
        self.a_z.raw_value = ((data[3] & 0xff) << 8) + (data[5] & 0xff)

    def recalibrate_offset(self):
        """Recalibrate the offset.

        :raise: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.

        :raises: raspy.io.io_exception.IOException if unable to write to the
        gyro.
        """
        total_x = 0
        total_y = 0
        total_z = 0

        min_x = 1000
        min_y = 1000
        min_z = 1000

        max_x = -1000
        max_y = -1000
        max_z = -1000

        for _ in itertools.repeat(None, CALIBRATION_SKIPS):
            self.read_gyro()
            core_utils.sleep_microseconds(1000)

        for _ in itertools.repeat(None, CALIBRATION_READS):
            self.read_gyro()

            x = self.a_x.raw_value
            y = self.a_y.raw_value
            z = self.a_z.raw_value

            total_x += x
            total_y += y
            total_z += z

            if x < min_x:
                min_x = x

            if y < min_y:
                min_y = y

            if z < min_z:
                min_z = z

            if x > max_x:
                max_x = x

            if y > max_y:
                max_y = y

            if z > max_z:
                max_z = z

        self.a_x.offset = total_x / CALIBRATION_READS
        self.a_y.offset = total_y / CALIBRATION_READS
        self.a_z.offset = total_z / CALIBRATION_READS
