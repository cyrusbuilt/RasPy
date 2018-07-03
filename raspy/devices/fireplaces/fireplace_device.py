"""This module contains the FireplaceDevice type."""


from raspy.argument_null_exception import ArgumentNullException
from raspy.devices.fireplaces import fireplace_state
from raspy.devices.fireplaces.fireplace import Fireplace
from raspy.devices.fireplaces.fireplace_light_exception import FireplaceLightException
from raspy.devices.fireplaces.fireplace_state_change_event import FireplaceStateChangeEvent
from raspy.devices.fireplaces.fireplace_pilot_light_event import FireplacePilotLightEvent
from raspy.components.relays import relay
from raspy.components.relays import relay_state
from raspy.components.sensors import sensor
from raspy.components.sensors import sensor_state


class FireplaceDevice(Fireplace):
    """A device that is an abstraction of a gas fireplace."""

    def __init__(self, control_relay, on_relay_state=relay_state.CLOSED,
                 pilot_sensor=None, pilot_state=sensor_state.CLOSED):
        """Initialize a new instance of FireplaceDevice.

        :param raspy.components.relays.relay.Relay control_relay: The control
        relay.
        :param int on_relay_state: The relay state used to consider the
        fireplace to be "on".
        :param raspy.components.sensors.sensor.Sensor pilot_sensor: The pilot
        light sensor (optional).
        :param int pilot_state: The pilot light state used to consider the
        pilot light to be "on".
        :raises: ArgumentNullException if control_relay is None.
        """
        Fireplace.__init__(self)
        if control_relay is None:
            msg = "Param 'control_relay' cannot be None."
            raise ArgumentNullException(msg)

        self.__controlRelay = control_relay
        self.__pilotLightSensor = pilot_sensor
        self.__onRelayState = on_relay_state
        self.__pilotSensorState = pilot_state
        self.__controlRelay.on(relay.EVENT_STATE_CHANGED,
                               lambda evt: self._handle_relay_state_change(evt))
        if self.__pilotLightSensor is not None:
            self.__pilotLightSensor.on(sensor.EVENT_STATE_CHANGED,
                                       lambda evt: self._handle_sensor_state_change(evt))

    def _handle_relay_state_change(self, evt):
        """Internal event handler for the relay state change event.

        This fires the fireplace state changed event when the relay's
        state changes.

        :param raspy.components.relays.relay_state_change_event.RelayStateChangeEvent evt:
        The event object.
        """
        if evt.new_state == self.__onRelayState:
            state_evt = FireplaceStateChangeEvent(fireplace_state.OFF, fireplace_state.ON)
        else:
            state_evt = FireplaceStateChangeEvent(fireplace_state.ON, fireplace_state.OFF)

        self.on_state_change(state_evt)

    def _handle_sensor_state_change(self, evt):
        """Internal handler for the pilot light sensor state change event.

        This fires the pilot light state change event when the pilot light's
        sensor state changes.

        :param raspy.components.sensors.sensor_state_change_event.SensorStateChangeEvent evt:
        The event object.
        """
        if evt.new_state == self.__pilotSensorState:
            self.turn_off()

        light_evt = FireplacePilotLightEvent(self.is_pilot_light_on)
        self.on_pilot_light_state_change(light_evt)

    @property
    def pilot_light_sensor(self):
        """Get the pilot light sensor used to detect the pilot light state.

        :returns: The pilot light sensor.
        :rtype: raspy.components.sensors.sensor.Sensor
        """
        return self.__pilotLightSensor

    @property
    def control_relay(self):
        """Get the relay being used to control ignition.

        :returns: The control relay.
        :rtype: raspy.components.relays.relay.Relay
        """
        return self.__controlRelay

    @property
    def is_pilot_light_on(self):
        """Get a flag indicating whether the pilot light is on.

        :returns: True if the pilot light is on.
        :rtype: bool
        """
        if self.__pilotLightSensor is None:
            return False
        return self.__pilotLightSensor.is_state(self.__pilotSensorState)

    @property
    def is_pilot_light_off(self):
        """Get a flag indicating whether the pilot light is off.

        :returns: True if the pilot light is off.
        :rtype: bool
        """
        return not self.is_pilot_light_on

    @property
    def state(self):
        """Get the fireplace state.

        :returns: The fireplace state.
        :rtype: int
        """
        if self.__controlRelay.state == self.__onRelayState:
            return fireplace_state.ON
        return fireplace_state.OFF

    @state.setter
    def state(self, the_state):
        """Set the fireplace state.

        :param int the_state: The fireplace state.
        :raises: FireplacePilotLightException if no pilot light sensor is present.
        """
        if self.state != the_state:
            if the_state == fireplace_state.OFF:
                if self.__controlRelay.state == self.__onRelayState:
                    self.__controlRelay.toggle()
            else:
                if self.__pilotLightSensor is not None and self.is_pilot_light_off:
                    raise FireplaceLightException()

                if self.__controlRelay.state != self.__onRelayState:
                    self.__controlRelay.state = self.__onRelayState

            Fireplace.state.fset(self, the_state)

    def dispose(self):
        """Release all managed resources used by this component."""
        if self.is_disposed:
            return

        if self.__controlRelay is not None:
            self.__controlRelay.dispose()
            self.__controlRelay = None

        if self.__pilotLightSensor is not None:
            self.__pilotLightSensor.dispose()
            self.__pilotLightSensor = None

        Fireplace.dispose(self)
