"""This module contains the Size structure class."""


class Size(object):
    """A 2-dimensional size structure."""

    def __init__(self, width=0, height=0):
        """Initialize new instance of raspy.size.Size class.

        Initializes a new instance of the Size class with the width and height.

        :param int width: The width.
        :param int height: The height.
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
    def width(self, width):
        """Set the width.

        Sets the size width.

        :param int width: The width.
        """
        self._width = width

    @property
    def height(self):
        """Get the height.

        Gets the size height.

        :returns: The height.
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Set the height.

        Sets the size height.

        :param int height: The height.
        """
        self._height = height


EMPTY = Size()
"""An empty instance of Size."""
