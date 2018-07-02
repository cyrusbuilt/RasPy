"""This module contains the Opener type."""


import threading
from pyee import EventEmitter
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.devices.device import Device
from raspy.devices.access import opener_state


EVENT_STATE_CHANGED = "openerStateChangedEvent"
"""The name of the opener state change event."""

EVENT_LOCK_STATE_CHANGED = "lockStateChangedEvent"
"""The name of the opener lock state change event."""


class Opener(Device):
    """Opener device abstraction interface."""

    def __init__(self):
        """Initialize a new instance of Opener."""
        Device.__init__(self)
        self.__emitter = EventEmitter()
        self.__state = opener_state.CLOSED

    def on(self, evt, callback):
        """Register an event with a callback to handle it.

        :param str evt: The name of the event to register a handler for.
        :param function callback: The callback to execute when the event
        fires.
        :raises: ObjectDisposedException if this instance is disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Opener")

        self.__emitter.on(evt, callback)

    def emit(self, evt, args):
        """Emit the specified event to all registered listeners.

        :param str evt: The name of the event to emit.
        :param object args: The arguments to pass to the event handlers
        (listeners).
        :raises: ObjectDisposedException if this instance is disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Opener")

        self.__emitter.emit(evt, args)

    def remove_all_listeners(self):
        """Remove all registered event listeners."""
        if self.is_disposed:
            return

        if self.__emitter is not None:
            self.__emitter.remove_all_listeners()

    def on_opener_state_change(self, change_evt):
        """Fire the opener state change event.

        :param raspy.devices.access.opener_state_change_event.OpenerStateChangeEvent change_evt:
        The event object.
        :raises: ObjectDisposedException if this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Opener")

        _t = threading.Thread(target=self.emit,
                              name=EVENT_STATE_CHANGED,
                              args=(EVENT_STATE_CHANGED, change_evt))
        _t.daemon = True
        _t.start()

    def on_lock_state_change(self, change_evt):
        """Fire the lock state change event.

        :param raspy.devices.access.opener_lock_change_event.OpenerLockChangeEvent change_evt:
        The event object.
        :raises: ObjectDisposedException if this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Opener")

        _t = threading.Thread(target=self.emit,
                              name=EVENT_LOCK_STATE_CHANGED,
                              args=(EVENT_LOCK_STATE_CHANGED, change_evt))
        _t.daemon = True
        _t.start()

    @property
    def state(self):
        """Get the state of the opener.

        :returns: The opener state.
        :rtype: int
        """
        return self.__state

    @property
    def is_open(self):
        """Get a flag indicating whether the opener is open.

        :returns: True if open; Otherwise, False.
        :rtype: bool
        """
        return self.state == opener_state.OPEN

    @property
    def is_opening(self):
        """Get a flag indicating if in the process of opening.

        :returns: True if opening; Otherwise, False.
        :rtype: bool
        """
        return self.state == opener_state.OPENING

    @property
    def is_closed(self):
        """Get a flag indicating whether this opener is closed.

        :returns: True if closed; Otherwise, False.
        :rtype: bool
        """
        return self.state == opener_state.CLOSED

    @property
    def is_closing(self):
        """Get a flag indicating if in the process of closing.

        :returns: True if closing; Otherwise, False.
        :rtype: bool
        """
        return self.state == opener_state.CLOSING

    @property
    def is_locked(self):
        """Get a flag indicating whether this opener is locked.

        :returns: True if locked; Otherwise, False.
        :rtype: bool
        """
        return False

    def open(self):
        """Instruct the device to open.

        :raises: ObjectDisposedException if this instance has been disposed.
        """
        raise NotImplementedError("Method 'open()' not implemented.")

    def close(self):
        """Instruct the device to close.

        :raises: ObjectDisposedException if this instance has been disposed.
        """
        raise NotImplementedError("Method 'close()' not implemented.")

    def dispose(self):
        """Release managed resources used by this component."""
        if self.is_disposed:
            return

        self.__emitter.remove_all_listeners()
        self.__emitter = None
        self.__state = opener_state.CLOSED
        Device.dispose(self)
