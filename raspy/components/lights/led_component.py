"""This module contains the LedComponent type."""


import threading
from raspy.argument_null_exception import ArgumentNullException
from raspy.invalid_operation_exception import InvalidOperationException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.lights.led import Led
from raspy.components.lights.light_state_change_event import LightStateChangeEvent
from raspy.io import pin_state
from raspy.io import pin_mode
from raspy.pi_system import system_info


ON_STATE = pin_state.HIGH
OFF_STATE = pin_state.LOW


class LedComponent(Led):
    """A component that is an abstraction of an LED."""

    def __init__(self, pin):
        """Initialize a new instance of LedComponent.

        :param raspy.io.gpio.Gpio pin: The output pin the LED is wired to.
        :raises: raspy.argument_null_exception.ArgumentNullException if the
        pin is None.
        """
        Led.__init__(self)
        if pin is None:
            raise ArgumentNullException("'pin' param cannot be None.")

        self.__blinkElapsed = 0
        self.__blinkDuration = 0
        self.__blinkDelay = 0
        self.__pin = pin
        self.__pin.provision()
        self.__stopEvent = threading.Event()
        self.__stopEvent.set()
        self.__blinkThread = None

    @property
    def pin(self):
        """Get the underlying pin the LED is wired to.

        :returns: The underlying phyiscal pin.
        :rtype: raspy.io.gpio.Gpio
        """
        return self.__pin

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
            raise ObjectDisposedException("LedComponent")

        if self.__pin.mode != pin_mode.OUT:
            msg = "Pin is not configured as an output pin."
            raise InvalidOperationException(msg)

        if self.__pin.state != ON_STATE:
            self.__pin.write(pin_state.HIGH)
            evt = LightStateChangeEvent(True)
            Led.on_light_state_changed(self, evt)

    def turn_off(self):
        """Turn the light off.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("LedComponent")

        if self.__pin.mode != pin_mode.OUT:
            msg = "Pin is not configured as an output pin."
            raise InvalidOperationException(msg)

        if self.__pin.state != OFF_STATE:
            self.__pin.write(pin_state.LOW)
            evt = LightStateChangeEvent(False)
            Led.on_light_state_changed(self, evt)

    def reset_blink(self):
        """Reset the blink interval timer."""
        if self.is_disposed:
            return

        if self.__stopEvent.is_set() or self.__blinkThread is None:
            return

        self.__stopEvent.set()
        self.__blinkElapsed = 0
        self.__blinkDuration = 0
        self.__blinkDelay = 0

    def _do_blink_interval(self):
        """The blink interval callback function.

        This checks to see if still within the duration period, and if so,
        turns the LED on for the specified delay time, then turns it back off.
        """
        while not self.__stopEvent.is_set():
            millis = system_info.get_current_time_millis()
            if (millis - self.__blinkElapsed) <= self.__blinkDuration:
                self.__blinkElapsed = millis
                self.turn_on()
                delay = 0.0
                if self.__blinkDelay > 0.0:
                    delay = self.__blinkDelay / 1000
                _t = threading.Timer(delay, self.turn_off)
                _t.start()

    def _blink_once(self, delay):
        """Execute a single blink.

        This turns on the LED, wait for a delay, then turn the LED off.

        :param int delay: The delay in milliseconds.
        """
        self.turn_on()
        _d = 0.0
        if delay > 0.0:
            _d = delay / 1000
        _t = threading.Timer(_d, self.turn_off)
        _t.start()

    def blink(self, delay=0.0, duration=0.0):
        """Blink the LED.

        :param int delay: The delay between state change.
        :param int duration: The amount of time to blink the LED (in millis).
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("LedComponent")

        if duration > 0.0:
            self.__blinkDuration = duration
            self.__blinkDelay = delay
            self.__blinkElapsed = system_info.get_current_time_millis()
            self.__stopEvent.clear()
            self.__blinkThread = threading.Thread(target=self._do_blink_interval)
            self.__blinkThread.name = "blinkThread"
            self.__blinkThread.daemon = True
            self.__blinkThread.start()
        else:
            self._blink_once(delay)

    def pulse(self, duration=0.0):
        """Pulse the state of the LED.

        :param int duration: The amount of time to pulse the LED (in millis).
        """
        if duration > 0.0:
            self.__pin.pulse(duration)

    def dispose(self):
        """Dispose managed resources."""
        if self.is_disposed:
            return

        self.reset_blink()
        self.__blinkElapsed = 0
        self.__blinkDuration = 0
        self.__blinkDelay = 0
        self.__stopEvent = None
        self.__blinkThread = None
        if self.__pin is not None:
            self.__pin.dispose()
            self.__pin = None
        Led.dispose(self)
