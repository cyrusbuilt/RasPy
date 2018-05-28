"""Size class.

Size.py

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


class Size(object):
    """A 2-dimensional size structure."""

    def __init__(self, width=0, height=0):
        """Initialize new instance of RasPy.Size class.

        Initializes a new instance of the Size class with the width and height.

        :param width: The width.
        :param height: The height.
        :type width: int
        :type height: int
        """
        if width is None or not isinstance(width, int):
            width = 0

        if height is None or not isinstance(height, int):
            height = 0

        self._width = width
        self._height = height

    @property
    def width(self):
        """Get the width.

        Gets the size width.

        :returns: The width.
        :rtype: int
        """
        return self._width

    @width.setter
    def width(self, w):
        """Set the width.

        Sets the size width.

        :param w: The width.
        :type w: int
        """
        self._width = w

    @property
    def height(self):
        """Get the height.

        Gets the size height.

        :returns: The height.
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, h):
        """Set the height.

        Sets the size height.

        :param h: The height.
        :type h: int
        """
        self._height = h


EMPTY = Size()
"""An empty instance of Size."""
