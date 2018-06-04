"""This module contains the base type for all buttons."""


from threading import Timer
from pyee import EventEmitter
from raspy import string_utils
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.component import Component
from raspy.components.buttons import button_state
from raspy.components.buttons.button_event import ButtonEvent


EVENT_STATE_CHANGED = "stateChanged"
"""The name of the state changed event."""

EVENT_PRESSED = "buttonPressed"
"""The name of the buttons press event."""

EVENT_RELEASED = "buttonReleased"
"""The name of the buttons released event."""

EVENT_HOLD = "buttonHold"
"""The name of the buttons hold event."""


class Button(Component):
    """A buttons device abstraction component base class."""

    def __init__(self):
        """Initialize a new Button."""
        super(Component, self).__init__()
        self.__holdTimer = None
        self.__baseState = button_state.RELEASED
        self.__emitter = EventEmitter()

    @property
    def is_pressed(self):
        """Get a value indicating whether or not the buttons is pressed.

        :returns: True if the buttons is pressed; Otherwise, False.
        :rtype: bool
        """
        return self.__baseState == button_state.PRESSED

    @property
    def is_released(self):
        """Get a value indicating whether or not the buttons is released.

        :returns: True if the buttons is released; Otherwise, False.
        :rtype: bool
        """
        return self.__baseState == button_state.RELEASED

    def _set_state(self, state):
        """Override state with the specified state.

        :param int state: The state to set.
        """
        self.__baseState = state

    @property
    def state(self):
        """Get the buttons state.

        :returns: The buttons state.
        :rtype: int
        """
        return self.__baseState

    def is_state(self, state):
        """Check to see if the buttons is in the specified state.

        :param int state: The state to check.
        :returns: True if the buttons is in the specified state.
        :rtype: bool
        """
        return self.__baseState == state

    def on(self, evt, callback):
        """Register an event with a callback to handle it.

        :param str evt: The name of the event to register a handler for.
        :param function callback: The callback to execute when the event
        fires.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance is disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Button")

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
            raise ObjectDisposedException("Button")

        self.__emitter.emit(evt, args)

    def on_button_hold(self, btn_event):
        """Fire the buttons hold event.

        :param raspy.components.buttons.button_event.ButtonEvent btn_event: The
        buttons event info.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Button")

        self.emit(EVENT_HOLD, btn_event)

    def _on_hold_timer_elapsed(self, btn_event):
        """Handle the timer elapsed event.

        This internal method fires the button hold event when the hold timer
        elapses. Should only be called by _fire_button_hold_event().

        :param raspy.components.buttons.button_event.ButtonEvent btn_event: The
        button event info.
        """
        if self.is_pressed:
            self.on_button_hold(btn_event)

    def _stop_hold_timer(self):
        """Stop the internal hold timer."""
        if self.__holdTimer is not None:
            self.__holdTimer.cancel()

        self.__holdTimer = None

    def _fire_button_hold_event(self):
        """Fire the timer elapsed event handler."""
        evt = ButtonEvent(self)
        self._on_hold_timer_elapsed(evt)

    def _start_hold_timer(self):
        """Start the button hold timer."""
        self.__holdTimer = Timer(2.0, self._fire_button_hold_event)
        self.__holdTimer.start()

    def on_state_changed(self, btn_event):
        """Fire the buttons state changed event.

        :param raspy.components.buttons.button_event.ButtonEvent btn_event: The
        buttons event info.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Button")

        self.emit(EVENT_STATE_CHANGED, btn_event)
        if btn_event.is_pressed:
            self.on_button_pressed(btn_event)

        if btn_event.is_released:
            self.on_button_released(btn_event)

    def on_button_pressed(self, btn_event):
        """Fire the buttons pressed event.

        :param raspy.components.buttons.button_event.ButtonEvent btn_event: The
        buttons event info.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Button")

        self.emit(EVENT_PRESSED, btn_event)
        self._stop_hold_timer()
        self._start_hold_timer()

    def on_button_released(self, btn_event):
        """Fire the buttons released event.

        :param raspy.components.buttons.button_event.ButtonEvent btn_event: The
        buttons event info.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Button")

        self.emit(EVENT_RELEASED, btn_event)
        self._stop_hold_timer()

    def __str__(self):
        """Return the string representation of this class instance.

        :returns: The string representation of this class.
        :rtype: str
        """
        base = Component.component_name.fget()
        if not string_utils.is_null_or_empty(base):
            return base
        return self.__class__.__name__

    def dispose(self):
        """Dispose of all the managed resources used by this instance."""
        if self.is_disposed:
            return

        self.__emitter.remove_all_listeners()
        self._stop_hold_timer()
        self.__emitter = None
        Component.dispose(self)
