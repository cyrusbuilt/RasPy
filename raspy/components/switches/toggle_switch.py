"""This module contains the ToggleSwitch type."""


from raspy.components.switches.switch import Switch


class ToggleSwitch(Switch):
    """An interface/base for toggle switch device abstractions."""

    def __init__(self):
        """Initialize a new instance of ToggleSwitch."""
        Switch.__init__(self)
