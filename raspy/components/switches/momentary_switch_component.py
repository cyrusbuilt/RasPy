"""This module contains the MomentarySwitchComponent type."""


import threading
from raspy.argument_null_exception import ArgumentNullException
from raspy.invalid_operation_exception import InvalidOperationException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.switches import switch_state
from raspy.components.switches.momentary_switch import MomentarySwitch
from raspy.components.switches.switch_state_change_event import SwitchStateChangeEvent
from raspy.io import pin_mode
from raspy.io import pin_state
from raspy.io import gpio
from raspy.pi_system import core_utils


OFF_STATE = pin_state.LOW
"""The pin state to consider the switch off."""

ON_STATE = pin_state.HIGH
"""The pin state to consider the switch on."""


class MomentarySwitchComponent(MomentarySwitch):
    """A component that is an abstraction of a momentary switch."""

    def __init__(self, pin):
        """Initialize a new instance of MomentarySwitchComponent.

        :param gpio.Gpio pin: The input pin the switch is attached to.
        :raises: ArgumentNullException if pin is None.
        """
        MomentarySwitch.__init__(self)
        if pin is None:
            raise ArgumentNullException("'pin' param cannot be None.")

        self.__isPolling = False
        self.__pollThread = None
        self.__stopEvent = threading.Event()
        self.__stopEvent.set()
        self.__pin = pin
        self.__pin.provision()
        self.__pin.on(gpio.EVENT_GPIO_STATE_CHANGED,
                      lambda evt: self._on_pin_state_changed(evt))

    def _on_pin_state_changed(self, psce):
        """Handle the pin state change event.

        This verifies the state has actually changed, then fires the switch
        state change event.

        :param raspy.io.pin_state_change_event.PinStateChangeEvent psce: The
        pin state change event info.
        """
        if psce.new_state != psce.old_state:
            evt = SwitchStateChangeEvent(switch_state.ON, switch_state.OFF)
            if psce.new_state == ON_STATE:
                evt = SwitchStateChangeEvent(switch_state.OFF, switch_state.ON)
            self.on_switch_state_changed(evt)

    @property
    def pin(self):
        """Get the GPIO pin this switch is attached to.

        :returns: The underlying physical pin.
        :rtype: gpio.Gpio
        """
        return self.__pin

    @property
    def state(self):
        """Get the state of the switch.

        :returns: The switch state.
        :rtype: int
        """
        if self.__pin.state == ON_STATE:
            return switch_state.ON
        return switch_state.OFF

    @property
    def is_polling(self):
        """Check to see if the switch is in poll mode."""
        return self.__isPolling

    def _execute_poll(self):
        """Execute the poll cycle."""
        while not self.__stopEvent.is_set():
            self.__pin.read()
            core_utils.sleep(500)

    def poll(self):
        """Poll the switch status.

        :raises: ObjectDisposedException if this instance has been disposed.
        :raises: InvalidOperationException if this switch is attached to a
        pin that has not been configured as an input.
        """
        if self.is_disposed:
            raise ObjectDisposedException("SwitchComponent")

        if self.__pin.mode != pin_mode.IN:
            msg = "The pin this switch is attached to must be configured"
            msg += " as an input."
            raise InvalidOperationException(msg)

        if self.__isPolling:
            return

        self.__stopEvent.clear()
        self.__isPolling = True
        self.__pollThread = threading.Thread(target=self._execute_poll)
        self.__pollThread.name = "MomentarySwitchComponentPollThread"
        self.__pollThread.daemon = True
        self.__pollThread.start()

    def interrupt_poll(self):
        """Interrupt the poll cycle."""
        if not self.__isPolling or self.is_disposed:
            return

        if self.__stopEvent.is_set() or self.__pollThread is None:
            return

        self.__stopEvent.set()
        self.__isPolling = False

    def dispose(self):
        """Release managed resources used by this component."""
        if self.is_disposed:
            return

        self.interrupt_poll()
        if self.__pin is not None:
            self.__pin.dispose()
            self.__pin = None

        self.__stopEvent = None
        self.__pollThread = None
        MomentarySwitch.dispose(self)
