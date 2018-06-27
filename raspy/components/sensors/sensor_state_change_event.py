"""This module contains the SensorStateChangeEvent type."""


from raspy.components.sensors import sensor_state


class SensorStateChangeEvent(object):
    """The event that fires when a sensor changes state."""

    def __init__(self, sensor, old_state=sensor_state.OPEN,
                 new_state=sensor_state.CLOSED):
        """Initialize a new instance of SensorStateChangeEvent.

        :param sensor.Sensor sensor: The sensor that changed state.
        :param int old_state: The previous state.
        :param int new_state: The current state.
        """
        self.__sensor = sensor
        self.__oldState = old_state
        if self.__oldState is None:
            self.__oldState = sensor_state.OPEN
        self.__newState = new_state
        if self.__newState is None:
            self.__newState = sensor_state.OPEN

    @property
    def sensor(self):
        """Get the sensor that changed state.

        :returns: The sensor that changed state.
        :rtype: sensor.Sensor
        """
        return self.__sensor

    @property
    def old_state(self):
        """Get the previous state of the sensor.

        :returns: The previous sensor state.
        :rtype: int
        """
        return self.__oldState

    @property
    def new_state(self):
        """Get the current state of the sensor.

        :returns: The current sensor state.
        :rtype: int
        """
        return self.__oldState
