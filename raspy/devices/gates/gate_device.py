"""This module contains the GarageDevice type."""


from raspy.devices.access.opener_device import OpenerDevice
from raspy.devices.gates.gate import Gate


class GateDevice(Gate):
    """A garage door opener device abstraction."""

    def __init__(self, relay, door_sensor, open_state, lock):
        """Initialize a new instance of GarageDoorOpenerDevice.

        :param raspy.components.relays.Relay relay: The relay that controls
        the opener.
        :param raspy.components.sensors.sensor.Sensor sensor: The sensor
        monitoring the door state.
        :param int open_state: The sensor state that indicates door open.
        :param raspy.components.switches.switch_component.SwitchComponent lock:
        The switch that controls the lock (optional).
        :raises: ArgumentNullException if 'relay' or 'sensor' are None.
        """
        Gate.__init__(self)
        self.__base = OpenerDevice(relay, door_sensor, open_state, lock)

    @property
    def trigger_relay(self):
        """Get the relay being used to trigger the opener motor.

        :returns: The trigger relay.
        :rtype: raspy.components.relays.Relay
        """
        return self.__base.trigger_relay

    @property
    def state_sensor(self):
        """Get the sensor used to determine the opener's state.

        :returns: The state sensor.
        :rtype: raspy.components.sensors.sensor.Sensor
        """
        return self.__base.state_sensor

    @property
    def lock_switch(self):
        """Get the switch being used to lock the opener.

        :returns: The lock switch.
        :rtype: raspy.components.switches.switch_component.SwitchComponent
        """
        return self.__base.lock_switch

    @property
    def is_locked(self):
        """Get a flag indicating whether this opener is locked.

        :returns: True if locked; Otherwise, False.
        :rtype: bool
        """
        return self.__base.is_locked

    @property
    def state(self):
        """Get the state of the opener.

        :returns: The opener state.
        :rtype: int
        """
        # TODO handle the case of is_opening and is_closing
        return self.__base.state

    @property
    def is_open(self):
        """Get a flag indicating whether the opener is open.

        :returns: True if open; Otherwise, False.
        :rtype: bool
        """
        return self.__base.is_open

    @property
    def is_opening(self):
        """Get a flag indicating if in the process of opening.

        :returns: True if opening; Otherwise, False.
        :rtype: bool
        """
        return self.__base.is_opening

    @property
    def is_closed(self):
        """Get a flag indicating whether this opener is closed.

        :returns: True if closed; Otherwise, False.
        :rtype: bool
        """
        return self.__base.is_closed

    @property
    def is_closing(self):
        """Get a flag indicating if in the process of closing.

        :returns: True if closing; Otherwise, False.
        :rtype: bool
        """
        return self.__base.is_closing

    def open(self):
        """Instruct the device to open.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        self.__base.open()

    def close(self):
        """Instruct the device to close.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        self.__base.close()

    def override_lock(self, override_state):
        """Manually overrides the state of the lock.

        This can be used to force lock or force unlock the opener. This will
        cause this opener to ignore the state of the lock (if specified) and
        only read the specified lock state.

        :param int override_state: The state to override with.
        """
        self.__base.override_lock(override_state)

    def disable_override(self):
        """Disable the lock override.

        This will cause this opener to resume reading the actual state of the
        lock (if specified).
        """
        self.__base.disable_override()
