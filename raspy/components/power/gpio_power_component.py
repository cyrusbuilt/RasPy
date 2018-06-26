"""This module contains the GpioPowerComponent type."""


from raspy.argument_null_exception import ArgumentNullException
from raspy.invalid_operation_exception import InvalidOperationException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.power import power_interface as pwr
from raspy.components.power import power_state
from raspy.components.power import power_utils
from raspy.components.power.power_state_change_event import PowerStateChangeEvent
from raspy.io import pin_mode
from raspy.io import pin_state
from raspy.io import gpio
from raspy.io.invalid_pin_mode_exception import InvalidPinModeException


class GpioPowerComponent(pwr.PowerInterface):
    """A power control component implemented using a single native output GPIO."""

    def __init__(self, pin, on_state=pin_state.HIGH, off_state=pin_state.LOW):
        """Initialize a new instance of GpioPowerComponent.

        :param raspy.io.raspi_gpio.RaspiGpio pin: The GPIO on the RPi that the
        device is attached to.
        :param int on_state: The pin state to consider the device "on".
        :param int off_state: The pin state to consider the device "off".
        :raises: ArgumentNullException if the specified pin is None.
        """
        pwr.PowerInterface.__init__(self)
        if pin is None:
            raise ArgumentNullException("'pin' param cannot be None.")

        self.__output = pin
        self.__onState = on_state
        self.__offState = off_state
        self.__output.provision()
        self.__output.on(gpio.EVENT_GPIO_STATE_CHANGED,
                         lambda psce: self._on_output_state_changed(psce))

    def _on_output_state_changed(self, evt):
        """Internal handler for the output pin state change event.

        This dispatches the power state change event based on pin state.

        :param raspy.io.pin_state_change_event.PinStateChangeEvent evt: The
        state change event info.
        """
        if evt.new_state == self.__onState:
            pwr_evt = PowerStateChangeEvent(power_state.OFF, power_state.ON)
            self.on_power_state_changed(pwr_evt)
        else:
            pwr_evt = PowerStateChangeEvent(power_state.ON, power_state.OFF)
            self.on_power_state_changed(pwr_evt)

    @property
    def pin(self):
        """Get the pin this power component is attached to.

        :returns: The underlying physical pin.
        :rtype: raspy.io.raspi_gpio.RaspiGpio
        """
        return self.__output

    def dispose(self):
        """Release managed resources used by this component."""
        if self.is_disposed:
            return

        if self.__output is not None:
            self.__output.dispose()
            self.__output = None

        pwr.PowerInterface.dispose(self)

    @property
    def state(self):
        """Get the state of the power component.

        :returns: The state of the power component.
        :rtype: int
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        :raises: raspy.io.invalid_pin_mode_exception.InvalidPinModeException if
        the pin being used to control this device is not configure as an
        output.
        """
        if self.__output.state == self.__onState:
            return power_state.ON
        elif self.__output.state == self.__offState:
            return power_state.OFF
        else:
            return power_state.UNKNOWN

    @state.setter
    def state(self, pwr_state):
        """Set the state of the power component.

        :param int pwr_state: The state to set.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        :raises: raspy.io.invalid_pin_mode_exception.InvalidPinModeException if
        the pin being used to control this device is not configure as an
        output.
        :raises: raspy.invalid_operation_exception.InvalidOperationException if
        an invalid state is specified.
        """
        if self.is_disposed:
            raise ObjectDisposedException("GpioPowerComponent")

        if self.__output.mode != pin_mode.OUT:
            msg = "Pins in use by power components MUST be configured as "
            msg += "outputs."
            raise InvalidPinModeException(msg, self.__output)

        if pwr_state == power_state.OFF:
            self.__output.write(self.__offState)
            pwr.PowerInterface.state.fset(self, pwr_state)
        elif pwr_state == power_state.ON:
            self.__output.write(self.__onState)
            pwr.PowerInterface.state.fset(self, pwr_state)
        else:
            bad_state = power_utils.get_power_state_name(pwr_state)
            msg = "Cannot set power state: " + bad_state
            raise InvalidOperationException(msg)
