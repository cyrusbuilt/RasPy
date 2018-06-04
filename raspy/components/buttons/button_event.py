"""This module contains the buttons event type."""


class ButtonEvent(object):
    """Button event argument class."""

    def __init__(self, button):
        """Initialize a new instance of the ButtonEvent with the buttons.

        :param raspy.components.buttons.button.Button button: The button that
        triggered the event.
        """
        self.__button = button

    @property
    def button(self):
        """Get the button that triggered the event.

        :returns: The button that triggered the event.
        :rtype: raspy.components.buttons.button.Button
        """
        return self.__button

    @property
    def is_pressed(self):
        """Get a flag indicating whether or not the button is pressed.

        :returns: True if the button is pressed.
        :rtype: bool
        """
        if self.__button is None:
            return False

        return self.__button.is_pressed

    @property
    def is_released(self):
        """Get a flag indicating whether or not the button is released.

        :returns: True if the button is released.
        :rtype: bool
        """
        if self.__button is None:
            return False

        return self.__button.is_released

    def is_state(self, state):
        """Get a flag indicating whether or not the button is of the state.

        :param int state: The button state to check.
        :returns: True if the button is in the specified state.
        :rtype: bool
        """
        if self.__button is None:
            return False

        return self.__button.is_state(state)
