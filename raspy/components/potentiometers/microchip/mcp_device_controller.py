"""This module contains the MCPDeviceController type."""


from raspy.argument_null_exception import ArgumentNullException
from raspy.disposable import Disposable
from raspy.illegal_argument_exception import IllegalArgumentException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.potentiometers.microchip import device_control_channel
from raspy.components.potentiometers.microchip import mcp_command
from raspy.components.potentiometers.microchip import status_bit
from raspy.components.potentiometers.microchip.device_controller_status \
    import DeviceControllerStatus
from raspy.components.potentiometers.microchip.device_controller_term_config \
    import DeviceControllerTermConfig
from raspy.io.io_exception import IOException
from raspy.io.i2c.i2c_interface import I2CInterface


VOLATILE_WIPER = True
NON_VOLATILE_WIPER = False

MEMADDR_STATUS = 0x05
MEMADDR_WRITE_PROTECTION = 0x0F


class MCPDeviceController(Disposable):
    """An MCP45XX and MCP46XX device controller component."""

    def __init__(self, device, bus_address=-1):
        """Initialize a new instance of MCPDeviceController.

        :param raspy.io.i2c.i2c_interface.I2CInterface device: The I2C bus
        device this instance is connected to.
        :param int bus_address: The bus address of the device.
        :raises: raspy.argument_null_exception.ArgumentNullException if param
        'device' is None.
        :raises: raspy.illegal_argument_exception.IllegalArgumentException if
        param 'device' is not of type I2CInterface.
        """
        Disposable.__init__(self)
        if device is None:
            raise ArgumentNullException("Param 'device' cannot be None.")

        if not isinstance(device, I2CInterface):
            msg = "Param 'device' must be of I2CInterface."
            raise IllegalArgumentException(msg)

        self.__busAddress = bus_address
        self.__device = device
        if not self.__device.is_open:
            self.__device.open()

    def _read(self, mem_addr):
        """Read 2 bytes from the device at the given memory address.

        :param int mem_addr: The memory address to read from.
        :returns: The 2 bytes read.
        :rtype: int
        :raises: raspy.io.io_exception.IOException if communication failed
        - or - device returned a malformed result.
        """
        # Command to ask device for reading data.
        cmd = (mem_addr << 4) | mcp_command.READ
        self.__device.write_byte(self.__busAddress, cmd)

        # Read 2 bytes.
        buf = self.__device.read_bytes(self.__busAddress, 2)
        if len(buf) != 2:
            msg = "Malformed response. Expected to read 2 bytes but got: "
            msg += str(len(buf))
            raise IOException(msg)

        # Transform signed byte to unsigned byte stored as int.
        first = buf[0] & 0xFF
        second = buf[1] & 0xFF

        # Interpret both bytes as one integer.
        return (first << 8) | second

    @property
    def device_status(self):
        """Get the device status.

        :returns: The device status.
        :rtype: DeviceControllerStatus
        :raises: raspy.io.io_exception.IOException if status bits 4 to 8 are
        not set to 1.
        """
        # Get status from device.
        stat = self._read(MEMADDR_STATUS)

        # Check formal criteria.
        reserved = stat & status_bit.RESERVED_MASK
        if reserved != status_bit.RESERVED_VALUE:
            msg = "Status bits 4 to 8 must be 1 according to documentation "
            msg += "chapter 4.2.2.1. Got: " + str(reserved)
            raise IOException(msg)

        # Build the result.
        eeprom_write_active = (stat & status_bit.EEPROM_WRITE_ACTIVE) > 0
        eeprom_write_prot = (stat & status_bit.EEPROM_WRITE_PROTECTION) > 0
        wiper_lock0 = (stat & status_bit.WIPER_LOCK0) > 0
        wiper_lock1 = (stat & status_bit.WIPER_LOCK1) > 0
        return DeviceControllerStatus(eeprom_write_active, eeprom_write_prot,
                                      wiper_lock0, wiper_lock1)

    def dispose(self):
        """Release all resources used by this component."""
        if self.is_disposed:
            return

        if self.__device is not None:
            self.__device.dispose()
            self.__device = None

        Disposable.dispose(self)

    def _write(self, mem_addr, val):
        """Write 9 bytes of the given value to the device.

        :param int mem_addr: The memory address to write to.
        :param int val: The value to be written.
        :raises: raspy.io.io_exception.IOException if an an I/O error
        occurred. The specified address is inaccessible or the I2C transaction
        failed.
        """
        # Bit 8 of value.
        first_bit = (val >> 0) & 0x000001

        # Command to ask device for setting a value.
        cmd = (mem_addr << 4) | mcp_command.WRITE | first_bit

        # Now the 7 bits of actual value.
        data = val & 0x00FF

        # Write the sequence of command and data.
        pkt = [cmd, data]
        self.__device.write_bytes(self.__busAddress, pkt)

    def _increase_or_decrease(self, mem_addr, increase=False, steps=0):
        """Write 'n' (steps) bytes to the device and increment/decrement value.

        :param int mem_addr: The memory address to write to.
        :param bool increase: Set True to increment the wiper, or False to
        decrement.
        :param int steps: The number of steps the wiper has be incremented
        or decremented.
        :raises: raspy.io.io_exception.IOException if an I/O error occurred.
        The specified address is inaccessible or the I2C transaction failed.
        """
        # 0 steps means 'do nothing'.
        if steps == 0:
            return

        # Negative steps means decrease on 'increase' or increase on
        # 'decrease'.
        actual_steps = steps
        actual_increase = increase
        if steps < 0:
            actual_increase = not increase
            actual_steps = abs(steps)

        # Ask device for increase or decrease
        inc = mcp_command.DECREASE
        if actual_increase:
            inc = mcp_command.INCREASE

        cmd = (mem_addr << 4) | inc

        # Build sequence of commands (one for each step).
        seq = list()
        for i in range(0, actual_steps):
            seq[i] = cmd

        # Write sequence to device.
        self.__device.write_bytes(self.__busAddress, seq)

    def _set_bit(self, mem, mask, val=False):
        """Set or clear a bit in the specified memory (integer).

        :param int mem: The memory to modify.
        :param int mask: The mask which defineds. the bit to set/cleared.
        :param bool val: Whether ro set the bit (True) or clear the bit
        (False).
        :returns: The modfied memory.
        :rtype: int
        """
        if val:
            result = mem | mask   # Set bit using OR.
        else:
            result = mem & ~mask  # Clear bit by using AND with inverted mask

        return result

    def set_write_protection(self, enabled=False):
        """Enable or disable the device's write-protection.

        :param bool enabled: Set True to enable or False to disable.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        :raises: raspy.io.io_exception.IOException if an I/O error occurred.
        The specified address is inaccessible or the I2C transaction failed.
        """
        if self.is_disposed:
            return ObjectDisposedException("MCPDeviceController")

        flag = False
        if enabled is not None:
            flag = enabled
        self._increase_or_decrease(MEMADDR_WRITE_PROTECTION, flag, 1)

    def set_wiper_lock(self, channel=None, locked=False):
        """Enable or disable the wiper's lock.

        :param device_control_channel.DeviceControlChannel channel: The
        channel of the wiper to set the lock for.
        :param bool locked: Set True to enable the lock or False to disable.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        :raises: raspy.argument_null_exception.ArgumentNullException if
        channel is None.
        """
        if self.is_disposed:
            raise ObjectDisposedException("MCPDeviceController")

        if channel is None:
            raise ArgumentNullException("channel param cannot be None.")

        # Increasing or decreasing on non-volatile wipers enables or
        # disables the wiper lock.
        mem_addr = channel.non_volatile_mem_address
        flag = False
        if locked is not None:
            flag = locked
        self._increase_or_decrease(mem_addr, flag, 1)

    def set_terminal_config(self, config=None):
        """Set the device's terminal configuration.

        :param DeviceControllerTermConfig config: The configuration to set.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        :raises: raspy.argument_null_exception.ArgumentNullException if the
        'config' param is None.
        :raises: raspy.io.io_exception.IOException if an I/O error occurred.
        The specified address is inaccessible or the I2C transaction failed.
        """
        if self.is_disposed:
            return ObjectDisposedException("MCPDeviceController")

        if config is None:
            raise ArgumentNullException("'config' param cannot be None.")

        if not isinstance(config, DeviceControllerTermConfig):
            msg = "'config' param must be of type DeviceControllerTermConfig."
            raise IllegalArgumentException(msg)

        chan = config.channel
        if chan is None:
            msg = "A configuration with a null channel is not permitted."
            raise ArgumentNullException(msg)

        # Read current config.
        mem_addr = config.channel.term_control_address
        tcon = self._read(mem_addr)

        # Modify config.
        ctrl_bit = chan.hardware_config_ctrl_bit
        tcon = self._set_bit(tcon, ctrl_bit, config.channel_enabled)

        ctrl_bit = chan.term_a_connection_ctrl_bit
        tcon = self._set_bit(tcon, ctrl_bit, config.pin_a_enabled)

        ctrl_bit = chan.wiper_connection_ctrl_bit
        tcon = self._set_bit(tcon, ctrl_bit, config.pin_w_enabled)

        ctrl_bit = chan.term_b_connection_ctrl_bit
        tcon = self._set_bit(tcon, ctrl_bit, config.pin_b_enabled)

        # Write new config to device.
        self._write(mem_addr, tcon)

    def get_terminal_config(self, channel=None):
        """Get the terminal configuration for the specified channel.

        :param DeviceControlChannel channel: The channel to get the terminal
        configuration for.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        :raises: raspy.argument_null_exception.ArgumentNullException if the
        'channel' param is None.
        :raises: raspy.io.io_exception.IOException if an I/O error occurred.
        The specified address is inaccessible or the I2C transaction failed.
        """
        if self.is_disposed:
            return ObjectDisposedException("MCPDeviceController")

        if channel is None:
            raise ArgumentNullException("'channel' param cannot be None.")

        if not isinstance(channel, device_control_channel.DeviceControlChannel):
            msg = "'channel' param must be of type DeviceControlChannel."
            raise IllegalArgumentException(msg)

        # Read the current config.
        tcon = self._read(channel.term_control_address)

        # Build result
        chan_enabled = (tcon & channel.hardware_config_ctrl_bit) > 0
        pin_a_enabled = (tcon & channel.term_a_connection_ctrl_bit) > 0
        pin_w_enabled = (tcon & channel.wiper_connection_ctrl_bit) > 0
        pin_b_enabled = (tcon & channel.term_b_connection_ctrl_bit) > 0
        return DeviceControllerTermConfig(channel, chan_enabled,
                                          pin_a_enabled, pin_w_enabled,
                                          pin_b_enabled)

    def set_value(self, channel=None, value=0, non_vol=False):
        """Set the wiper's value in the device.

        :param DeviceControlChannel channel: The device channel the wiper
        is on.
        :param int value: The wiper's value.
        :param bool non_vol: Set True to write to non-volatile memory, or
        False to write to volatile memory.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        :raises: raspy.argument_null_exception.ArgumentNullException if the
        'channel' param is None.
        :raises: raspy.illegal_argument_exception.IllegalArgumentException if
        param 'channel' is not of type DeviceControlChannel - or - if 'value'
        param is a negative number.
        :raises: raspy.io.io_exception.IOException if an I/O error occurred.
        The specified address is inaccessible or the I2C transaction failed.
        """
        if self.is_disposed:
            return ObjectDisposedException("MCPDeviceController")

        if channel is None:
            raise ArgumentNullException("'channel' param cannot be None.")

        if not isinstance(channel, device_control_channel.DeviceControlChannel):
            msg = "'channel' param must be of type DeviceControlChannel."
            raise IllegalArgumentException(msg)

        if value < 0:
            msg = "Only positive integer values are permitted. Got value: '"
            msg += str(value) + "' for writing to channel '"
            msg += channel.name
            raise IllegalArgumentException(msg)

        # Choose proper mem address.
        if non_vol is None:
            non_vol = False

        mem_addr = channel.volatile_mem_address
        if non_vol:
            mem_addr = channel.non_volatile_mem_address

        # Write value to device.
        self._write(mem_addr, value)

    def get_value(self, channel=None, non_vol=False):
        """Receive the current wiper's value from the device.

        :param DeviceControlChannel channel: The device channel the wiper
        is on.
        :param bool non_vol: Set True to read from non-volatile memory, or
        False to read from volatile memory.
        :returns: The wiper's value.
        :rtype: int
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        :raises: raspy.argument_null_exception.ArgumentNullException if the
        'channel' param is None.
        :raises: raspy.illegal_argument_exception.IllegalArgumentException if
        param 'channel' is not of type DeviceControlChannel.
        :raises: raspy.io.io_exception.IOException if an I/O error occurred.
        The specified address is inaccessible or the I2C transaction failed.
        """
        if self.is_disposed:
            return ObjectDisposedException("MCPDeviceController")

        if channel is None:
            raise ArgumentNullException("'channel' param cannot be None.")

        if not isinstance(channel, device_control_channel.DeviceControlChannel):
            msg = "'channel' param must be of type DeviceControlChannel."
            raise IllegalArgumentException(msg)

        # Choose proper mem address.
        if non_vol is None:
            non_vol = False

        mem_addr = channel.volatile_mem_address
        if non_vol:
            mem_addr = channel.non_volatile_mem_address
        return self._read(mem_addr)

    def decrease(self, channel=None, steps=0):
        """Decrement the volatile wiper for the given number of steps.

        :param DeviceControlChannel channel: The device channel the wiper
        is on.
        :param int steps: The number of steps.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        :raises: raspy.argument_null_exception.ArgumentNullException if the
        'channel' param is None.
        :raises: raspy.illegal_argument_exception.IllegalArgumentException if
        param 'channel' is not of type DeviceControlChannel.
        :raises: raspy.io.io_exception.IOException if an I/O error occurred.
        The specified address is inaccessible or the I2C transaction failed.
        """
        if self.is_disposed:
            return ObjectDisposedException("MCPDeviceController")

        if channel is None:
            raise ArgumentNullException("'channel' param cannot be None.")

        if not isinstance(channel, device_control_channel.DeviceControlChannel):
            msg = "'channel' param must be of type DeviceControlChannel."
            raise IllegalArgumentException(msg)

        # Decrease only works on volatile-wiper.
        if steps is None:
            steps = 0

        mem_addr = channel.volatile_mem_address
        self._increase_or_decrease(mem_addr, False, steps)

    def increase(self, channel=None, steps=0):
        """Increment the volatile wiper for the given number of steps.

        :param DeviceControlChannel channel: The device channel the wiper
        is on.
        :param int steps: The number of steps.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        :raises: raspy.argument_null_exception.ArgumentNullException if the
        'channel' param is None.
        :raises: raspy.illegal_argument_exception.IllegalArgumentException if
        param 'channel' is not of type DeviceControlChannel.
        :raises: raspy.io.io_exception.IOException if an I/O error occurred.
        The specified address is inaccessible or the I2C transaction failed.
        """
        if self.is_disposed:
            return ObjectDisposedException("MCPDeviceController")

        if channel is None:
            raise ArgumentNullException("'channel' param cannot be None.")

        if not isinstance(channel, device_control_channel.DeviceControlChannel):
            msg = "'channel' param must be of type DeviceControlChannel."
            raise IllegalArgumentException(msg)

        # Increase only works on volatile-wiper.
        if steps is None:
            steps = 0

        mem_addr = channel.volatile_mem_address
        self._increase_or_decrease(mem_addr, True, steps)
