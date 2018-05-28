"""Tests for the RasPy.IO.InvalidPinModeException class."""


from RasPy.IO import Gpio
from RasPy.IO import GpioPins
from RasPy.IO import PinMode
from RasPy.IO import PinState
from RasPy.IO.InvalidPinModeException import InvalidPinModeException


class FakeGpio(Gpio.Gpio):
    def __init__(self, pn):
        super(FakeGpio, self).__init__(pn, None, None)

        self.mode = PinMode.OUT
        self.pin_name = self.inner_pin.name

    def read(self):
        if (self.mode != PinMode.IN, self):
            raise InvalidPinModeException("Pin must be an input.", self)

        return PinState.HIGH


class TestInvalidPinModeException(object):
    """Test InvalidPinModeException class."""

    def test_throw(self):
        """Test throwing the exception."""
        pinAddr = -1
        result = False
        fg = FakeGpio(GpioPins.GPIO01)

        try:
            fg.read()
        except Exception as ex:
            result = isinstance(ex, InvalidPinModeException)
            if result:
                pinAddr = ex.pin.address

        assert result
        assert pinAddr == GpioPins.GPIO01.value
