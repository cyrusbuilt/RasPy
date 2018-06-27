"""This module contains the SensorComponent type."""


import threading
from raspy.invalid_operation_exception import InvalidOperationException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.sensors import sensor
from raspy.components.sensors import sensor_state
from raspy.components.sensors.sensor_state_change_event import SensorStateChangeEvent
from raspy.io import pin_mode
from raspy.io import pin_state
from raspy.pi_system import core_utils


OPEN_STATE = pin_state.LOW
"""The pin state used to consider the sensor open."""


class SensorComponent(sensor.Sensor):
    """A component that is an abstraction of a sensor device."""

    def __init__(self, pin):
        """Initialize a new instance of SensorComponent.

        :param raspy.io.gpio.Gpio pin: The input pin to sample the sensor
        data from.
        :raises: raspy.argument_null_exception.ArgumentNullException if
        pin is None.
        """
        sensor.Sensor.__init__(self, pin)
        self.__isPolling = False
        self.__pollThread = None
        self.__stopEvent = threading.Event()
        self.__stopEvent.set()
        self.__lastState = sensor_state.OPEN

    @property
    def state(self):
        """Get the state of the sensor.

        :returns: The sensor state.
        :rtype: int
        """
        if self.pin.state == OPEN_STATE:
            return sensor_state.OPEN
        return sensor_state.CLOSED

    @property
    def is_polling(self):
        """Check to see if this sensor is polling.

        :returns: True if actively polling.
        :rtype: bool
        """
        return self.__isPolling

    def _execute_poll(self):
        """Execute the poll cycle."""
        while not self.__stopEvent.is_set():
            new_state = self.state
            if new_state != self.__lastState:
                old_state = self.__lastState
                self.__lastState = new_state
                evt = SensorStateChangeEvent(self, old_state, new_state)
                self.on_sensor_state_change(evt)
        core_utils.sleep(200)

    def interrupt_poll(self):
        """Interrupt the poll cycle."""
        if not self.__isPolling or self.is_disposed:
            return

        if self.__stopEvent.is_set() or self.__pollThread is None:
            return

        self.__stopEvent.set()
        self.__isPolling = False

    def poll(self):
        """Poll the input pin status every 200ms until stopped.

        :raises: ObjectDisposedException if this instance has been disposed.
        :raises: InvalidOperationException if the underlying pin is not
        configured as an input.
        """
        if self.is_disposed:
            raise ObjectDisposedException("SensorComponent")

        if self.pin.mode != pin_mode.IN:
            msg = "The specified pin is not configured as an input pin, which "
            msg += "is required to read sensor data."
            raise InvalidOperationException(msg)

        if self.__isPolling:
            return

        self.__stopEvent.clear()
        self.__isPolling = True
        self.__pollThread = threading.Thread(target=self._execute_poll)
        self.__pollThread.name = "SensorComponentPollThread"
        self.__pollThread.daemon = True
        self.__pollThread.start()

    def dispose(self):
        """Release managed resources used by this component."""
        if self.is_disposed:
            return

        self.interrupt_poll()
        self.__pollThread = None
        self.__stopEvent = None
        self.__lastState = sensor_state.OPEN
        sensor.Sensor.dispose(self)
