"""Pin state change event.

PinStateChangeEvent.py

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


class PinStateChangeEvent(object):
    """Pin state change event."""

    def __init__(self, oldState, newState, pinAddress):
        """Initialize a new instance of the PinStateChangeEvent.

        Initializes a new instance of the RasPy.IO.PinStateChangeEvent class
        with the previous pin state, new pin state, and pin address.

        :param oldState: The previous pin state.
        :param newState: The new (current) pin state.
        :param pinAddress: The pin address.
        :type oldState: int
        :type newState: int
        :type pinAddress: int
        """
        self.__oldState = oldState
        self.__newState = newState
        self.__pinAddress = pinAddress

    @property
    def old_state(self):
        """Get the previous state of the pin.

        :returns: The previous pin state.
        :rtype: int
        """
        return self.__oldState

    @property
    def new_state(self):
        """Get the new (current) state of the pin.

        :returns: The new (current) pin state.
        :rtype: int
        """
        return self.__newState

    @property
    def pin_address(self):
        """Get the pin address.

        :returns: The pin address (GPIO number).
        :rtype: int
        """
        return self.__pinAddress
