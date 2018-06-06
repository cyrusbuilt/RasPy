"""This module contains the I2CBus type."""


from smbus2 import SMBus, i2c_msg
from raspy import board_revision
from raspy.illegal_argument_exception import IllegalArgumentException
from raspy.invalid_operation_exception import InvalidOperationException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.io.io_exception import IOException
from raspy.io.i2c.i2c_interface import I2CInterface


class I2CBus(I2CInterface):
    """An I2C bus implementation for the Raspberry Pi.

    Derived from the SMBus2 library by 'kplindegaard' at
    https://github.com/kplindegaard/smbus2.
    """

    def __init__(self, board_rev=board_revision.REV1):
        """Initialize a new instance of I2CBus.

        :param int board_rev: The board revision.
        """
        I2CInterface.__init__(self)
        self.__busID = 1
        if board_rev == board_revision.REV1:
            self.__busID = 0

        self.__isOpen = False
        self.__bus = None

    @property
    def is_open(self):
        """Get a value indicating whether the connection is open.

        :returns: True if the connection is open.
        :rtype: bool
        """
        return self.__isOpen

    def open(self):
        """Open a connection to the I2C bus.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.

        :raises: raspy.io.io_exception.IOException if unable to open the
        bus connection.
        """
        if self.is_disposed:
            raise ObjectDisposedException("I2CBus")

        if self.__isOpen:
            return

        try:
            self.__bus = SMBus(self.__busID)
        except OSError or IOError:
            msg = "Error opening bus '" + str(self.__busID) + "'."
            raise IOException(msg)

        if self.__bus.fd is None:
            msg = "Error opening bus '" + str(self.__busID) + "'."
            raise IOException(msg)

        self.__isOpen = True

    def close(self):
        """Close the bus connection."""
        if self.is_disposed:
            return

        if self.__isOpen:
            if self.__bus is not None:
                self.__bus.close()
            self.__isOpen = False
            self.__bus = None

    def dispose(self):
        """Dispose of all the managed resources used by this instance."""
        if self.is_disposed:
            return

        self.close()
        self.__busID = None
        I2CInterface.dispose(self)

    def write_bytes(self, address, buf):
        """Write a list of bytes to the specified device address.

        Currently, RPi drivers do not allow writing more than 3 bytes at a
        time. As such, if any list of greater than 3 bytes is provided, an
        exception is thrown.

        :param int address: The address of the target device.
        :param list buf: A list of bytes to write to the bus.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.

        :raises: raspy.invalid_operation_exception.InvalidOperationException if
        a connection to the I2C bus has not yet been opened.

        :raises: raspy.illegal_argument_exception.IllegalArgumentException if
        the buffer contains more than 3 bytes or if the specified buffer
        parameter is not a list.

        :raises: raspy.io.io_exception.IOException if an error occurs while
        writing the buffer contents to the I2C bus or if only a partial
        write succeeds.
        """
        if self.is_disposed:
            raise ObjectDisposedException("I2CBus")

        if not self.__isOpen:
            raise InvalidOperationException("No open connection to write to.")

        if isinstance(buf, list):
            if len(buf) > 3:
                # TODO we only do this to keep parity with the JS and C#
                # ports. They each have their own underlying native
                # implementations. SMBus2 itself is capable of writing
                # much more than 3 bytes. We should change this as soon
                # as we can get the other ports to support more.
                msg = "Cannot write more than 3 bytes at a time."
                raise IllegalArgumentException(msg)
        else:
            msg = "The specified buf param value is not a list."
            raise IllegalArgumentException(msg)

        try:
            trans = i2c_msg.write(address, buf)
            self.__bus.i2c_rdwr(trans)
        except OSError or IOError:
            msg = "Error writing to address '" + str(address)
            msg += "': I2C transaction failed."
            raise IOException(msg)

    def write_byte(self, address, byt):
        """Write a single byte to the specified device address.

        :param int address: The address of the target device.
        :param int byt: The byte value to write.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.

        :raises: raspy.invalid_operation_exception.InvalidOperationException if
        a connection to the I2C bus has not yet been opened.

        :raises: raspy.io.io_exception.IOException if an error occurs while
        writing the buffer contents to the I2C bus or if only a partial
        write succeeds.
        """
        buf = list()
        buf[0] = byt
        self.write_bytes(address, buf)

    def write_command(self, address, command, data1=None, data2=None):
        """Write a command with data to the specified device address.

        :param int address: The address of the target device.
        :param int command: The command to send to the device.
        :param int data1: The data to send as the first parameter (optional).
        :param int data2: The data to send as the second parameter (optional).
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.

        :raises: raspy.invalid_operation_exception.InvalidOperationException if
        a connection to the I2C bus has not yet been opened.

        :raises: raspy.io.io_exception.IOException if an error occurs while
        writing the buffer contents to the I2C bus or if only a partial
        write succeeds.
        """
        buf = list()
        buf[0] = command

        if data1:
            buf[1] = data1

        if data1 and data2:
            buf[1] = data1
            buf[2] = data2

        self.write_bytes(address, buf)

    def write_command_byte(self, address, command, data):
        """Write a command with data to the specified device address.

        :param int address: The address of the target device.
        :param int command: The command to send to the device.
        :param int data: The data to send with the command.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.

        :raises: raspy.invalid_operation_exception.InvalidOperationException if
        a connection to the I2C bus has not yet been opened.

        :raises: raspy.io.io_exception.IOException if an error occurs while
        writing the buffer contents to the I2C bus or if only a partial
        write succeeds.
        """
        buf = list()
        buf[0] = command
        buf[1] = data & 0xff
        buf[2] = data >> 8
        self.write_bytes(address, buf)

    def read_bytes(self, address, count):
        """Read bytes from the device at the specified address.

        :param int address: The address of the device to read from.
        :param int count: The number of bytes to read.
        :returns: The bytes read.
        :rtype: list
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.

        :raises: raspy.invalid_operation_exception.InvalidOperationException if
        a connection to the I2C bus has not yet been opened.

        :raises: raspy.io.io_exception.IOException if an error occurs while
        writing the buffer contents to the I2C bus or if only a partial
        write succeeds.
        """
        if self.is_disposed:
            return

        if not self.__isOpen:
            raise InvalidOperationException("No open connection to read from.")

        buf = []
        msg = "Error reading from address '" + str(address)
        msg += "': I2C transaction failed."
        try:
            trans = i2c_msg.read(address, count)
            self.__bus.i2c_rdwr(trans)
            buf = list(trans)
        except OSError or IOError:
            raise IOException(msg)

        if len(buf) <= 0:
            raise IOException(msg)

        return buf

    def read(self, address):
        """Read a single byte from the device at the specified address.

        :param int address: The address of the device to read from.
        :returns: The byte read.
        :rtype: int
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.

        :raises: raspy.invalid_operation_exception.InvalidOperationException if
        a connection to the I2C bus has not yet been opened.

        :raises: raspy.io.io_exception.IOException if an error occurs while
        writing the buffer contents to the I2C bus or if only a partial
        write succeeds.
        """
        result = self.read_bytes(address, 1)
        return result[0]
