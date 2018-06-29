"""This module contains the TempSensor type."""


import threading
from pyee import EventEmitter
from raspy.argument_null_exception import ArgumentNullException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.component import Component
from raspy.components.temperature import temp_scale
from raspy.components.temperature import temp_conversion
from raspy.sensors.ds1620 import DS1620


EVENT_TEMPERATURE_CHANGED = "temperatureChangedEvent"
"""The name of the temperature change event."""


class TemperatureSensor(Component):
    """An abstract temperature sensor interface/base."""

    def __init__(self, clock, data, reset):
        """Initialize a new instance of TempSensor.

        :param raspy.io.gpio.Gpio clock: The GPIO pin used for the clock.
        :param raspy.io.gpio.Gpio data: The GPIO used for data.
        :param raspy.io.gpio.Gpio reset: The GPIO pin used to trigger reset.
        :raises: ArgumentNullException if any of the pins are None.
        """
        Component.__init__(self)
        if clock is None:
            raise ArgumentNullException("'clock' cannot be None.")

        if data is None:
            raise ArgumentNullException("'data' cannot be None.")

        if reset is None:
            raise ArgumentNullException("'reset' cannot be None.")

        self.__emitter = EventEmitter()
        self.__rawTemp = 0.0
        self.__scale = temp_scale.CELCIUS
        self.__tempSensor = DS1620(clock, data, reset)

    def dispose(self):
        """Release managed resources used by this component."""
        if self.is_disposed:
            return

        if self.__tempSensor is not None:
            self.__tempSensor.dispose()
            self.__tempSensor = None

        self.__rawTemp = 0.0
        self.__scale = temp_scale.CELCIUS
        self.__emitter.remove_all_listeners()
        self.__emitter = None
        Component.dispose(self)

    def on(self, evt, callback):
        """Register an event with a callback to handle it.

        :param str evt: The name of the event to register a handler for.
        :param function callback: The callback to execute when the event
        fires.
        :raises: ObjectDisposedException if this instance is disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("TempSensor")

        self.__emitter.on(evt, callback)

    def emit(self, evt, args):
        """Emit the specified event to all registered listeners.

        :param str evt: The name of the event to emit.
        :param object args: The arguments to pass to the event handlers
        (listeners).
        :raises: ObjectDisposedException if this instance is disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("TempSensor")

        self.__emitter.emit(evt, args)

    def remove_all_listeners(self):
        """Remove all registered event listeners."""
        if self.is_disposed:
            return

        if self.__emitter is not None:
            self.__emitter.remove_all_listeners()

    def get_raw_temperature(self):
        """Get the raw temperature value.

        :returns: The raw value read from the sensor.
        :rtype: float
        :raises: ObjectDisposedException if this instance has been disposed.
        """
        return self.__rawTemp

    @property
    def scale(self):
        """Get the temperature scale.

        :returns: The temperature scale.
        :rtype: int
        """
        return self.__scale

    @scale.setter
    def scale(self, the_scale):
        """Set the temperature scale.

        :param int the_scale: The temperature scale to set.
        """
        self.__scale = the_scale

    def _set_raw_temp(self, temp):
        """Set the raw temperature.

        :param float temp: The temperature to set.
        """
        self.__rawTemp = temp

    def on_temperature_change(self, change_evt):
        """Fire the temperature change event.

        :param raspy.components.temperature.temp_chang_event.TempChangeEvent change_evt:
        The event object.
        :raises: ObjectDisposedException if this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("TempSensor")

        _t = threading.Thread(target=self.emit,
                              name=EVENT_TEMPERATURE_CHANGED,
                              args=(EVENT_TEMPERATURE_CHANGED, change_evt))
        _t.daemon = True
        _t.start()

    def get_temperature(self, scale):
        """Get the temperature value.

        :param int scale: The scale to use for measurement.
        :returns: The temperature value in the specified scale.
        :rtype: float
        :raises: ObjectDisposedException if this instance has been disposed.
        """
        raw = self.get_raw_temperature()
        return temp_conversion.convert(self.scale, scale, raw)

    @property
    def sensor(self):
        """Get the sensor being used to measure.

        :returns: The temperature sensor.
        :rtype: raspy.sensors.ds1620.DS1620
        """
        return self.__tempSensor
