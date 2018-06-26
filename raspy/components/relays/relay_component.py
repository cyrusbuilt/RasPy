"""This module contains the RelayComponent type."""


from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.relays import relay
from raspy.components.relays import relay_state
from raspy.components.relays.relay_state_change_event import RelayStateChangeEvent
from raspy.io import pin_state


class RelayComponent(relay.Relay):
    """A component that is an abstraction of a relay device."""

    def __init__(self, pin):
        """Initialize a new instance of RelayComponent.

        :param raspy.io.gpio.Gpio pin: The output pin being used to control
        the relay.
        :raises: ArgumentNullException if pin param is None.
        """
        relay.Relay.__init__(self, pin)

    @property
    def state(self):
        """Get the relay state.

        :returns: The relay state.
        :rtype: int
        """
        if self.pin.state == relay.OPEN_STATE:
            return relay_state.OPEN
        return relay_state.CLOSED

    @state.setter
    def state(self, rel_state):
        """Set the relay state.

        :param int rel_state: The relay state to set.
        :raises: ObjectDisposedException if this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Relay")

        old_state = self.state
        if old_state != rel_state:
            if rel_state == relay_state.OPEN:
                if not self.is_open:
                    self.pin.write(pin_state.LOW)
                    relay.Relay.state.fset(self, rel_state)
            elif rel_state == relay_state.CLOSED:
                if not self.is_closed:
                    self.pin.write(pin_state.HIGH)
                    relay.Relay.state.fset(self, rel_state)
            else:
                pass

        evt = RelayStateChangeEvent(old_state, rel_state)
        self.on_relay_state_changed(evt)

    def pulse(self, millis=0):
        """Pulse the relay on for the specified number of milliseconds.

        :param int millis: The number of milliseconds to wait before switching
        back off. If not specified or invalid, then pulses for
        DEFAULT_PULSE_MILLISECONDS.
        """
        if millis is None or millis <= 0:
            millis = relay.DEFAULT_PULSE_MILLISECONDS

        self.on_pulse_start()
        self.close()
        self.pin.pulse(millis)
        self.open()
        self.on_pulse_stop()

    def is_state(self, rel_state):
        """Check to see if the relay is in the specified state.

        :param int rel_state: The state to check.
        :returns: True if in the specified state.
        :rtype: bool
        """
        return self.state == rel_state
