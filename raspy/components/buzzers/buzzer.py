"""This module contains the Buzzer base type."""


from raspy.components.component import Component


class Buzzer(Component):
    """A piezo buzzer device abstraction component base type."""

    def __init__(self):
        """Initialize a new instance of a Buzzer."""
        Component.__init__(self)

    def buzz(self, freq, duration=None):
        """Start the buzzer at the specified freq.

        :param float freq: The frequency to buzz at.
        :param float duration: The duration in milliseconds. If not specified,
        buzzes until stopped.
        """
        pass

    def stop(self):
        """Stop the buzzer."""
        pass
