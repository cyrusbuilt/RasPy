"""This module contains the LightComponent type."""


from raspy.argument_null_exception import ArgumentNullException
from raspy.invalid_operation_exception import InvalidOperationException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.lights import light
from raspy.components.lights.light_state_change_event import LightStateChangeEvent
from raspy.io import pin_state
from raspy.io import pin_mode


ON_STATE = pin_state.HIGH
OFF_STATE = pin_state.LOW


class LightComponent(light.Light):
    """A component that is an abstraction of a light."""

    def __init__(self, pin):
        """Initialize a new intance of LightComponent.

        :param raspy.io.gpio.Gpio pin: The output pin the light is wired to.
        :raises: raspy.argument_null_exception.ArgumentNullException if pin
        is None.
        """
        light.Light.__init__(self)
        if pin is None:
            raise ArgumentNullException("'pin' param cannot be None.")

        self.__pin = pin
        self.__pin.provision()

    def dispose(self):
        """Dispose managed resources."""
        if self.is_disposed:
            return

        if self.__pin is not None:
            self.__pin.dispose()
            self.__pin = None

        self.remove_all_listeners()
        light.Light.dispose(self)

    @property
    def is_on(self):
        """Get a value indicating whether or not the light is on.

        :returns: True if the light is on.
        :rtype: bool
        """
        return self.__pin.state == ON_STATE

    def turn_on(self):
        """Turn the light on.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("LightComponent")

        if self.__pin.mode != pin_mode.OUT:
            msg = "Pin is not configured as an output pin."
            raise InvalidOperationException(msg)

        if self.__pin.state != ON_STATE:
            self.__pin.write(pin_state.HIGH)
            evt = LightStateChangeEvent(True)
            light.Light.on_light_state_changed(self, evt)

    def turn_off(self):
        """Turn the light off.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("LightComponent")

        if self.__pin.mode != pin_mode.OUT:
            msg = "Pin is not configured as an output pin."
            raise InvalidOperationException(msg)

        if self.__pin.state != OFF_STATE:
            self.__pin.write(pin_state.LOW)
            evt = LightStateChangeEvent(False)
            light.Light.on_light_state_changed(self, evt)
