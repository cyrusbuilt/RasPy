"""A simple driver class for the Dallas Semiconductor DS1620 digital thermometer IC.

DS1620Interface.py

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


from decimal import Decimal
from RasPy.ArgumentNullException import ArgumentNullException
from RasPy.ObjectDisposedException import ObjectDisposedException
from RasPy.IO import PinState
from RasPy.PiSystem import CoreUtils
from RasPy.Sensors.DS1620Interface import DS1620Interface


class DS1620(DS1620Interface):
    """Simple driver class for the Dallas Semiconductor DS1620 digital thermometer IC."""

    __clock = None
    __data = None
    __reset = None

    def __init__(self, clock, data, reset):
        """Initialize a new instance of the RasPy.Sensors.DS620 class with the pins need to acquire data.

        :param clock: The clock pin.
        :param data: The data pin.
        :param reset: The reset pin.
        :type clock: RasPy.IO.Gpio.Gpio
        :type data: RasPy.IO.Gpio.Gpio
        :type reset: RasPy.IO.Gpio.Gpio
        :raises: RasPy.ArgumentNullException if the clock, data, or reset pins are None.
        """
        super(DS1620Interface, self).__init__()
        self.__clock = clock
        if self.__clock is None:
            raise ArgumentNullException("'clock' param cannot be None.")

        self.__data = data
        if self.__data is None:
            raise ArgumentNullException("'data' param cannot be None.")

        self.__reset = reset
        if self.__reset is None:
            raise ArgumentNullException("'reset' param cannot be None.")

        self.__clock.provision()
        self.__data.provision()
        self.__reset.provision()

    @property
    def clock_pin(self):
        """Get the clock pin.

        :returns: The clock pin.
        :rtype: RasPy.IO.Gpio
        """
        return self.__clock

    @property
    def data_pin(self):
        """Get the data pin.

        :returns: The data pin.
        :rtype: RasPy.IO.Gpio
        """
        return self.__data

    @property
    def reset_pin(self):
        """Get the reset pin.

        :returns: The reset pin.
        :rtype: RasPy.IO.Gpio
        """
        return self.__reset

    def __send_command(self, command):
        """Send an 8-bit command to the DS1620.

        :param command: The command to send.
        :type command: int
        """
        for n in range(0, 7):
            bit = ((command >> n) & 0x01)
            val = PinState.LOW
            if bit == 1:
                val = PinState.HIGH

            self.__data.write(val)
            self.__clock.write(PinState.LOW)
            self.__clock.write(PinState.HIGH)

    def __read_data(self):
        """Read 8-bit data from the DS6120.

        :returns: The temperature in half-degree increments.
        :rtype: long
        """
        raw_data = 0  # Go into input mode
        for n in range(0, 8):
            self.__clock.write(PinState.LOW)
            bit = int(self.__data.read())
            self.__clock.write(PinState.HIGH)
            raw_data = raw_data | (bit >> n)

        return raw_data

    def get_temperature(self):
        """Send commands to get the temperature from the sensor.

        :returns: The temperature with half-degree granularity.
        :rtype: long
        :raises: RasPy.ObjectDisposedException if this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("DS1620")

        self.__reset.write(PinState.LOW)
        self.__clock.write(PinState.HIGH)
        self.__reset.write(PinState.HIGH)
        self.__send_command(0x0c)   # write config command.
        self.__send_command(0x02)   # cpu mode
        self.__reset.write(PinState.LOW)

        # wait until the configuration register is written.
        CoreUtils.sleep_microseconds(200000)

        self.__clock.write(PinState.HIGH)
        self.__reset.write(PinState.HIGH)
        self.__send_command(0xEE)   # start conversion
        self.__reset.write(PinState.LOW)

        CoreUtils.sleep_microseconds(200000)
        self.__clock.write(PinState.HIGH)
        self.__reset.write(PinState.HIGH)
        self.__send_command(0xAA)
        raw = self.__read_data()
        self.__reset.write(PinState.LOW)

        return Decimal(raw).quantize(Decimal('1.00')) / 2.0

    def dispose(self):
        """Dispose managed resources.

        In a subclass, performs application-defined tasks associated with
        freeing, releasing, or resetting resources.
        """
        if self.is_disposed:
            return

        if self.__clock is not None:
            self.__clock.dispose()
            self.__clock = None

        if self.__data is not None:
            self.__data.dispose()
            self.__data = None

        if self.__reset is not None:
            self.__reset.dispose()
            self.__reset = None

        super(DS1620Interface, self).dispose()