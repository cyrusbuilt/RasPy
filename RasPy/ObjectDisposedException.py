"""Object disposed exception.

ObjectDisposedException.py

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


class ObjectDisposedException(Exception):
    """Object disposed exception.

    The exception that is thrown when an object is referenced that has been
    disposed.
    """

    def __init__(self, objname):
        """Initialize a new instance of RasPy.ObjectDisposedException.

        Initializes with the object that has been disposed.

        :param self: Reference to self.
        :param objname: The name of the object that has been disposed.
        :type self: ObjectDisposedException
        :type objname: string
        """
        msg = objname + " has been disposed and can no longer be referenced."
        super(ObjectDisposedException, self).__init__(msg)
