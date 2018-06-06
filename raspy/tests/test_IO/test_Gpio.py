"""Tests for raspy.io.Gpio class."""


from raspy import board_revision
from raspy.io import gpio
from raspy.io import gpio_pins
from raspy.io import pin_mode
from raspy.io import pin_state
from raspy.io.pin_state_change_event import PinStateChangeEvent


class FakeGpio(gpio.Gpio):
    """Dummy GPIO for testing."""

    def __init__(self, pin, mode, value):
        """ctor."""
        gpio.Gpio.__init__(self, pin, mode, value)
        if value is None or not isinstance(value, (int, long)):
            value = pin_state.LOW

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
        fg = FakeGpio(gpio_pins.Gpio01, pin_mode.IN, pin_state.LOW)
        assert not fg.is_disposed

        fg.dispose()
        assert fg.is_disposed

    def test_board_revision(self):
        """Test change_board_revision method."""
        fg = FakeGpio(gpio_pins.Gpio01, pin_mode.IN, pin_state.LOW)
        fg.change_board_revision(board_revision.REV2)
        assert fg.revision == board_revision.REV2

    def test_read(self):
        """Test read method."""
        fg = FakeGpio(gpio_pins.Gpio01, pin_mode.IN, pin_state.LOW)
        assert fg.read() == pin_state.LOW

    def test_state(self):
        """Test state property."""
        fg = FakeGpio(gpio_pins.Gpio01, pin_mode.IN, pin_state.HIGH)
        assert fg.state == pin_state.HIGH

    def test_write(self):
        """Test write method."""
        fg = FakeGpio(gpio_pins.Gpio01, pin_mode.IN, pin_state.LOW)
        assert fg.state == pin_state.LOW

        fg.write(pin_state.HIGH)
        assert fg.state == pin_state.HIGH

    def test_inner_pin(self):
        """Test inner_pin property."""
        fg = FakeGpio(gpio_pins.Gpio01, pin_mode.IN, pin_state.LOW)
        p = fg.inner_pin

        assert p.value == gpio_pins.Gpio01.value

    def test_mode(self):
        """Test mode property."""
        fg = FakeGpio(gpio_pins.Gpio01, pin_mode.IN, pin_state.LOW)
        assert fg.mode == pin_mode.IN

        fg.mode = pin_mode.OUT
        assert fg.mode == pin_mode.OUT

    def test_address(self):
        """Test address property."""
        fg = FakeGpio(gpio_pins.Gpio01, pin_mode.IN, pin_state.LOW)
        assert fg.address == gpio_pins.Gpio01.value

    def __state_change_handler(self, stateChanged):
        assert stateChanged.old_state == pin_state.LOW
        assert stateChanged.new_state == pin_state.HIGH

    def test_pin_state_change(self):
        """Test state change event."""
        print "Testing test_pin_state_change"
        fg = FakeGpio(gpio_pins.Gpio01, pin_mode.IN, pin_state.LOW)
        fg.on(gpio.EVENT_GPIO_STATE_CHANGED, self.__state_change_handler)
        fg.write(pin_state.HIGH)
