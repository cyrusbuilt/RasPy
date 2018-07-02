"""This module contains the OpenerStateChangeEvent type."""


from raspy.devices.access import opener_state


class OpenerStateChangeEvent(object):
    """The event that fires when an opener device changes state."""

    def __init__(self, old_state=opener_state.CLOSED,
                 new_state=opener_state.CLOSED):
        """Initialize a new instance of OpenerStateChangeEvent.

        :param int old_state: The previous state of the opener.
        :param int new_state: The current state of the opener.
        """
        self.__oldState = old_state
        self.__newState = new_state

    @property
    def old_state(self):
        """Get the previous state of the opener.

        :returns: The previous opener state.
        :rtype: int
        """
        return self.__oldState

    @property
    def new_state(self):
        """Get the current state of the opener.

        :returns: The new (current) opener state.
        :rtype: int
        """
        return self.__newState
