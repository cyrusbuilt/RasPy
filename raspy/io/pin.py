"""This module contains the base type for a phyiscal pin."""


from raspy import string_utils
from raspy.disposable import Disposable
from raspy.io import pin_state
from raspy.io import pin_mode


class Pin(Disposable):
    """A physical pin base class."""

    __pinName = string_utils.EMPTY
    __tag = None

    def __init__(self):
        """Initialize a new instance of raspy.io.Pin."""
        super(Disposable, self).__init__()

    def dispose(self):
        """Dispose managed resources.

        In a subclass, performs application-defined tasks associated with
        freeing, releasing, or resetting resources.
        """
        if self.is_disposed:
            return

        self.__pinName = None
        self.__tag = None
        Disposable.dispose(self)

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

        :param string name: The name of the pin.
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

        :param object tag: The object reference to tag this instance with.
        """
        self.__tag = tag

    @property
    def state(self):
        """Get the state of the pin.

        :returns: The pin state.
        :rtype: int
        """
        return pin_state.LOW

    @property
    def mode(self):
        """Get the pin mode.

        :returns: The pin mode.
        :rtype: int
        """
        return pin_mode.TRI

    @property
    def pin_address(self):
        """Get the pin address (GPIO number).

        :returns: The pin address.
        :rtype: int
        """
        return 0
