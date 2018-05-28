"""The exception that is thrown when an invalid pin mode is used.

IOException.py

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


class InvalidPinModeException(Exception):
    """Invalid pin mode exception.

    The exception that is thrown when an invalid pin mode is used.
    """

    def __init__(self, message, pn):
        """Initialize new instance of RasPy.IO.InvalidPinModeException.

        Initializes a new instance of the InvalidPinModeException class with
        the pin that has the incorrect mode and a message describing the
        exception.

        :param message: The message describing the exception.
        :param pn: The pin that is the cause of the exception.
        :type message: string
        :type pn: RasPy.IO.Pin
        """
        super(InvalidPinModeException, self).__init__(message)
        self.__pin = pn

    @property
    def pin(self):
        """Get the pin that is the cause of the exception.

        :returns: The pin that is configured with the incorrect mode.
        :rtype: RasPy.IO.Pin
        """
        return self.__pin
