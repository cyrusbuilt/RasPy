"""This module contains the Fireplace type."""


import datetime
import threading
from pyee import EventEmitter
from raspy.invalid_operation_exception import InvalidOperationException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.devices.device import Device
from raspy.devices.fireplaces import fireplace_state
from raspy.devices.fireplaces.fireplace_timeout_event import FireplaceTimeoutEvent
from raspy.pi_system import time_unit


EVENT_STATE_CHANGED = "fireplaceStateChangeEvent"
"""The name of the state change event."""

EVENT_PILOT_LIGHT_STATE_CHANGED = "fireplacePilotStateChangeEvent"
"""The name of the pilot light state change event."""

EVENT_OPERATION_TIMEOUT = "fireplaceOperationTimeout"
"""The name of the operation timeout event."""


class Fireplace(Device):
    """Fireplace device abstraction interface/base type."""

    def __init__(self):
        """Initialize a new instance of Fireplace."""
        Device.__init__(self)
        self.__emitter = EventEmitter()
        self.__timeoutDelay = 0
        self.__timeoutDelayMillis = 0
        self.__timeoutUnit = time_unit.MINUTES
        self.__taskTimer = None
        self.__killTimer = None
        self.__state = fireplace_state.OFF
        self.__emitter.on(EVENT_STATE_CHANGED,
                          lambda evt: self._internal_state_changed(evt))

    def _cancel_timeout_task(self):
        """Cancel the timeout task (if running)."""
        if self.__taskTimer is not None:
            self.__taskTimer.cancel()
            self.__taskTimer = None

    def _internal_state_changed(self, evt):
        """An internal handler for the state change event.

        :param raspy.devices.fireplaces.fireplace_state_change_event.FireplaceStateChangeEvent evt:
        The event object.
        """
        if evt:
            pass
        self._cancel_timeout_task()

    def on(self, evt, callback):
        """Register an event with a callback to handle it.

        :param str evt: The name of the event to register a handler for.
        :param function callback: The callback to execute when the event
        fires.
        :raises: ObjectDisposedException if this instance is disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Fireplace")

        self.__emitter.on(evt, callback)

    def emit(self, evt, args):
        """Emit the specified event to all registered listeners.

        :param str evt: The name of the event to emit.
        :param object args: The arguments to pass to the event handlers
        (listeners).
        :raises: ObjectDisposedException if this instance is disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Fireplace")

        self.__emitter.emit(evt, args)

    def remove_all_listeners(self):
        """Remove all registered event listeners."""
        if self.is_disposed:
            return

        if self.__emitter is not None:
            self.__emitter.remove_all_listeners()

    def on_state_change(self, evt):
        """Fire the state change event.

        :param raspy.devices.fireplaces.fireplace_state_change_event.FireplaceStateChangeEvent evt:
        The event object.
        :raises: ObjectDisposedException if this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Fireplace")

        _t = threading.Thread(target=self.emit,
                              name=EVENT_STATE_CHANGED,
                              args=(EVENT_STATE_CHANGED, evt))
        _t.daemon = True
        _t.start()

    def on_operation_timeout(self, evt):
        """Fire the operation timeout event.

        :param raspy.devices.fireplaces.fireplace_timeout_event.FireplaceTimeoutEvent evt:
        The event object.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Fireplace")

        _t = threading.Thread(target=self.emit,
                              name=EVENT_OPERATION_TIMEOUT,
                              args=(EVENT_OPERATION_TIMEOUT, evt))
        _t.daemon = True
        _t.start()

    def on_pilot_light_state_change(self, evt):
        """Fire the pilot light state change event.

        :param raspy.devices.fireplaces.fireplace_pilot_light_event.FireplacePilotLightEvent evt:
        The event object.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Fireplace")

        _t = threading.Thread(target=self.emit,
                              name=EVENT_PILOT_LIGHT_STATE_CHANGED,
                              args=(EVENT_PILOT_LIGHT_STATE_CHANGED, evt))
        _t.daemon = True
        _t.start()

    @property
    def state(self):
        """Get the fireplace state.

        :returns: The fireplace state.
        :rtype: int
        """
        return self.__state

    @state.setter
    def state(self, the_state):
        """Set the fireplace state.

        :param int the_state: The fireplace state.
        :raises: .fireplace_pilot_light_exception.FireplacePilotLightException if
        no pilot light sensor is present.
        """
        self.__state = the_state

    @property
    def is_on(self):
        """Get a flag indicating whether the fireplace is on.

        :returns: True if the fireplace is on.
        :rtype: bool
        """
        return self.state == fireplace_state.ON

    @property
    def is_off(self):
        """Get a flag indicating whether the fireplace is off.

        :returns: True if the fireplace is off.
        :rtype: bool
        """
        return self.state == fireplace_state.OFF

    @property
    def is_pilot_light_on(self):
        """Get a flag indicating whether the pilot light is on.

        :returns: True if the pilot light is on.
        :rtype: bool
        """
        return False

    @property
    def is_pilot_light_off(self):
        """Get a flag indicating whether the pilot light is off.

        :returns: True if the pilot light is off.
        :rtype: bool
        """
        return False

    def get_timeout_delay(self):
        """Get the timeout delay.

        :returns: The timeout delay.
        :type: int
        """
        return self.__timeoutDelay

    def get_timeout_unit(self):
        """Get the timeout unit of time.

        :returns: The time unit being used for the timeout delay.
        :rtype: int
        """
        return self.__timeoutUnit

    def set_timeout_delay(self, delay, unit):
        """Get the timeout delay.

        :param int delay: The timeout delay.
        :param int unit: The time unit of measure for the timeout.
        :raises: raspy.invalid_operation_exception.InvalidOperationException if
        the fireplace is turned off.
        """
        if self.is_off:
            msg = "Cannot set timeout when the fireplace is off."
            raise InvalidOperationException(msg)

        self.__timeoutDelay = delay
        self.__timeoutUnit = unit
        self.cancel_timeout()
        if self.__timeoutDelay > 0:
            wait_time = datetime.timedelta()
            if unit == time_unit.DAYS:
                wait_time = datetime.timedelta(days=delay)
            elif unit == time_unit.HOURS:
                wait_time = datetime.timedelta(hours=delay)
            elif unit == time_unit.MINUTES:
                wait_time = datetime.timedelta(minutes=delay)
            elif unit == time_unit.SECONDS:
                wait_time = datetime.timedelta(seconds=delay)
            elif unit == time_unit.MILLISECONDS:
                wait_time = datetime.timedelta(milliseconds=delay)

            kill_delay = datetime.timedelta(milliseconds=wait_time.total_seconds())
            kill_delay += datetime.timedelta(seconds=1)
            sec = kill_delay.total_seconds()
            self.__killTimer = threading.Timer(sec, self._cancel_timeout_task)
            self.__killTimer.start()
            self._start_cancel_task()

    def turn_on(self, timeout_delay, timeout_unit):
        """Turn the fireplace on with the specified timeout.

        If the operation is not successful within the allotted time, the
        operation is cancelled for safety reasons.

        :param int timeout_delay: The timeout delay. If not specified or
        less than or equal to zero, then the fireplace is turned on without
        any safety delay (not recommended).
        :param int timeout_unit: The time unit of measure for the timeout. If
        not specified, `time_unit.SECONDS` is assumed.
        """
        self.state = fireplace_state.ON
        if timeout_unit is None:
            timeout_unit = self.__timeoutUnit

        if timeout_delay is not None:
            if timeout_delay > 0:
                self.set_timeout_delay(timeout_delay, timeout_unit)

    def turn_off(self):
        """Turn the fireplace off."""
        self.state = fireplace_state.OFF

    def _task_action(self):
        """The action for the background timeout task.

        This fires the operation timeout event, then turns off the fireplace.
        """
        evt = FireplaceTimeoutEvent()
        self.on_operation_timeout(evt)
        if not evt.is_handled:
            self.turn_off()

    def _do_task(self):
        self._task_action()
        self.__killTimer.cancel()
        self.__killTimer = None

    def _start_cancel_task(self):
        """Start the background cancellation task."""
        if self.__killTimer is not None:
            self.__taskTimer = threading.Timer(self.__timeoutDelayMillis, self._do_task)
            self.__taskTimer.start()

    def cancel_timeout(self):
        """Cancel the timeout."""
        self._cancel_timeout_task()

    def shutdown(self):
        """Shutdown the fireplace."""
        self.cancel_timeout()
        self.turn_off()

    def dispose(self):
        """Release all managed resources used by this component."""
        if self.is_disposed:
            return

        self._cancel_timeout_task()
        if self.__killTimer is not None:
            self.__killTimer.cancel()
            self.__killTimer = None

        self.__emitter.remove_all_listeners()
        self.__emitter = None
        self.__state = fireplace_state.OFF
        self.__timeoutDelay = 0
        self.__timeoutDelayMillis = 0
        Device.dispose(self)
