"""This module contains the MotorStateChangeEvent type."""


from raspy.components.motors import motor_state


class MotorStateChangeEvent(object):
    """The event that gets raised when a motor changes state."""

    def __init__(self, old_state, new_state):
        """Initialize a new instance of MotorStateChangeEvent.

        :param int old_state: The state the motor was in prior to the change.
        :param int new_state: The current state of the motor since the change.
        """
        self.__oldState = old_state
        if self.__oldState is None:
            self.__oldState = motor_state.STOP

        self.__newState = new_state
        if self.__newState is None:
            self.__newState = motor_state.STOP

    @property
    def old_state(self):
        """Get the state the motor was in prior to the change.

        :returns: The previous state.
        :rtype: int
        """
        return self.__oldState

    @property
    def new_state(self):
        """Get the new (current) state.

        :returns: The new (current) state.
        :rtype: int
        """
        return self.__newState
