"""This module contains the MotionSensorComponent type."""


import threading
from datetime import datetime
from raspy.invalid_operation_exception import InvalidOperationException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.sensors.motion_sensor import MotionSensor
from raspy.components.sensors.motion_detected_event import MotionDetectedEvent
from raspy.io import pin_mode
from raspy.io import pin_state
from raspy.pi_system import core_utils


MOTION_DETECTED = pin_state.HIGH
"""The pin state to consider motion detected."""


class MotionSensorComponent(MotionSensor):
    """A component that is an abstraction of a motion sensor device."""

    def __init__(self, pin):
        """Initialize a new instance of MotionSensorComponet.

        :param raspy.io.gpio.Gpio pin: The input pin to check for motion on.
        :raises: ArgumentNullException if pin is None.
        """
        MotionSensor.__init__(self, pin)
        self.__isPolling = False
        self.__lastCheckDetected = False
        self.__stopEvent = threading.Event()
        self.__stopEvent.set()
        self.__pollThread = None

    @property
    def is_polling(self):
        """Check to see if this instance is currently polling.

        :returns: True if polling; Otherwise, False.
        :rtype: bool
        """
        return self.__isPolling

    @property
    def is_motion_detected(self):
        """Check to see if motion was detected.

        :returns: True if motion was detected.
        :rtype: bool
        """
        return self.pin.state == MOTION_DETECTED

    def interrupt_poll(self):
        """Interrupt the poll cycle."""
        if not self.__isPolling or self.is_disposed:
            return

        if self.__stopEvent.is_set() or self.__pollThread is None:
            return

        self.__stopEvent.set()
        self.__isPolling = False

    def dispose(self):
        """Release managed resources used by this component."""
        if self.is_disposed:
            return

        self.interrupt_poll()
        MotionSensor.dispose(self)

    def _execute_poll(self):
        """Execute the poll cycle."""
        while not self.__stopEvent.is_set():
            detected = self.is_motion_detected
            if detected != self.__lastCheckDetected:
                self.__lastCheckDetected = detected
                now = datetime.now()
                evt = MotionDetectedEvent(self.__lastCheckDetected, now)
                self.on_motion_state_changed(evt)
            core_utils.sleep(500)

    def poll(self):
        """Poll the input pin status every 500ms until stopped.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        :raises: raspy.invalid_operation_exception.InvalidOperationException
        if the underlying pin is not an input pin.
        """
        if self.is_disposed:
            raise ObjectDisposedException("MotionSensorComponent")

        if self.pin.mode != pin_mode.IN:
            msg = "The specified pin is not configured as an input pin, which"
            msg += " is required to read sensor data."
            raise InvalidOperationException(msg)

        self.__stopEvent.clear()
        self.__isPolling = True
        self.__pollThread = threading.Thread(target=self._execute_poll)
        self.__pollThread.name = "MotionSensorComponentPollThread"
        self.__pollThread.daemon = True
        self.__pollThread.start()
