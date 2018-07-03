"""This module contains the FireplacePilotLightEvent type."""


class FireplacePilotLightEvent(object):
    """The event that fires when a pilot light event occcurs."""

    def __init__(self, light_is_on=False):
        """Initialize a new instance of FireplacePilotLightevent.

        :param bool light_is_on: Set True if the pilot light is on.
        """
        self.__isLightOn = light_is_on

    @property
    def light_is_on(self):
        """Get a flag indicating whether the pilot light is on.

        :returns: True if the pilot light is on.
        :rtype: bool
        """
        return self.__isLightOn
