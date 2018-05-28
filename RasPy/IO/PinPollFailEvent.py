"""Pin poll failure event.

PinPollFailEvent.py

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


class PinPollFailEvent(object):
    """Pin poll failure event."""

    def __init__(self, cause):
        """Initialize a new instance of PinPollFailEvent.

        Initializes a new instance of the RasPy.IO.PinPollFailEvent class
        with the exception that is the cause of the event.

        :param cause: The Error (exception) that is the cause of the event.
        :type cause: Exception
        """
        self.__cause = cause

    @property
    def failure_cause(self):
        """Get the exception that caused the event.

        :returns: The Error or Exception that caused the event.
        :rtype: Exception
        """
        return self.__cause
