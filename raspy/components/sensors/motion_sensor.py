"""This module contains the MotionSensor type."""


import threading
from datetime import datetime
from pyee import EventEmitter
from raspy.argument_null_exception import ArgumentNullException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.component import Component


EVENT_MOTION_STATE_CHANGED = "motionStateChanged"
"""The name of the motion state changed event."""


class MotionSensor(Component):
    """A motion sensor abstraction component interface."""

    def __init__(self, pin):
        """Initialize a new instance of MotionSensor.

        :param raspy.io.gpio.Gpio pin: The input pin to check for motion on.
        :raises: ArgumentNullException if pin is None.
        """
        Component.__init__(self)
        if pin is None:
            raise ArgumentNullException("'pin' param cannot be None.")

        self.__emitter = EventEmitter()
        self.__lastMotion = None
        self.__lastInactive = None
        self.__pin = pin
        self.__pin.provision()

    def dispose(self):
        """Release managed resources used by this component."""
        if self.is_disposed:
            return

        if self.__pin is not None:
            self.__pin.dispose()
            self.__pin = None

        self.__lastMotion = None
        self.__lastInactive = None
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
            raise ObjectDisposedException("MotionSensor")

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
            raise ObjectDisposedException("MotionSensor")

        self.__emitter.emit(evt, args)

    def remove_all_listeners(self):
        """Remove all registered event listeners."""
        if self.is_disposed:
            return

        if self.__emitter is not None:
            self.__emitter.remove_all_listeners()

    def on_motion_state_changed(self, motion_evt):
        """Fire the motion state changed event.

        :param raspy.components.sensors.motion_detected_event.MotionDetectedEvent motion_evt:
        The motion detected event object.
        :raises: ObjectDisposedException if this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("MotionSensor")

        if motion_evt.is_motion_detected:
            self.__lastMotion = datetime.now()
        else:
            self.__lastInactive = datetime.now()

        _t = threading.Thread(target=self.emit,
                              name=EVENT_MOTION_STATE_CHANGED,
                              args=(EVENT_MOTION_STATE_CHANGED, motion_evt))
        _t.daemon = True
        _t.start()

    @property
    def last_motion_timestamp(self):
        """Get the timestamp of the last time motion was detected.

        :returns: The timestamp of when motion was detected.
        :rtype: datetime.datetime
        """
        return self.__lastMotion

    @property
    def last_inactivity_timestamp(self):
        """The last inactivity timestamp.

        :returns: The timestamp of the last time the sensor went idle.
        :rtype: datetime.datetime
        """
        return self.__lastInactive

    @property
    def pin(self):
        """Get the pin being used to sample sensor data.

        :returns: The underlying physical pin.
        :rtype: raspy.io.gpio.Gpio
        """
        return self.__pin

    @property
    def is_motion_detected(self):
        """Check to see if motion was detected.

        :returns: True if motion was detected.
        :rtype: bool
        """
        return False
