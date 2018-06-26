"""This module contains the Relay base type."""


import threading
from pyee import EventEmitter
from raspy.argument_null_exception import ArgumentNullException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.component import Component
from raspy.components.relays import relay_state
from raspy.io import pin_state


EVENT_STATE_CHANGED = "relayStateChanged"
"""The name of the relay state change event."""

EVENT_PULSE_START = "relayPulseStart"
"""The name of the relay pulse start event."""

EVENT_PULSE_STOP = "relayPulseStop"
"""The name of the relay pulse stop event."""

OPEN_STATE = pin_state.LOW
"""The pin state when the relay is open."""

CLOSED_STATE = pin_state.HIGH
"""The pin state when the relay is closed."""

DEFAULT_PULSE_MILLISECONDS = 200
"""The default pulse time (200 ms)."""


class Relay(Component):
    """A relay component abstraction interface/base."""

    def __init__(self, pin):
        """Initialize a new instance of Relay.

        :param raspy.io.gpio.Gpio pin: The output pin being used to control
        the relay.
        :raises: ArgumentNullException if pin param is None.
        """
        Component.__init__(self)
        if pin is None:
            raise ArgumentNullException("'pin' param cannot be None.")

        self.__emitter = EventEmitter()
        self.__state = relay_state.OPEN
        self.__pin = pin
        self.__pin.provision()

    def dispose(self):
        """Release managed resources used by this component."""
        if self.is_disposed:
            return

        if self.__pin is not None:
            self.__pin.dispose()
            self.__pin = None

        self.__state = relay_state.OPEN
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
            raise ObjectDisposedException("Relay")

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
            raise ObjectDisposedException("Relay")

        self.__emitter.emit(evt, args)

    def remove_all_listeners(self):
        """Remove all registered event listeners."""
        if self.is_disposed:
            return

        if self.__emitter is not None:
            self.__emitter.remove_all_listeners()

    def on_relay_state_changed(self, change_evt):
        """Fire the relay state change event.

        :param raspy.components.relays.relay_state_change_event.RelayStateChangeEvent change_evt:
        The state change event info.
        :raises: ObjectDisposedException if this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Relay")

        _t = threading.Thread(target=self.emit,
                              name=EVENT_STATE_CHANGED,
                              args=(EVENT_STATE_CHANGED, change_evt))
        _t.daemon = True
        _t.start()

    def on_pulse_start(self):
        """Fire the pulse start event.

        :raises: ObjectDisposedException if this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Relay")

        _t = threading.Thread(target=self.emit,
                              name=EVENT_PULSE_START,
                              args=[EVENT_PULSE_START])
        _t.daemon = True
        _t.start()

    def on_pulse_stop(self):
        """Fire the pulse stop event.

        :raises: ObjectDisposedException if this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Relay")

        _t = threading.Thread(target=self.emit,
                              name=EVENT_PULSE_STOP,
                              args=[EVENT_PULSE_STOP])
        _t.daemon = True
        _t.start()

    @property
    def state(self):
        """Get the relay state.

        :returns: The relay state.
        :rtype: int
        """
        return self.__state

    @state.setter
    def state(self, rel_state):
        """Set the relay state.

        :param int rel_state: The relay state to set.
        :raises: ObjectDisposedException if this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Relay")

        self.__state = rel_state

    @property
    def is_open(self):
        """Check to see if the relay is in an open state.

        :returns: True if in an open state; Otherwise, False.
        :rtype: bool
        """
        return self.state == relay_state.OPEN

    @property
    def is_closed(self):
        """Check to see if the relay is in a closed state.

        :returns: True if closed; Otherwise, False.
        :rtype: bool
        """
        return self.state == relay_state.CLOSED

    @property
    def pin(self):
        """Get the pin being used to drive the relay.

        :returns: The underlying physical pin.
        :rtype: raspy.io.gpio.Gpio
        """
        return self.__pin

    def open(self):
        """Open (deactivate) the relay."""
        self.state = relay_state.OPEN

    def close(self):
        """Close (activate) the relay."""
        self.state = relay_state.CLOSED

    def toggle(self):
        """Toggle the relay (switch on, then off)."""
        if self.is_open:
            self.close()
        else:
            self.open()

    def pulse(self, millis=0):
        """Pulse the relay on for the specified number of milliseconds.

        :param int millis: The number of milliseconds to wait before switching
        back off. If not specified or invalid, then pulses for
        DEFAULT_PULSE_MILLISECONDS.
        """
        self.on_pulse_start()
        self.close()
        self.__pin.pulse(millis)
        self.open()
        self.on_pulse_stop()
