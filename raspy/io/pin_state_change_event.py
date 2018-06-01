"""Pin state change event."""


class PinStateChangeEvent(object):
    """Pin state change event."""

    def __init__(self, old_state, new_state, pin_address):
        """Initialize a new instance of the PinStateChangeEvent.

        Initializes a new instance of the raspy.io.PinStateChangeEvent class
        with the previous pin state, new pin state, and pin address.

        :param int old_state: The previous pin state.
        :param int new_state: The new (current) pin state.
        :param int pin_address: The pin address.
        """
        self.__oldState = old_state
        self.__newState = new_state
        self.__pinAddress = pin_address

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
