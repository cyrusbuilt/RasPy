"""Implemented by classes that represent GPIO pins on the Raspberry Pi."""

import threading
import time
from pyee import EventEmitter
from raspy import board_revision
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.io import gpio_pins
from raspy.io import pin_state
from raspy.io import pin_mode
from raspy.io.pin import Pin


EVENT_GPIO_STATE_CHANGED = "gpioStateChanged"
"""The name of the GPIO state changed event."""


class Gpio(Pin):
    """Implemented by classes that represent GPIO pins on the Raspberry Pi."""

    def __init__(self, pn, mode, value):
        """Initialize a new instance of raspy.io.Gpio.

        :param raspy.io.gpio_pins.GpioPin pn: The GPIO pin.
        :param int mode: The I/O pin mode.
        :param int value: The initial pin value.
        """
        super(Pin, self).__init__()
        self.__emitter = EventEmitter()

        self.__pin = pn
        if self.__pin is None:
            self.__pin = gpio_pins.GpioNone

        self.__mode = mode
        if not isinstance(self.__mode, (int, long)):
            self.__mode = pin_mode.OUT

        self.__initValue = value
        if not isinstance(self.__initValue, (int, long)):
            self.__initValue = pin_state.LOW

        self.__revision = board_revision.REV2
        self.__state = pin_state.LOW

    def on(self, evt, callback):
        """Register an event with a callback to handle it.

        :param str evt: The name of the event to register a handler for.
        :param function callback: The callback to execute when the event
        fires.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance is disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Gpio")

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
            raise ObjectDisposedException("Gpio")

        self.__emitter.emit(evt, args)

    def remove_all_listeners(self):
        """Remove all registered event listeners."""
        if self.is_disposed:
            return

        if self.__emitter is not None:
            self.__emitter.remove_all_listeners()

    def write(self, ps):
        """Write a value to the pin.

        :param int ps: The pin state value to write to the pin.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Gpio")

        self.__state = ps

    def pulse(self, millis):
        """Pulse the pin output for the specified number of milliseconds.

        :param int, long millis: The number of milliseconds to wait between
        states.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if not isinstance(millis, (int, long)):
            millis = 0

        if self.is_disposed:
            raise ObjectDisposedException("Gpio")

        seconds = 0
        if millis > 0:
            seconds = millis / 1000

        self.write(pin_state.HIGH)
        time.sleep(seconds)
        self.write(pin_state.LOW)

    def read(self):
        """Read a value from the pin.

        :returns: The state (value) of the pin.
        :rtype: int
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Gpio")

        return pin_state.LOW

    def on_pin_state_change(self, psce):
        """Fire the pin state change event.

        :param raspy.io.pin_state_change_event.PinStateChangeEvent psce: The
        event object.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance is disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Gpio")

        _t = threading.Thread(target=self.emit,
                              name="stateChange",
                              args=(EVENT_GPIO_STATE_CHANGED, psce))
        _t.daemon = True
        _t.start()

    @property
    def revision(self):
        """Get the board revision.

        :returns: The board revision.
        :rtype: int
        """
        return self.__revision

    @property
    def state(self):
        """Get the state of the pin.

        :returns: The pin state.
        :rtype: int
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        self.__state = self.read()
        return self.__state

    @property
    def inner_pin(self):
        """Get the physical pin being represented by this instance.

        :returns: The underlying physical pin.
        :rtype: raspy.io.gpio_pins.GpioPin
        """
        return self.__pin

    def provision(self):
        """Provision this pin.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Gpio")

        self.write(self.__initValue)

    @property
    def mode(self):
        """Get the pin mode.

        :returns: The pin mode.
        :rtype: int
        """
        return self.__mode

    @mode.setter
    def mode(self, p_mode):
        """Set the pin mode.

        :param int p_mode: The pin mode to set.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Gpio")

        if p_mode is None:
            p_mode = p_mode.TRI

        if self.__mode != p_mode:
            self.__mode = p_mode
            self.provision()

    @property
    def address(self):
        """Get the pin address.

        :returns: The pin address.
        :rtype: int
        """
        return self.__pin.value

    def change_board_revision(self, revision):
        """Change the board revision.

        :param int revision: The board revision.
        """
        if revision is None or not isinstance(revision, (int, long)):
            revision = board_revision.REV2

        self.__revision = revision

    def get_initial_pin_value(self):
        """Get the initial pin value.

        :returns: The initial pin value.
        :rtype: int
        """
        return self.__initValue

    @property
    def pwm(self):
        """Get the PWM (pulse-width modulation) value.

        :returns: The PWM value.
        :rtype: int
        """
        return 0

    @pwm.setter
    def pwm(self, val):
        """Set the PWM (pulse-width modulation) value.

        :param int val: The PWM value.
        """
        pass

    @property
    def pwm_range(self):
        """Get the PWM (pulse-width modulation) range.

        :returns: The PWM range.
        :rtype: int
        """
        return 0

    @pwm_range.setter
    def pwm_range(self, rng):
        """Set the PWM (pulse-width modulation) range.

        :param int rng: The PWM range.
        """
        pass

    def dispose(self):
        """Dispose managed resources."""
        if self.is_disposed:
            return

        self.__emitter.remove_all_listeners()
        self.__emitter = None
        self.__state = None
        self.__mode = None
        self.__pin = None
        self.__initValue = None
        Pin.dispose(self)
