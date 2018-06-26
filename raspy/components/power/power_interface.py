"""This module contains the PowerInterface type."""


import threading
from pyee import EventEmitter
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.component import Component
from raspy.components.power import power_state


EVENT_STATE_CHANGED = "powerStateChanged"
"""The name of the state change event."""


class PowerInterface(Component):
    """An interface base type for power components."""

    def __init__(self):
        """Initialize a new instance of PowerInterface."""
        Component.__init__(self)
        self.__emitter = EventEmitter()
        self.__state = power_state.OFF

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

    def on_power_state_changed(self, event_info):
        """Fire the power state change event.

        :param raspy.components.power.power_state_change_event.PowerStateChangeEvent event_info:
        The event info object.
        """
        if self.is_disposed:
            raise ObjectDisposedException("PowerInterface")

        _t = threading.Thread(target=self.emit,
                              name=EVENT_STATE_CHANGED,
                              args=(EVENT_STATE_CHANGED, event_info))
        _t.daemon = True
        _t.start()

    @property
    def state(self):
        """Get the state of the power component.

        :returns: The state of the power component.
        :rtype: int
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        :raises: raspy.io.invalid_pin_mode_exception.InvalidPinModeException if
        the pin being used to control this device is not configure as an
        output.
        """
        return power_state.UNKNOWN

    @state.setter
    def state(self, pwr_state):
        """Set the state of the power component.

        :param int pwr_state: The state to set.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        :raises: raspy.io.invalid_pin_mode_exception.InvalidPinModeException if
        the pin being used to control this device is not configure as an
        output.
        :raises: raspy.invalid_operation_exception.InvalidOperationException if
        an invalid state is specified.
        """
        pass

    @property
    def is_on(self):
        """Check to see if the device is on.

        :returns: True if the device is on.
        :rtype: bool
        """
        return self.state == power_state.ON

    @property
    def is_off(self):
        """Check to see if the device is off.

        :returns: True if the device is off.
        :rtype: bool
        """
        return self.state == power_state.OFF

    def turn_on(self):
        """Turn the device on."""
        self.state = power_state.ON

    def turn_off(self):
        """Turn the device off."""
        self.state = power_state.OFF
