"""Tests for RasPy.IO.Gpio class."""


from RasPy import BoardRevision
from RasPy.IO import Gpio
from RasPy.IO import GpioPins
from RasPy.IO import PinMode
from RasPy.IO import PinState
from RasPy.IO.PinStateChangeEvent import PinStateChangeEvent


class FakeGpio(Gpio.Gpio):
    """Dummy GPIO for testing."""

    def __init__(self, pin, mode, value):
        """ctor."""
        super(FakeGpio, self).__init__(pin, mode, value)
        if value is None or not isinstance(value, (int, long)):
            value = PinState.LOW

        self.__overriddenState = value

    def read(self):
        """Read value."""
        return self.__overriddenState

    def write(self, ps):
        """Write value."""
        if self.__overriddenState != ps:
            addr = self.inner_pin.value
            evt = PinStateChangeEvent(self.__overriddenState, ps, addr)
            self.__overriddenState = ps
            self.on_pin_state_change(evt)


class TestGpio(object):
    """Test GPIO of class."""

    def test_dispose_and_isdisposed(self):
        """Test dispose method and isDisposed property."""
        fg = FakeGpio(GpioPins.GPIO01, PinMode.IN, PinState.LOW)
        assert not fg.is_disposed

        fg.dispose()
        assert fg.is_disposed

    def test_board_revision(self):
        """Test change_board_revision method."""
        fg = FakeGpio(GpioPins.GPIO01, PinMode.IN, PinState.LOW)
        fg.change_board_revision(BoardRevision.REV2)
        assert fg.revision == BoardRevision.REV2

    def test_read(self):
        """Test read method."""
        fg = FakeGpio(GpioPins.GPIO01, PinMode.IN, PinState.LOW)
        assert fg.read() == PinState.LOW

    def test_state(self):
        """Test state property."""
        fg = FakeGpio(GpioPins.GPIO01, PinMode.IN, PinState.HIGH)
        assert fg.state == PinState.HIGH

    def test_write(self):
        """Test write method."""
        fg = FakeGpio(GpioPins.GPIO01, PinMode.IN, PinState.LOW)
        assert fg.state == PinState.LOW

        fg.write(PinState.HIGH)
        assert fg.state == PinState.HIGH

    def test_inner_pin(self):
        """Test inner_pin property."""
        fg = FakeGpio(GpioPins.GPIO01, PinMode.IN, PinState.LOW)
        p = fg.inner_pin

        assert p.value == GpioPins.GPIO01.value

    def test_mode(self):
        """Test mode property."""
        fg = FakeGpio(GpioPins.GPIO01, PinMode.IN, PinState.LOW)
        assert fg.mode == PinMode.IN

        fg.mode = PinMode.OUT
        assert fg.mode == PinMode.OUT

    def test_address(self):
        """Test address property."""
        fg = FakeGpio(GpioPins.GPIO01, PinMode.IN, PinState.LOW)
        assert fg.address == GpioPins.GPIO01.value

    def __state_change_handler(self, stateChanged):
        assert stateChanged.old_state == PinState.LOW
        assert stateChanged.new_state == PinState.HIGH

    def test_pin_state_change(self):
        """Test state change event."""
        print "Testing test_pin_state_change"
        fg = FakeGpio(GpioPins.GPIO01, PinMode.IN, PinState.LOW)
        fg.on(Gpio.EVENT_GPIO_STATE_CHANGED, self.__state_change_handler)
        fg.write(PinState.HIGH)
