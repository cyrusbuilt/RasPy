"""Provides base class for defining a disosable type.

Disposable.py

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


class Disposable(object):
    """Base class for a disposable type.

    Defines a type which provides a mechanism for releasing unmanaged
    resources.
    """

    __isDisposed = False

    def __init__(self):
        """Constructor."""
        pass

    def dispose(self):
        """Dispose managed resources.

        In a subclass, performs application-defined tasks associated with
        freeing, releasing, or resetting resources.
        """
        self.__isDisposed = True

    @property
    def is_disposed(self):
        """Determine if instance has been disposed.

        In a subclass, determines whether or not the current instance has been
        disposed.

        :returns: True if disposed; Otherwise, False.
        :rtype: bool
        """
        return self.__isDisposed
