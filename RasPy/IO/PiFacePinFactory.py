"""Contains factory methods for creating PiFace digital I/O's.

The PiFace is an expansion board for the Raspberry Pi.

PiFacePinFactory.py

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
from RasPy.IO import PinMode
from RasPy.IO import PinState
from RasPy.IO import PinPullResistance
from RasPy.IO.PiFaceGpioDigital import PiFaceGpioDigital


def create_output_pin(pin, name):
    """Factory method for creating a PiFace digital output pin.

    :param pin: The pin to create an output for.
    :type pin: object
    :param name: The name of the pin. If not specified, the default hardware
    name of the pin will be used instead.
    :type name: string
    :returns: A PiFace digital output.
    :rtype: RasPy.IO.PiFaceGpioDigital
    :raises: RasPy.IO.IOException if unable to communicate with the SPI bus.
    """
    if StringUtils.is_null_or_empty(name):
        name = pin.name

    val = pin.value
    speed = PiFaceGpioDigital.BUS_SPEED
    pfgd = PiFaceGpioDigital(pin, PinState.LOW, val, speed)
    pfgd.pin_name = name
    pfgd.mode = PinMode.OUT
    pfgd.pull_resistance = PinPullResistance.OFF
    return pfgd


def create_input_pin(pin, name):
    """Factory method for creating a PiFace digital input pin.

    Creates an input pin with the internal pull-up resistor enabled.

    :param pin: The pin to create an output for.
    :type pin: object
    :param name: The name of the pin. If not specified, the default hardware
    name of the pin will be used instead.
    :type name: string
    :returns: A PiFace digital input.
    :rtype: RasPy.IO.PiFaceGpioDigital
    :raises: RasPy.IO.IOException if unable to communicate with the SPI bus.
    """
    if StringUtils.is_null_or_empty(name):
        name = pin.name

    val = pin.value
    speed = PiFaceGpioDigital.BUS_SPEED
    pfgd = PiFaceGpioDigital(pin, PinState.LOW, val, speed)
    pfgd.pin_name = name
    pfgd.mode = PinMode.IN
    pfgd.pull_resistance = PinPullResistance.PULL_UP
    return pfgd
