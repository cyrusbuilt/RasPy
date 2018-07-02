"""This module contains the OpenerDevice type."""


import threading
from raspy.argument_null_exception import ArgumentNullException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.devices.access import opener
from raspy.devices.access import opener_state
from raspy.devices.access.opener_lock_change_event import OpenerLockChangeEvent
from raspy.devices.access.opener_state_change_event import OpenerStateChangeEvent
from raspy.devices.access.opener_locked_exception import OpenerLockedException
from raspy.components.sensors import sensor_state
from raspy.components.switches import switch_state
from raspy.components.switches import switch


class OpenerDevice(opener.Opener):
    """A device abstraction of a door opener (ie. Garage Door Opener)."""

    def __init__(self, relay, sensor, open_state=sensor_state.CLOSED, lock=None):
        """Initialize a new instance of OpenerDevice.

        :param raspy.components.relays.Relay relay: The relay that controls
        the opener.
        :param raspy.components.sensors.sensor.Sensor sensor: The sensor
        monitoring the door state.
        :param int open_state: The sensor state that indicates door open.
        :param raspy.components.switches.switch_component.SwitchComponent lock:
        The switch that controls the lock (optional).
        :raises: ArgumentNullException if 'relay' or 'sensor' are None.
        """
        opener.Opener.__init__(self)
        if relay is None:
            raise ArgumentNullException("Param 'relay' cannot be None.")

        if sensor is None:
            raise ArgumentNullException("Param 'sensor' cannot be None.")

        self.__relay = relay
        self.__sensor = sensor
        self.__overrideLockState = switch_state.OFF
        self.__lockOverride = False
        self.__openState = open_state
        self.__lock = lock
        if self.__lock is not None:
            self.__lock.on(switch.EVENT_STATE_CHANGED,
                           lambda evt: self._handle_lock_state_change(evt))
            self.__lock.poll()

    def _handle_lock_state_change(self, evt):
        """Handle the lock state change.

        :param raspy.components.switches.switch_state_change_event.SwitchStateChangeEvent evt:
        The event object.
        """
        if not self.__lockOverride:
            is_on = evt.new_state == switch_state.ON
            evt = OpenerLockChangeEvent(is_on)
            self.on_lock_state_change(evt)

    @property
    def trigger_relay(self):
        """Get the relay being used to trigger the opener motor.

        :returns: The trigger relay.
        :rtype: raspy.components.relays.Relay
        """
        return self.__relay

    @property
    def state_sensor(self):
        """Get the sensor used to determine the opener's state.

        :returns: The state sensor.
        :rtype: raspy.components.sensors.sensor.Sensor
        """
        return self.__sensor

    @property
    def lock_switch(self):
        """Get the switch being used to lock the opener.

        :returns: The lock switch.
        :rtype: raspy.components.switches.switch_component.SwitchComponent
        """
        return self.__lock

    def _get_opener_state(self, sens_state):
        """Get the state of the opener base on sensor state.

        :param int sens_state: The sensor state.
        :returns: The opener state.
        :rtype: int
        """
        if self.__openState == sens_state:
            return opener_state.OPEN
        return opener_state.CLOSED

    def dispose(self):
        """Release managed resources used by this component."""
        if self.is_disposed:
            return

        if self.__relay is not None:
            self.__relay.dispose()
            self.__relay = None

        if self.__sensor is not None:
            self.__sensor.dispose()
            self.__sensor = None

        if self.__lock is not None:
            self.__lock.dispose()
            self.__lock = None

        self.__overrideLockState = switch_state.OFF
        self.__lockOverride = False
        self.__openState = sensor_state.CLOSED
        opener.Opener.dispose(self)

    @property
    def is_locked(self):
        """Get a flag indicating whether this opener is locked.

        :returns: True if locked; Otherwise, False.
        :rtype: bool
        """
        if self.__lockOverride:
            return self.__overrideLockState == switch_state.ON
        else:
            if self.__lock is None:
                return False
            return self.__lock.is_on

    @property
    def state(self):
        """Get the state of the opener.

        :returns: The opener state.
        :rtype: int
        """
        # TODO handle the case of is_opening and is_closing
        return self._get_opener_state(self.__sensor.state)

    def _do_open(self):
        """Perform the open operation."""
        if self.__sensor.state == self.__openState:
            evt = OpenerStateChangeEvent(opener_state.CLOSED, opener_state.OPEN)
            self.on_opener_state_change(evt)

    def open(self):
        """Instruct the device to open.

        :raises: ObjectDisposedException if this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("OpenerDevice")

        if self.is_locked:
            raise OpenerLockedException(self.device_name)

        if not self.__sensor.is_state(self.__openState):
            self.__relay.pulse()
            millis = 200 / 1000
            _t = threading.Timer(millis, self._do_open)
            _t.start()

    def _do_close(self):
        """Perform the close operation."""
        if self.__sensor.state != self.__openState:
            evt = OpenerStateChangeEvent(opener_state.OPEN, opener_state.CLOSED)
            self.on_opener_state_change(evt)

    def close(self):
        """Instruct the device to close.

        :raises: ObjectDisposedException if this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("OpenerDevice")

        if self.is_locked:
            raise OpenerLockedException(self.device_name)

        if self.__sensor.is_state(self.__openState):
            self.__relay.pulse()
            millis = 200 / 1000
            _t = threading.Timer(millis, self._do_close)
            _t.start()

    def override_lock(self, override_state):
        """Manually overrides the state of the lock.

        This can be used to force lock or force unlock the opener. This will
        cause this opener to ignore the state of the lock (if specified) and
        only read the specified lock state.

        :param int override_state: The state to override with.
        """
        self.__overrideLockState = override_state
        self.__lockOverride = True

    def disable_override(self):
        """Disable the lock override.

        This will cause this opener to resume reading the actual state of the
        lock (if specified).
        """
        self.__lockOverride = False
