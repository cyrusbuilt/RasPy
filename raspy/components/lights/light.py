"""This module contains the base type for lights."""


import threading
from pyee import EventEmitter
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.component import Component


EVENT_STATE_CHANGED = "lightStateChanged"
"""The event to fire when a state change occurs."""

EVENT_LEVEL_CHANGED = "lightLevelChanged"
"""The event to fire when a brightness change occurs."""


class Light(Component):
    """The base type for light component abstractions."""

    def __init__(self):
        """Initialize a new instance of Light."""
        Component.__init__(self)
        self.__emitter = EventEmitter()

    def on(self, evt, callback):
        """Register an event with a callback to handle it.

        :param str evt: The name of the event to register a handler for.
        :param function callback: The callback to execute when the event
        fires.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance is disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Light")

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
            raise ObjectDisposedException("Light")

        self.__emitter.emit(evt, args)

    def remove_all_listeners(self):
        """Remove all registered event listeners."""
        if self.is_disposed:
            return

        if self.__emitter is not None:
            self.__emitter.remove_all_listeners()

    @property
    def is_on(self):
        """Get a value indicating whether or not the light is on.

        :returns: True if the light is on.
        :rtype: bool
        """
        return False

    @property
    def is_off(self):
        """Get a value indicating whether or not the light is off.

        :returns: True if the light is off.
        :rtype: bool
        """
        return not self.is_on

    def turn_on(self):
        """Turn the light on.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        raise NotImplementedError("Method turn_on() not implemented.")

    def turn_off(self):
        """Turn the light off.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        raise NotImplementedError("Method turn_off() not implemented.")

    def on_light_state_changed(self, evt):
        """Fire the light state change event.

        :param raspy.components.lights.light_state_change_event.LightStateChangeEvent evt:
        The state change event object.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Light")

        _t = threading.Thread(target=self.emit,
                              name="stateChange",
                              args=(EVENT_STATE_CHANGED, evt))
        _t.daemon = True
        _t.start()

    def dispose(self):
        """Dispose managed resources."""
        if self.is_disposed:
            return

        if self.__emitter is not None:
            self.__emitter.remove_all_listeners()
            self.__emitter = None

        Component.dispose(self)
