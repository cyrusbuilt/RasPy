"""Unrecognized pin found event.

UnrecognizedPinFoundEvent.py

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


class UnrecognizedPinFoundEvent(object):
    """Unrecognized pin found event."""

    def __init__(self, message):
        """Initialize a new instance of the UnrecognizedPinFoundEvent class.

        Initializes a new instance of the RasPy.IO.UnrecognizedPinFoundEvent
        class with a message describing the event.

        :param message: A message describing the event.
        :type message: string
        """
        self.__message = message

    @property
    def event_message(self):
        """Get the message describing the event.

        :returns: The event message.
        :rtype: string
        """
        return self.__message
