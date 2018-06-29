"""This module contains the TempSensorComponent type."""


import threading
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.temperature import temp_scale
from raspy.components.temperature import temp_sensor
from raspy.components.temperature import temp_conversion
from raspy.components.temperature.temp_change_event import TempChangeEvent
from raspy.pi_system import core_utils


class TempSensorComponent(temp_sensor.TemperatureSensor):
    """A component that is an abstraction of a temperature sensor device."""

    def __init__(self, scale, clock, data, reset):
        """Initialize a new instance of TempSensorComponent.

        :param int scale:
        :param raspy.io.gpio.Gpio clock: The GPIO pin used for the clock.
        :param raspy.io.gpio.Gpio data: The GPIO used for data.
        :param raspy.io.gpio.Gpio reset: The GPIO pin used to trigger reset.
        :raises: ArgumentNullException if any of the pins are None.
        """
        temp_sensor.TemperatureSensor.__init__(self, clock, data, reset)
        self.scale = scale
        self.__isPolling = False
        self.__lastTemp = 0.0
        self.__pollThread = None
        self.__stopEvent = threading.Event()
        self.__stopEvent.set()

    def is_polling(self):
        """Check to see if this instance is currently polling.

        :returns: True if polling; Otherwise, False.
        :rtype: bool
        """
        return self.__isPolling

    def interrupt_poll(self):
        """Interrupt the poll cycle."""
        if not self.__isPolling or self.is_disposed:
            return

        if self.__stopEvent.is_set() or self.__pollThread is None:
            return

        self.__stopEvent.set()
        self.__isPolling = False

    def dispose(self):
        """Release all managed resources used by this component."""
        if self.is_disposed:
            return

        self.interrupt_poll()
        self.__lastTemp = 0.0
        self.__stopEvent = None
        self.__pollThread = None
        temp_sensor.TemperatureSensor.dispose(self)

    def get_raw_temperature(self):
        """Get the raw temperature value.

        :returns: The raw value read from the sensor.
        :rtype: float
        :raises: ObjectDisposedException if this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("TempSensorComponent")

        cel = temp_scale.CELCIUS
        temp = self.sensor.get_temperature()
        if self.scale != cel:
            return temp_conversion.convert(cel, self.scale, temp)
        return temp

    def _execute_poll(self):
        """Execute the poll cycle."""
        while not self.__stopEvent.is_set():
            new_temp = self.get_raw_temperature()
            if new_temp != self.__lastTemp:
                old_temp = self.__lastTemp
                self.__lastTemp = new_temp
                evt = TempChangeEvent(old_temp, new_temp)
                self.on_temperature_change(evt)

            core_utils.sleep(200)

    def poll(self):
        """Poll the input pin status every 200ms."""
        if self.is_disposed:
            raise ObjectDisposedException("TempSensorComponent")

        if self.__isPolling:
            return

        self.__stopEvent.clear()
        self.__isPolling = True
        self.__pollThread = threading.Thread(target=self._execute_poll)
        self.__pollThread.name = "TempSensorComponentPollThread"
        self.__pollThread.daemon = True
        self.__pollThread.start()
