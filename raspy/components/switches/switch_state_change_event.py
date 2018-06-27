"""This module contains the SwitchStateChangeEvent type."""


from raspy.components.switches import switch_state


class SwitchStateChangeEvent(object):
    """The event that gets fired when a switch changes state."""

    def __init__(self, old_state=switch_state.OFF, new_state=switch_state.OFF):
        """Initialize a new instance of SwitchStateChangeEvent."""
        self.__oldState = old_state
        self.__newState = new_state

    @property
    def old_state(self):
        """Get the old state.

        :returns: The previous state.
        :rtype: int
        """
        return self.__oldState

    @property
    def new_state(self):
        """Get the new state.

        :returns: The new (current) state.
        :rtype: int
        """
        return self.__newState
