"""Implemented by classes that represent GPIO pins on the Raspberry Pi."""

import os.path
from raspy import exec_utils
from raspy.invalid_operation_exception import InvalidOperationException
from raspy.io import gpio
from raspy.io import gpio_pins
from raspy.io import pin_state
from raspy.io import pin_mode
from raspy.io import pin_utils
from raspy.io.io_exception import IOException
from raspy.io.pin_state_change_event import PinStateChangeEvent

IO_PATH = "/sys/class/gpio/"
"""The filesystem base path for I/O pins."""


class GpioStandard(gpio.Gpio):
    """Raspberry Pi GPIO using the file-based access method."""

    GPIO_PATH = IO_PATH
    """The path on the Raspberry Pi for the GPIO interface."""

    def __init__(self, pn, mode, initial_val):
        """Initialize a new instance of raspy.io.gpio_standard.GpioStandard.

        :param raspy.io.gpio_pins.GpioPin pn: The GPIO pin.
        :param int mode: The I/O pin mode.
        :param int initial_val: The initial pin value.
        """
        gpio.Gpio.__init__(self, pn, mode, initial_val)

        self.__lastState = pin_state.LOW
        self.__pwm = 0
        self.__pwmRange = 1024
        self.__isPWM = False

    @property
    def pwm(self):
        """Get the PWM (pulse-width modulation) value.

        :returns: The PWM value.
        :rtype: int
        """
        return self.__pwm

    @pwm.setter
    def pwm(self, val):
        """Get the PWM (pulse-width modulation) value.

        :param int val: The PWM value.
        :raises: raspy.invalid_operation_exception.InvalidOperationException
        if setting a PWM value on a pin that is not configured as PWM.
        """
        if self.mode == pin_mode.PWM:
            err_msg = "Cannot set PWM value on a pin not configured for PWM."
            raise InvalidOperationException(err_msg)

        if val < 0:
            val = 0

        if val > 1023:
            val = 1023

        if self.__pwm != val:
            self.__pwm = val
            if not self.__isPWM:
                cmd = "gpio mode " + str(self.inner_pin) + " pwm"
                exec_utils.execute_command(cmd)

            cmd = "gpio pwm " + str(self.inner_pin) + " " + str(self.__pwm)
            exec_utils.execute_command(cmd)

    @property
    def pwm_range(self):
        """Get the PWM (pulse-width modulation) range.

        :returns: The PWM range.
        :rtype: int
        """
        return self.__pwmRange

    @pwm_range.setter
    def pwm_range(self, rng):
        """Set the PWM (pulse-width modulation) range.

        :param int rng: The PWM range.
        """
        if rng < 0:
            rng = 0

        if rng > 1024:
            rng = 1024

        if self.__pwmRange != rng:
            self.__pwmRange = rng

    def __internal_export_pin(self, mode, pin_num, pin_name):
        """Export the GPIO setting the direction.

        This creates the /sys/class/gpio/gpioXX directory.

        :param int mode: The I/O pin mode.
        :param str pin_num: The pin number.
        :param str pin_name: The name of the pin.
        :raises: raspy.io.io_exception.IOException if an IOErr occurs while
        trying to write to the specified pin.
        """
        pin_path = IO_PATH + "gpio" + pin_num
        m = pin_utils.get_pin_mode_name(mode)

        # If the pin is already exported, check it's in the proper direction.
        # If the direction matches, return out of the function. If not,
        # change the direction.
        if self.mode == mode:
            return

        # export
        if os.path.exists(pin_path):
            pin_utils.write_fs_pin(IO_PATH + "export", pin_num)

        # set I/O direction
        print("Setting direction on pin " + pin_name + "/gpio" + pin_num + " as " + m)
        pin_utils.write_fs_pin(pin_path + "/direction", m)

    def __export_pin(self, pn, mode):
        """Export the GPIO setting the direction.

        This creates the /sys/class/gpio/gpioXX directory.

        :param raspy.io.gpio_pins.GpioPin pn: The pin to export.
        :param int mode: The I/O pin mode.
        :raises: raspy.io.io_exception.IOException if an IOError occurs
        while trying to write to the specified pin.
        """
        self.__internal_export_pin(mode, str(pn.value), pn.name)

    def __internal_write(self, pin_address, val, gpio_num, pin_name):
        """Write the specified value to the specified GPIO pin.

        :param int pin_address: The address of the pin to write to.
        :param int val: The value to write to the pin.
        :param str gpio_num: The GPIO number associated with the pin.
        :param str pin_name: The name of the pin.
        :raises: raspy.io.io_exception.IOException if an IOError occurs
        while trying to write to the specified pin.
        """
        # GpioNone is the same value for both Rev1 and Rev2 boards.
        if pin_address == gpio_pins.GpioNone.value:
            return

        self.__internal_export_pin(pin_mode.OUT, gpio_num, pin_name)
        pin_path = IO_PATH + "gpio" + gpio_num + "/value"
        pin_utils.write_fs_pin(pin_path, str(val))

    def __write(self, pn, val):
        """Write specified value to the specified GPIO pin.

        :param raspy.io.gpio_pins.GpioPin pn: The pin to write the value to.
        :param int val: The value to write to the pin.
        :raises: raspy.io.io_exception.IOException if an IOError occurs while
        trying to write to the specified pin.
        """
        self.__internal_write(pn.value, val, str(pn.value), pn.name)

    def __internal_unexport_pin(self, gpio_num):
        """Unexport the GPIO.

        This removes the /sys/class/gpio/gpioXX directory.

        :param str gpio_num: The GPIO number associated with the pin.
        :raises: raspy.io.io_exception.IOException if an IOError occurs
        while trying to write to the specified pin.
        """
        pin_utils.write_fs_pin(IO_PATH + "unexport", gpio_num)

    def __unexport_pin(self, pin):
        """Unexport the GPIO.

        This removes the /sys/class/gpio/gpioXX directory.

        :param raspy.io.gpio_pins.GpioPin pin: The GPIO pin to unexport.
        :raises: raspy.io.IOException if an IOError occurs while trying to
        write to the specified pin.
        """
        self.__write(pin, pin_state.LOW)
        self.__internal_unexport_pin(str(pin.value))

    def provision(self):
        """Provision this pin.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        self.__export_pin(self.inner_pin, self.mode)
        self.__write(self.inner_pin, self.__get_initial_pin_value())

    def __internal_read(self, gpio_num, gpio_name):
        """Read the value of the specified GPIO pin.

        :param str gpio_num: The GPIO pin number.
        :param str gpio_name: The name of the GPIO.
        :returns: The value of the pin.
        :rtype: int
        :raises: raspy.io.io_exception.IOException if the specified pin could
        not be read (device does not exist).
        """
        return_value = pin_state.LOW
        self.__internal_export_pin(pin_mode.IN, gpio_num, gpio_name)
        file_name = IO_PATH + "gpio" + gpio_num + "/value"
        if os.path.exists(file_name):
            read_value = pin_utils.read_fs_pin(file_name)
            if read_value == 1:
                return_value = pin_state.HIGH
        else:
            err_msg = "Cannot read from pin " + gpio_num + ". "
            err_msg += "Device does not exist"
            raise IOException(err_msg)

        return return_value

    def __read(self, pn):
        """Read a value from the specified pin.

        :param raspy.io.gpio_pins.GpioPin pn: The pin to read from.
        :returns: The value read from the pin (high or low).
        :rtype: int
        :raises: raspy.io.io_exception.IOException if the specified pin could
        not be read (device does not exist).
        """
        return self.__internal_read(str(pn.value), pn.name)

    def write(self, ps):
        """Write a value to the pin.

        :param int ps: The pin state value to write to the pin.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        gpio.Gpio.write(self, ps)
        self.__write(self.inner_pin, ps)
        if self.__lastState != self.state:
            evt = PinStateChangeEvent(self.__lastState, self.state)
            self.on_pin_state_change(evt)

    def pulse(self, millis):
        """Pulse the pin output for the specified number of milliseconds.

        :param int, long millis: The number of milliseconds to wait between
        states.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.mode == pin_mode.IN:
            err_msg = "You cannot pulse a pin set as an input"
            raise InvalidOperationException(err_msg)

        pin_addr = self.inner_pin.value
        self.__write(self.inner_pin, pin_state.HIGH)
        evt = PinStateChangeEvent(self.state, pin_state.HIGH, pin_addr)
        self.on_pin_state_change(evt)
        super(GpioStandard, self).pulse(millis)
        self.__write(self.inner_pin, pin_state.LOW)
        evt = PinStateChangeEvent(self.state, pin_state.LOW, pin_addr)
        self.on_pin_state_change(evt)

    def pulse_default(self):
        """Pulse the pin for the default value of 500ms."""
        self.pulse(500)

    def read(self):
        """Read a value from the pin.

        :returns: The state (value) of the pin.
        :rtype: int
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        val = self.__read(self.inner_pin)
        if self.__lastState != val:
            pin_addr = self.inner_pin.value
            evt = PinStateChangeEvent(self.__lastState, val, pin_addr)
            self.on_pin_state_change(evt)

        return val

    def dispose(self):
        """Dispose managed resources.

        Performs application-defined tasks associated with freeing, releasing,
        or resetting resources.
        """
        if gpio.Gpio.is_disposed:
            return

        self.__unexport_pin(self.inner_pin)
        if self.__isPWM:
            cmd = "gpio unexport " + str(self.inner_pin.value)
            exec_utils.execute_command(cmd)

        self.write(pin_state.LOW)
        gpio.Gpio.dispose(self)
