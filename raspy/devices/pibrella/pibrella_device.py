"""This module contains the PiBrellaDevice type."""


from raspy.devices.pibrella.pibrella_interface import PiBrellaInterface


class PiBrellaDevice(PiBrellaInterface):
    """An abstraction of a PiBrella device."""

    def __init__(self):
        """Initialize a new instance of PiBrellaDevice."""
        PiBrellaInterface.__init__(self)
