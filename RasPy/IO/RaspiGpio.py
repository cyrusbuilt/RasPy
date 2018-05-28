"""A Raspberry Pi GPIO Interface.

RaspiGpio.py

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


from RasPy import BoardRevision
from RasPy.IO import GpioPins
from RasPy.IO.Gpio import Gpio


class RaspiGpio(Gpio):
    """A Raspberry Pi GPIO interface."""

    def __init__(self):
        """Initializes a new instance of the RasPy.IO.RaspiGpio class."""
        super(Gpio, self).__init__()

    @property
    def revision(self):
        """Get the board revision.

        :returns: The board revision.
        :rtype: int
        """
        return BoardRevision.REV2

    @property
    def inner_pin(self):
        """Get the inner pin being represented by this instance.

        :returns: The underlying physical pin.
        :rtype: RasPy.IO.GpioPins
        """
        return GpioPins.GPIO_NONE

    def on_pin_state_change(self, psce):
        """Fire the pin state change event.

        :param psce: The pin state change event.
        :type psce: RasPy.IO.PinStateChangeEvent
        """
        pass
