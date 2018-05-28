"""Implemented by classes that represent GPIO pins on the PiFace.

The PiFace is an expansion board for the Raspberry Pi.

PiFaceGPIO.py

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

from RasPy import StringUtils
from RasPy.ArgumentNullException import ArgumentNullException
from RasPy.IllegalArgumentException import IllegalArgumentException
from RasPy.IO import Gpio
from RasPy.IO import PiFacePins
from RasPy.IO import PinMode


class PiFaceGPIO(Gpio.Gpio):
    """Implemented by classes that represent GPIO pins on the PiFace.

    The PiFace is an expansion board for the Raspberry Pi.
    """

    EVENT_STATE_CHANGED = "piFaceGpioStateChanged"
    """The name of the state changed event."""

    OUTPUTS = [
        PiFacePins.OUTPUT00,
        PiFacePins.OUTPUT01,
        PiFacePins.OUTPUT02,
        PiFacePins.OUTPUT03,
        PiFacePins.OUTPUT04,
        PiFacePins.OUTPUT05,
        PiFacePins.OUTPUT06,
        PiFacePins.OUTPUT07
    ]
    """An array of all the PiFace outputs."""

    INPUTS = [
        PiFacePins.INPUT00,
        PiFacePins.INPUT01,
        PiFacePins.INPUT02,
        PiFacePins.INPUT03,
        PiFacePins.INPUT04,
        PiFacePins.INPUT05,
        PiFacePins.INPUT06,
        PiFacePins.INPUT07
    ]
    """An array of all PiFace inputs."""

    __pwm = 0
    __pwmRange = 0

    def __init__self(self, pn, initialVal, name):
        """Initialize a new instance of the RasPy.IO.PiFaceGPIO class."""
        super(PiFaceGPIO, self).__init__(pn, PinMode.IN, initialVal)

        if pn is None:
            raise ArgumentNullException("pn param cannot be None.")

        if not isinstance(pn, object):
            errMsg = "pn param must be a PiFacePins memmber."
            raise IllegalArgumentException(errMsg)

        self.pin_name = name
        if StringUtils.is_null_or_empty(self.pin_name):
            self.pin_name = pn.name

        if (pn == PiFacePins.INPUT00 or pn == PiFacePins.INPUT01 or
                pn == PiFacePins.INPUT02 or pn == PiFacePins.INPUT03 or
                pn == PiFacePins.INPUT04 or pn == PiFacePins.INPUT05 or
                pn == PiFacePins.INPUT06 or pn == PiFacePins.INPUT07):
            self.mode = PinMode.IN
        elif (pn == PiFacePins.OUTPUT00 or pn == PiFacePins.OUTPUT01 or
                pn == PiFacePins.OUTPUT02 or pn == PiFacePins.OUTPUT03 or
                pn == PiFacePins.OUTPUT04 or pn == PiFacePins.OUTPUT05 or
                pn == PiFacePins.OUTPUT06 or pn == PiFacePins.OUTPUT07):
            self.mode = PinMode.OUT

    @property
    def inner_pin(self):
        """Get the inner pin."""
        return PiFacePins.NONE

    def dispose(self):
        """Dispose managed resources.

        Performs application-defined tasks associated with freeing, releasing,
        or resetting resources.
        """
        if self.is_disposed:
            return

        self.__pwm = 0
        self.__pwmRange = 0
        super(PiFaceGPIO, self).dispose()

    @property
    def pwm(self):
        """Get the PWM (pulse-width modulation) value.

        :returns: The PWM value.
        :rtype: int
        """
        return self.__pwm

    @pwm.setter
    def pwm(self, val):
        """Set the PWM (pulse-width modulation) value.

        :param val: The PWM value.
        :type val: int
        """
        self.__pwm = val

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
        self.__pwmRange = rng
