"""Implemented by classes that represent GPIO pins on the Raspberry Pi.

GpioStandard.py

Author:
      Chris Brunner <cyrusbuilt at gmail dot com>

  Copyright (c) 2017 CyrusBuilt

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
"""

import os.path
from RasPy import ExecUtils
from RasPy.InvalidOperationException import InvalidOperationException
from RasPy.IO import Gpio
from RasPy.IO import GpioPins
from RasPy.IO import PinState
from RasPy.IO import PinMode
from RasPy.IO import PinUtils
from RasPy.IO.IOException import IOException
from RasPy.IO.PinStateChangeEvent import PinStateChangeEvent

IO_PATH = "/sys/class/gpio/"
"""The filesystem base path for I/O pins."""


class GpioStandard(Gpio.Gpio):
    """Raspberry Pi GPIO using the file-based access method."""

    GPIO_PATH = IO_PATH
    """The path on the Raspberry Pi for the GPIO interface."""

    def __init__(self, pn, mode, initialVal):
        """Initialize a new instance of RasPy.IO.GpioStandard.

        :param pn: The GPIO pin.
        :param mode: The I/O pin mode.
        :param value: The initial pin value.
        :type pn: RasPy.IO.GpioPins
        :type mode: int
        :type value: int
        """
        super(GpioStandard, self).__init__(pn, mode, initialVal)

        self.__lastState = PinState.LOW
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

        :param val: The PWM value.
        :type val: int
        :raises: RasPy.InvalidOperationException if setting a PWM value on a
        pin that is not configured as PWM.
        """
        if self.mode == PinMode.PWM:
            errMsg = "Cannot set PWM value on a pin not configured for PWM."
            raise InvalidOperationException(errMsg)

        if val < 0:
            val = 0

        if val > 1023:
            val = 1023

        if self.__pwm != val:
            self.__pwm = val
            cmd = ""
            if not self.__isPWM:
                cmd = "gpio mode " + str(self.inner_pin) + " pwm"
                ExecUtils.execute_command(cmd)

            cmd = "gpio pwm " + str(self.inner_pin) + " " + str(self.__pwm)
            ExecUtils.execute_command(cmd)

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

        :param range: The PWM range.
        :type range: int
        """
        if rng < 0:
            rng = 0

        if rng > 1024:
            rng = 1024

        if self.__pwmRange != rng:
            self.__pwmRange = rng

    def __internal_export_pin(self, mode, pinnum, pinname):
        """Export the GPIO setting the direction.

        This creates the /sys/class/gpio/gpioXX directory.

        :param mode: The I/O pin mode.
        :param pinnum: The pin number.
        :param pinname: The name of the pin.
        :type mode: int
        :type pinnum: string
        :type pinname: string
        :raises: RasPy.IO.IOException if an IOErr occurs while trying to write
        to the specified pin.
        """
        pinPath = IO_PATH + "gpio" + pinnum
        m = PinUtils.get_pin_mode_name(mode)

        # If the pin is already exported, check it's in the proper direction.
        # If the direction matches, return out of the function. If not,
        # change the direction.
        if self.inner_pin.mode == mode:
            return

        # export
        if os.path.exists(pinPath):
            PinUtils.write_fs_pin(IO_PATH + "export", pinnum)

        # set I/O direction
        PinUtils.write_fs_pin(pinPath + "/direction", m)

    def __export_pin(self, pn, mode):
        """Export the GPIO setting the direction.

        This creates the /sys/class/gpio/gpioXX directory.

        :param pn: The pin to export.
        :param mode: The I/O pin mode.
        :type pn: RasPy.IO.GpioPins
        :type mode: int
        :raises: RasPy.IO.IOException if an IOError occurs while trying to
        write to the specified pin.
        """
        self.__internal_export_pin(pn.value, mode, str(pn.value), pn.name)

    def __internal_write(self, pinAddress, val, gpioNum, pinName):
        """Write the specified value to the specified GPIO pin.

        :param pinAddress: The address of the pin to write to.
        :param val: The value to write to the pin.
        :param gpioNum: The GPIO number associated with the pin.
        :param pinName: The name of the pin.
        :type pinAddress: int
        :type val: int
        :type gpioNum: string
        :type pinName: string
        :raises: RasPy.IO.IOException if an IOError occurs while trying to
        write to the specified pin.
        """
        # GPIO_NONE is the same value for both Rev1 and Rev2 boards.
        if pinAddress == GpioPins.GPIO_NONE.value:
            return

        self.__internal_export_pin(pinAddress, PinMode.OUT, gpioNum, pinName)
        pinPath = IO_PATH + "gpio" + gpioNum + "/value"
        PinUtils.write_fs_pin(pinPath, str(val))

    def __write(self, pn, val):
        """Write specified value to the specified GPIO pin.

        :param pn: The pin to write the value to.
        :param val: The value to write to the pin.
        :type pn: RasPy.IO.GpioPins
        :type val: int
        :raises: RasPy.IO.IOException if an IOError occurs while trying to
        write to the specified pin.
        """
        self.__internal_write(pn, val, str(pn.value), pn.name)

    def __internal_unexport_pin(self, gpioNum):
        """Unexport the GPIO.

        This removes the /sys/class/gpio/gpioXX directory.

        :param gpioNum: The GPIO number associated with the pin.
        :type gpioNum: string
        :raises: RasPy.IO.IOException if an IOError occurs while trying to
        write to the specified pin.
        """
        PinUtils.write_fs_pin(IO_PATH + "unexport", gpioNum)

    def __unexport_pin(self, pin):
        """Unexport the GPIO.

        This removes the /sys/class/gpio/gpioXX directory.

        :param pin: The GPIO pin to unexport.
        :type pin: RasPy.IO.GpioPins
        :raises: RasPy.IO.IOException if an IOError occurs while trying to
        write to the specified pin.
        """
        self.__write(pin, PinState.LOW)
        self.__internal_unexport_pin(str(pin.value))

    def provision(self):
        """Provision this pin.

        :raises: RasPy.ObjectDisposedException if this instance has been
        disposed.
        """
        self.__export_pin(self.inner_pin, self.mode)
        self.__write(self.inner_pin, self.__get_initial_pin_value)

    def __internal_read(self, pinAddress, gpioNum, gpioName):
        """Read the value of the specified GPIO pin.

        :param pinAddress: The pin address associated with the GPIO pin.
        :param gpioNum: The GPIO pin number.
        :param gpioName: The name of the GPIO.
        :type pinAddress: int
        :type gpioNum: string
        :type gpioName: string
        :returns: The value of the pin.
        :rtype: int
        :raises: RasPy.IO.IOException if the specified pin could not be read
        (device does not exist).
        """
        returnValue = PinState.LOW
        self.__internal_unexport_pin(pinAddress, PinMode.IN, gpioNum, gpioName)
        fileName = IO_PATH + "gpio" + gpioNum + "/value"
        if os.path.exists(fileName):
            readValue = PinUtils.read_fs_pin(fileName)
            if readValue == 1:
                returnValue = PinState.HIGH
        else:
            errMsg = "Cannot read from pin " + gpioNum + ". "
            errMsg += "Device does not exist"
            raise IOException(errMsg)

        return returnValue

    def __read(self, pn):
        """Read a value from the specified pin.

        :param pn: The pin to read from.
        :type pn: RasPy.IO.GpioPins
        :returns: The value read from the pin (high or low).
        :rtype: int
        :raises: RasPy.IO.IOException if the specified pin could not be read
        (device does not exist).
        """
        return self.__internal_read(pn.value, str(pn.value), pn.name)

    def write(self, ps):
        """Write a value to the pin.

        :param ps: The pin state value to write to the pin.
        :type ps: int
        :raises: RasPy.ObjectDisposedException if this instance has been
        disposed.
        """
        super(GpioStandard, self).write(ps)
        self.__write(self.inner_pin, ps)
        if self.__lastState != self.state:
            evt = PinStateChangeEvent(self.__lastState, self.state)
            self.on_pin_state_change(evt)

    def pulse(self, millis):
        """Pulse the pin output for the specified number of milliseconds.

        :param millis: The number of milliseconds to wait between states.
        :type millis: int, long
        :raises: RasPy.ObjectDisposedException if this instance has been
        disposed.
        """
        if self.mode == PinMode.IN:
            errMsg = "You cannot pulse a pin set as an input"
            raise InvalidOperationException(errMsg)

        self.__write(self.inner_pin, PinState.HIGH)
        evt = PinStateChangeEvent(self.state, PinState.HIGH)
        self.on_pin_state_change(evt)
        super(GpioStandard, self).pulse(millis)
        self.__write(self.inner_pin, PinState.LOW)
        evt = PinStateChangeEvent(self.state, PinState.LOW)
        self.on_pin_state_change(evt)

    def pulse_default(self):
        """Pulse the pin for the default value of 500ms."""
        self.pulse(500)

    def read(self):
        """Read a value from the pin.

        :returns: The state (value) of the pin.
        :rtype: int
        :raises: RasPy.ObjectDisposedException if this instance has been
        disposed.
        """
        val = self.__read(self.inner_pin)
        if self.__lastState != val:
            evt = PinStateChangeEvent(self.__lastState, val)
            self.on_pin_state_change(evt)

        return val

    def dispose(self):
        """Dispose managed resources.

        Performs application-defined tasks associated with freeing, releasing,
        or resetting resources.
        """
        self.__unexport_pin(self.inner_pin)
        if self.__isPWM:
            cmd = "gpio unexport " + str(self.inner_pin.value)
            ExecUtils.execute_command(cmd)

        self.write(PinState.LOW)
        super(GpioStandard, self).dispose()
