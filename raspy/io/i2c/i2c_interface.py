"""This module contains the I2C bus base type."""


from raspy.disposable import Disposable


class I2CInterface(Disposable):
    """Implemented by classes that represent an I2C bus."""

    def __init__(self):
        """Initialize a new instance of I2CInterface."""
        Disposable.__init__(self)

    @property
    def is_open(self):
        """Get a value indicating whether the connection is open.

        :returns: True if the connection is open.
        :rtype: bool
        """
        return False

    def open(self):
        """Open a connection to the I2C bus.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.

        :raises: raspy.io.io_exception.IOException if unable to open the
        bus connection.
        """
        pass

    def close(self):
        """Close the bus connection."""
        pass

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
        pass

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
        pass

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
        pass

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
        pass

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
        raise NotImplementedError("Method read_bytes(address, count) not implemented.")

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
        raise NotImplementedError("Method read(address) not implemented.")
