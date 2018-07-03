"""This module contains the FireplaceStateChangeEvent type."""


from raspy.devices.fireplaces import fireplace_state


class FireplaceStateChangeEvent(object):
    """The event that fires when the fireplace changes state."""

    def __init__(self, old_state=fireplace_state.OFF,
                 new_state=fireplace_state.OFF):
        """Initialize a new instance of FireplaceStateChangeEvent.

        :param int old_state: The previous state.
        :param int new_state: The current state.
        """
        self.__oldState = old_state
        self.__newState = new_state

    @property
    def old_state(self):
        """Get the previous state.

        :returns: The previous state.
        :rtype: int
        """
        return self.__oldState

    @property
    def new_state(self):
        """Get the current state.

        :returns: The current state.
        :rtype: int
        """
        return self.__newState
