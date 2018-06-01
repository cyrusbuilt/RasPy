"""Tests for the raspy.io.InvalidPinModeException class."""


from raspy.io import gpio
from raspy.io import gpio_pins
from raspy.io import pin_mode
from raspy.io import pin_state
from raspy.io.invalid_pin_mode_exception import InvalidPinModeException


class FakeGpio(gpio.Gpio):
    def __init__(self, pn):
        super(FakeGpio, self).__init__(pn, None, None)

        self.mode = pin_mode.OUT
        self.pin_name = self.inner_pin.name

    def read(self):
        if (self.mode != pin_mode.IN, self):
            raise InvalidPinModeException("Pin must be an input.", self)

        return pin_state.HIGH


class TestInvalidPinModeException(object):
    """Test InvalidPinModeException class."""

    def test_throw(self):
        """Test throwing the exception."""
        pinAddr = -1
        result = False
        fg = FakeGpio(gpio_pins.Gpio01)

        try:
            fg.read()
        except Exception as ex:
            result = isinstance(ex, InvalidPinModeException)
            if result:
                pinAddr = ex.pin.address

        assert result
        assert pinAddr == gpio_pins.Gpio01.value
