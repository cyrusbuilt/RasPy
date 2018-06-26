"""This module contains the PowerStateChangeEvent type."""


from raspy.components.power import power_state


class PowerStateChangeEvent(object):
    """The event that gets fired when a power control device changes state."""

    def __init__(self, old_state=power_state.UNKNOWN, new_state=power_state.UNKNOWN):
        """Initialize a new instance of PowerStateChangeEvent.

        :param int old_state: The previous state of the device.
        :param int new_state: The new state of of the device.
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
        """Get the new (current) state.

        :returns: The current state.
        :rtype: int
        """
        return self.__newState
