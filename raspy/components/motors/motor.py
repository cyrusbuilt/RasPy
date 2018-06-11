"""This module contains the motor base type."""


import threading
from pyee import EventEmitter
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.component import Component
from raspy.components.motors import motor_state
from raspy.components.motors.motor_state_change_event import MotorStateChangeEvent


EVENT_STATE_CHANGED = "motorStateChanged"
"""The event that fires when the motor state changes."""

EVENT_STOPPED = "motorStopped"
"""The event that fires when the motor stops."""

EVENT_FORWARD = "motorForward"
"""The event that fires when the motor moves forward."""

EVENT_REVERSE = "motorReverse"
"""The event that fires when the motor moves in revers."""


class Motor(Component):
    """A motor abstraction base class."""

    def __init__(self):
        """Initialize a new instance of Motor."""
        Component.__init__(self)
        self.__emitter = EventEmitter()
        self.__state = motor_state.STOP

    def dispose(self):
        """Dispose managed resources."""
        if self.is_disposed:
            return

        self.__emitter.remove_all_listeners()
        self.__emitter = None
        Component.dispose(self)

    def remove_all_listeners(self):
        """Remove all registered event listeners."""
        if self.is_disposed:
            return

        if self.__emitter is not None:
            self.__emitter.remove_all_listeners()

    def on(self, evt, callback):
        """Register an event with a callback to handle it.

        :param str evt: The name of the event to register a handler for.
        :param function callback: The callback to execute when the event
        fires.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance is disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Motor")

        self.__emitter.on(evt, callback)

    def emit(self, evt, args=None):
        """Emit the specified event to all registered listeners.

        :param str evt: The name of the event to emit.
        :param object args: The arguments to pass to the event handlers
        (listeners).
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance is disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Motor")

        self.__emitter.emit(evt, args)

    def _fire_events(self, change_evt):
        """Fire motor state change events.

        :param raspy.components.motors.motor_state_change_event.MotorStateChangeEvent change_evt:
        The event info object.
        """
        self.emit(EVENT_STATE_CHANGED, change_evt)
        if change_evt.new_state == motor_state.STOP:
            self.emit(EVENT_STOPPED)
        elif change_evt.new_state == motor_state.FORWARD:
            self.emit(EVENT_FORWARD)
        elif change_evt.new_state == motor_state.REVERSE:
            self.emit(EVENT_REVERSE)

    def on_motor_state_change(self, change_evt):
        """Fire the motor state change event.

        :param raspy.components.motors.motor_state_change_event.MotorStateChangeEvent change_evt:
        The event info object.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Motor")

        _t = threading.Thread(target=self._fire_events,
                              name="motorStateChange",
                              args=[change_evt])
        _t.daemon = True
        _t.start()

    @property
    def state(self):
        """Get the motor state.

        :returns: The motor state.
        :rtype: int
        """
        return self.__state

    @state.setter
    def state(self, mot_state):
        """Set the motor state.

        :param int mot_state: The motor state.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Motor")
        self.__state = mot_state

    @property
    def is_stopped(self):
        """Get whether or not the motor is stopped.

        :returns: True if the motor is stopped.
        :rtype: bool
        """
        return self.is_state(motor_state.STOP)

    def forward(self, millis=0):
        """Tell the motor to move forward for the specified millis.

        :param int millis: The number of milliseconds to continue moving
        forward for. If zero or None, then moves forward continuously until
        stopped.
        """
        if self.state == motor_state.FORWARD:
            return

        old_state = self.state
        self.state = motor_state.FORWARD
        evt = MotorStateChangeEvent(old_state, motor_state.FORWARD)
        self.on_motor_state_change(evt)
        if millis > 0:
            _t = threading.Timer(millis / 1000, self.stop)
            _t.start()

    def reverse(self, millis=0):
        """Tell the motor to move in reverse for the specified millis.

        :param int millis: The number of milliseconds to continue moving in
        reverse for. If zero or None, then moves in reverse continuously until
        stopped.
        """
        if self.state == motor_state.REVERSE:
            return

        old_state = self.state
        self.state = motor_state.REVERSE
        evt = MotorStateChangeEvent(old_state, motor_state.REVERSE)
        self.on_motor_state_change(evt)
        if millis > 0:
            _t = threading.Timer(millis / 1000, self.stop)
            _t.start()

    def stop(self):
        """Stop the motor's movement."""
        if self.state == motor_state.STOP:
            return

        old_state = self.state
        self.state = motor_state.STOP
        evt = MotorStateChangeEvent(old_state, motor_state.STOP)
        self.on_motor_state_change(evt)

    def is_state(self, state):
        """Determine if motor is in the specified state.

        :param int state: The state to check for.
        :returns: True if the motor is in the specified state.
        :rtype: bool
        """
        return self.__state == state
