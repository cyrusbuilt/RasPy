"""This module contains the TempChangeEvent type."""


class TempChangeEvent(object):
    """The event that gets fired when a change in temperature occurs."""

    def __init__(self, old_temp=0.0, new_temp=0.0):
        """Initialize a new instance of TempChangeEvent.

        :param float old_temp: The temperature value prior to the change event.
        :param float new_temp: The temperature value after the change event.
        """
        self.__oldTemp = old_temp
        self.__newTemp = new_temp

    @property
    def old_temp(self):
        """Get the previous temperature value.

        :returns: The previous temperature.
        :rtype: float
        """
        return self.__oldTemp

    @property
    def new_temp(self):
        """Get the current temperature value.

        :returns: The new (current) temperature value.
        :rtype: float
        """
        return self.__newTemp

    def get_temperature_change(self):
        """Get the difference temperature from the old temp to the new temp.

        :returns: The change value (difference).
        :rtype: float
        """
        return self.__newTemp - self.__oldTemp
