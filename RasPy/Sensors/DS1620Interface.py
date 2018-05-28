"""Implemented by classes that represent DS1620 sensors.

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


from RasPy import Disposable


class DS1620Interface(Disposable):
    """Implemented by classes that represent DS1620 sensors."""

    def __init__(self):
        """Initializes a new instance of RasPy.Sensors.DS1620Interface"""

        super(Disposable, self).__init__()

    @property
    def clock_pin(self):
        """Get the clock pin.

        :returns: The clock pin.
        :rtype: RasPy.IO.Gpio
        """
        return None

    @property
    def data_pin(self):
        """Get the data pin.

        :returns: The data pin.
        :rtype: RasPy.IO.Gpio
        """
        return None

    @property
    def reset_pin(self):
        """Get the reset pin.

        :returns: The reset pin.
        :rtype: RasPy.IO.Gpio
        """
        return None

    def get_temperature(self):
        """Send commands to get the temperature from the sensor.

        :returns: The temperature with half-degree granularity.
        :rtype: long
        :raises: RasPy.ObjectDisposedException if this instance has been disposed.
        """
        return 0
