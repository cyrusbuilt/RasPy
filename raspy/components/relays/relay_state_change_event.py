"""This module contains the RelayStateChangeEvent type."""


from raspy.components.relays import relay_state


class RelayStateChangeEvent(object):
    """The event that fires when a relay changes state."""

    def __init__(self, old_state=relay_state.OPEN, new_state=relay_state.OPEN):
        """Initialize a new intance of RelayStatechangeEvent.

        :param int old_state: The previous relay state.
        :param int new_state: The current relay state.
        """
        self.__oldState = old_state
        if self.__oldState is None:
            self.__oldState = relay_state.OPEN

        self.__newState = new_state
        if self.__newState is None:
            self.__newState = relay_state.OPEN

    @property
    def old_state(self):
        """Get the previous state of the relay.

        :returns: The previous relay state.
        :rtype: int
        """
        return self.__oldState

    @property
    def new_state(self):
        """Get the current state of the relay.

        :returns: The current relay state.
        :rtype: int
        """
        return self.__newState
