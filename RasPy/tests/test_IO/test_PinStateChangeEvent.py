"""Test the PinStateChangeEvent class."""


from pyee import EventEmitter
from RasPy.IO import GpioPins
from RasPy.IO import PinState
from RasPy.IO.PinStateChangeEvent import PinStateChangeEvent


class DummyEmitter(object):
    """Dummy emitter for testing."""

    __emitter = None

    def __init__(self):
        """ctor."""
        self.__emitter = EventEmitter()

    def on(self, evt, callback):
        """Register event handler."""
        self.__emitter.on(evt, callback)

    def emit(self, evt, args):
        """Fire event."""
        self.__emitter.emit(evt, args)

    def on_pin_state_change(self, psce):
        """Fire the pin state change event."""
        self.emit("gpioStateChanged", psce)

    def trigger_event(self):
        """Trigger the state change event."""
        pinAddress = GpioPins.GPIO01.value
        oldState = PinState.LOW
        newState = PinState.HIGH
        evt = PinStateChangeEvent(oldState, newState, pinAddress)
        self.on_pin_state_change(evt)


class TestPinStateChangeEvent(object):
    """Test pin state change event."""

    def __state_change_handler(self, stateChangeEvt):
        assert isinstance(stateChangeEvt, PinStateChangeEvent)
        expected = PinState.LOW
        actual = stateChangeEvt.old_state
        assert actual == expected

        expected = PinState.HIGH
        actual = stateChangeEvt.new_state
        assert actual == expected

        expected = 1
        actual = stateChangeEvt.pin_address
        assert actual == expected

    def test_state_change(self):
        """Actually tests the event."""
        d = DummyEmitter()
        d.on("gpioStateChanged", self.__state_change_handler)
        d.trigger_event()
