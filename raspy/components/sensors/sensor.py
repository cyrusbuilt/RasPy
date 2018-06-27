"""This module contains the Sensor interface/base type."""


import threading
from pyee import EventEmitter
from raspy.argument_null_exception import ArgumentNullException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.component import Component
from raspy.components.sensors import sensor_state


EVENT_STATE_CHANGED = "sensorStateChanged"
"""The name of the sensor state changed event."""


class Sensor(Component):
    """A sensor abstraction component interface."""

    def __init__(self, pin):
        """Initialize a new instance of Sensor.

        :param raspy.io.gpio.Gpio pin: The input pin to sample data from.
        :raises: ArgumentNullException if 'pin' param is None.
        """
        Component.__init__(self)
        if pin is None:
            raise ArgumentNullException("'pin' param cannot be None.")

        self.__emitter = EventEmitter()
        self.__state = sensor_state.OPEN
        self.__pin = pin
        self.__pin.provision()

    def dispose(self):
        """Release managed resources used by this component."""
        if self.is_disposed:
            return

        if self.__pin is not None:
            self.__pin.dispose()
            self.__pin = None

        self.__state = sensor_state.OPEN
        self.__emitter.remove_all_listeners()
        self.__emitter = None
        Component.dispose(self)

    def on(self, evt, callback):
        """Register an event with a callback to handle it.

        :param str evt: The name of the event to register a handler for.
        :param function callback: The callback to execute when the event
        fires.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance is disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Sensor")

        self.__emitter.on(evt, callback)

    def emit(self, evt, args):
        """Emit the specified event to all registered listeners.

        :param str evt: The name of the event to emit.
        :param object args: The arguments to pass to the event handlers
        (listeners).
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance is disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Sensor")

        self.__emitter.emit(evt, args)

    def remove_all_listeners(self):
        """Remove all registered event listeners."""
        if self.is_disposed:
            return

        if self.__emitter is not None:
            self.__emitter.remove_all_listeners()

    def on_sensor_state_change(self, change_evt):
        """Fire the sensor state change event.

        :param sensor_state_change_event.SensorStateChangeEvent change_evt:
        The state change event object.
        :raises: ObjectDisposedException if this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Sensor")

        _t = threading.Thread(target=self.emit,
                              name=EVENT_STATE_CHANGED,
                              args=(EVENT_STATE_CHANGED, change_evt))
        _t.daemon = True
        _t.start()

    @property
    def state(self):
        """Get the state of the sensor.

        :returns: The sensor state.
        :rtype: int
        """
        return self.__state

    def is_state(self, sens_state):
        """Check to see if the sensor is in the specified state.

        :param int sens_state: The state to check.
        :returns: True if in the specified state.
        :rtype: bool
        """
        return self.state == sens_state

    @property
    def is_open(self):
        """Get a value indicating whether this is sensor is open.

        :returns: True if open; Otherwise, False.
        :rtype: bool
        """
        return self.is_state(sensor_state.OPEN)

    @property
    def is_closed(self):
        """Get a value indicating whether this sensor is closed.

        :returns: True if closed; Otherwise, False.
        :rtype: bool
        """
        return self.is_state(sensor_state.CLOSED)

    @property
    def pin(self):
        """Get the pin being used to sample sensor data.

        :returns: The underlying physical pin.
        :type: raspy.io.gpio.Gpio
        """
        return self.__pin
