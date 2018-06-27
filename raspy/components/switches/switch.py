"""This module contains the Switch type."""


import threading
from pyee import EventEmitter
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.component import Component
from raspy.components.switches import switch_state


EVENT_STATE_CHANGED = "switchStateChanged"
"""The name of the switch state changed event."""


class Switch(Component):
    """An interface/base type for switch device abstractions."""

    def __init__(self):
        """Initialize a new instance of Switch."""
        Component.__init__(self)
        self.__emitter = EventEmitter()
        self.__state = switch_state.OFF

    def dispose(self):
        """Release managed resources used by this component."""
        if self.is_disposed:
            return

        self.__state = switch_state.OFF
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
            raise ObjectDisposedException("Switch")

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
            raise ObjectDisposedException("Switch")

        self.__emitter.emit(evt, args)

    def remove_all_listeners(self):
        """Remove all registered event listeners."""
        if self.is_disposed:
            return

        if self.__emitter is not None:
            self.__emitter.remove_all_listeners()

    def on_switch_state_changed(self, evt):
        """Fire the switch state change event.

        :param: raspy.components.switches.switch_state_change_event.SwitchStateChangeEvent evt:
        The event info object.
        :raises: ObjectDisposedException if this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Switch")

        _t = threading.Thread(target=self.emit,
                              name=EVENT_STATE_CHANGED,
                              args=(EVENT_STATE_CHANGED, evt))
        _t.daemon = True
        _t.start()

    @property
    def state(self):
        """Get the state of the switch.

        :returns: The switch state.
        :rtype: int
        """
        return self.__state

    def is_state(self, sw_state):
        """Get the state of the switch.

        :param int sw_state: The state to check.
        :returns: The switch state.
        :rtype: int
        """
        return self.state == sw_state

    @property
    def is_on(self):
        """Get whether or not this switch is in the on position.

        :returns: True if on; Otherwise, False.
        :rtype: bool
        """
        return self.is_state(switch_state.ON)

    @property
    def is_off(self):
        """Get whether or not this switch is in the off position.

        :returns: True if off; Otherwise, False.
        :rtype: bool
        """
        return self.is_state(switch_state.OFF)

    @property
    def pin(self):
        """Get the underlying physical pin.

        :returns: The pin.
        :rtype: raspy.io.gpio.Gpio
        """
        return None
