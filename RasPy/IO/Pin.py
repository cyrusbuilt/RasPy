"""A phyiscal pin.

Pin.py

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
from RasPy.Disposable import Disposable
from RasPy.IO import PinState
from RasPy.IO import PinMode


class Pin(Disposable):
    """A physical pin base class."""

    __pinName = StringUtils.EMPTY
    __tag = None

    def __init__(self):
        """Initialize a new instance of RasPy.IO.Pin."""
        super(Pin, self).__init__()

    def dispose(self):
        """Dispose managed resources.

        In a subclass, performs application-defined tasks associated with
        freeing, releasing, or resetting resources.
        """
        if self.is_disposed:
            return

        self.__pinName = None
        self.__tag = None
        super(Pin, self).dispose()

    @property
    def pin_name(self):
        """Get the pin name.

        :returns: The name of the pin.
        :rtype: string
        """
        return self.__pinName

    @pin_name.setter
    def pin_name(self, name):
        """Set the pin name.

        :param name: The name of the pin.
        :type name: string
        """
        self.__pinName = name

    @property
    def tag(self):
        """Get the tag.

        :returns: The object reference this instance is tagged with.
        :rtype: object
        """
        return self.__tag

    @tag.setter
    def tag(self, tag):
        """Set the tag.

        :param tag: The object reference to tag this instance with.
        :type tag: object
        """
        self.__tag = tag

    @property
    def state(self):
        """Get the state of the pin.

        :returns: The pin state.
        :rtype: int
        """
        return PinState.LOW

    @property
    def mode(self):
        """Get the pin mode.

        :returns: The pin mode.
        :rtype: int
        """
        return PinMode.TRI

    @property
    def pin_address(self):
        """Get the pin address (GPIO number).

        :returns: The pin address.
        :rtype: int
        """
        return 0
