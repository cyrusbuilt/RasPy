"""This module contains the MomentarySwitch type."""


from raspy.components.switches.switch import Switch


class MomentarySwitch(Switch):
    """An interface/base for momentary switch device abstractions."""

    def __init__(self):
        """Initialize a new instance of MomentarySwitch."""
        Switch.__init__(self)
