"""Tests the UnrecognizedPinFoundEvent class."""


from pyee import EventEmitter
from raspy.io import gpio_pins
from raspy.io.unrecognized_pin_found_event import UnrecognizedPinFoundEvent


class DummyEmitter(object):
    """Dummy emitter for testing."""

    __emitter = None
    __scanPin = None
    __pinCache = []

    def __init__(self, pin):
        """ctor."""
        self.__emitter = EventEmitter()
        self.__scanPin = pin
        if self.__scanPin is None:
            self.__scanPin = gpio_pins.Gpio01
        self.__pinCache = [gpio_pins.Gpio00, gpio_pins.Gpio04]

    def on(self, evt, callback):
        """Register event handler."""
        self.__emitter.on(evt, callback)

    def emit(self, evt, args):
        """Fire event."""
        self.__emitter.emit(evt, args)

    def on_unrecognized_pin(self, pinFoundEvent):
        """Fire then unrecognized pin found event."""
        self.emit("unrecognizedPinFound", pinFoundEvent)

    def scan_pins(self):
        """Scan the pin cache."""
        found = False
        for i in range(len(self.__pinCache)):
            if self.__pinCache[i].value == self.__scanPin.value:
                found = True
                break

        if not found:
            msg = "Unknown pin: " + self.__scanPin.name
            evt = UnrecognizedPinFoundEvent(msg)
            self.on_unrecognized_pin(evt)


class TestUnrecognizedPinFoundEvent(object):
    """Test UnrecognizedPinFoundEvent."""

    def __event_handler(self, evt):
        """Event handler."""
        assert isinstance(evt, UnrecognizedPinFoundEvent)
        expected = "Unknown pin: " + gpio_pins.Gpio01.name
        actual = evt.event_message
        assert actual == expected

    def test_unrecognized_pin_found_event(self):
        """Test the event."""
        d = DummyEmitter(gpio_pins.Gpio01)
        d.on("unrecognizedPinFound", self.__event_handler)
        d.scan_pins()
