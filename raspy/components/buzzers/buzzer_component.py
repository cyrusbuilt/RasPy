"""This module contains the BuzzerComponent type."""


import threading
from raspy import string_utils
from raspy.argument_null_exception import ArgumentNullException
from raspy.components.component import Component
from raspy.components.buzzers.buzzer import Buzzer


class BuzzerComponent(Buzzer):
    """A buzzer device abstraction component."""

    STOP_FREQ = 0.0
    """The stop frequency."""

    def __init__(self, pwm_pin):
        """Initialize a new instance of BuzzerComponent.

        :param raspy.io.gpio.Gpio pwm_pin: The pin the buzzer is attached to.
        :raise: raspy.argument_null_exception.ArgumentNullException if pin is
        None.
        """
        Buzzer.__init__(self)
        if pwm_pin is None:
            raise ArgumentNullException("'pwm_pin' cannot be None.")

        self.__pwmPin = pwm_pin
        self.__isBuzzing = False
        self.__pwmPin.provision()
        self.__buzzTimer = None

    @property
    def pin(self):
        """Get the underlying pin the buzzer is attached to.

        :returns The underlying physical pin.
        :rtype: raspy.io.gpio.Gpio
        """
        return self.__pwmPin

    def dispose(self):
        """Dispose managed resources.

        Performs application-defined tasks associated with freeing, releasing,
        or resetting resources.
        """
        if self.is_disposed:
            return

        if self.__pwmPin is not None:
            self.__pwmPin.dispose()
            self.__pwmPin = None

        Buzzer.dispose(self)

    @property
    def is_buzzing(self):
        """Get whether or not this buzzer is buzzing.

        :returns: True if buzzer is buzzing; Otherwise, False.
        :rtype: bool
        """
        return self.__isBuzzing

    def _internal_buzz(self, freq):
        """Start the buzzer at the specified frequency.

        :param float freq: the frequency to buzz at.
        """
        if freq == self.STOP_FREQ:
            self.__pwmPin.pwm = freq
            self.__isBuzzing = False
            if self.__buzzTimer is not None:
                self.__buzzTimer.cancel()
        else:
            rng = 600000.0 / freq
            self.__pwmPin.pwm_range = rng
            self.__pwmPin.pwm = freq / 2.0
            self.__isBuzzing = True

    def stop(self):
        """Stop the buzzer."""
        self._internal_buzz(self.STOP_FREQ)

    def buzz(self, freq, duration=None):
        """Start the buzzer at the specified freq.

        :param float freq: The frequency to buzz at.
        :param float duration: The duration in milliseconds. If not specified,
        buzzes until stopped.
        """
        if duration is None:
            duration = self.STOP_FREQ

        self._internal_buzz(freq)
        if duration > self.STOP_FREQ:
            self.__buzzTimer = threading.Timer(duration, self.stop)
            self.__buzzTimer.start()

    def __str__(self):
        """Return the string representation of this class instance.

        :returns: The string representation of this class.
        :rtype: str
        """
        base = Component.component_name.fget()
        if not string_utils.is_null_or_empty(base):
            return base
        return self.__class__.__name__
