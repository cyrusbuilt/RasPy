"""Contains utility methods for working with pins.

PinUtils.py

Author:
      Chris Brunner <cyrusbuilt at gmail dot com>

  Copyright (c) 2015 CyrusBuilt

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
from RasPy.IO.IOException import IOException


def get_pin_mode_name(mode):
    """Convert the specified mdoe to its name string.

    :param mode: The mode to get the name of.
    :type mode: int
    :returns: The mode name.
    :rtype: string
    """
    if not isinstance(mode, (int, long)):
        return StringUtils.EMPTY

    if mode == PinMode.IN:
        return "IN"

    elif mode == PinMode.OUT:
        return "OUT"

    elif mode == PinMode.PWM:
        return "PWM"

    elif mode == PinMode.CLOCK:
        return "CLOCK"

    elif mode == PinMode.UP:
        return "UP"

    elif mode == PinMode.DOWN:
        return "DOWN"

    elif mode == PinMode.TRI:
        return "TRI"

    else:
        return StringUtils.EMPTY


def write_fs_pin(pinPath, valString):
    """Write the specified string to the specified pin.

    :param pinPath: The full path to the pin to write to.
    :param valString: The value string to write to the pin.
    :type pinPath: string
    :type valString: string
    :raises: RasPy.IO.IOException if an IOError occurred while accessing the
    pin.
    """
    try:
        target = open(pinPath, 'w')
        target.write(valString)
        target.close()
    except IOError as ex:
        raise IOException(ex.strerror)


def read_fs_pin(pinPath):
    """Read the value from the specified pin.

    :param pinPath: The full path to the pin to write to.
    :type pinPath: string
    :returns: The value read from the pin.
    :rtype: int
    :raises: RasPy.IO.IOException if an IOError occurred while accessing the
    pin.
    """
    val = 0

    try:
        target = open(pinPath, 'r')
        readString = target.read()
        val = int(readString[0:1])
        target.close()
    except IOError as ex:
        raise IOException(ex.strerror)

    return val
