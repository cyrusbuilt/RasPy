"""Test the PinPollFailEvent class."""


import threading
from pyee import EventEmitter
from raspy.io.pin_poll_fail_event import PinPollFailEvent
from raspy.io.io_exception import IOException


class DummyEmitter(object):
    """Dummy emitter for testing."""

    __emitter = None
    __evt = None
    __pollThread = None

    def __init__(self):
        """ctor."""
        self.__emitter = EventEmitter()

    def on(self, evt, callback):
        """Register event handler."""
        self.__emitter.on(evt, callback)

    def emit(self, evt, args):
        """Fire event."""
        self.__emitter.emit(evt, args)

    def on_poll_fail(self):
        """Fire pin poll faiure event."""
        self.emit("pinPollFailed", self.__evt)

    def poll(self):
        """Execute pin polling on background thread."""
        ioEx = IOException("Poll failed.")
        self.__evt = PinPollFailEvent(ioEx)
        self.__pollThread = threading.Thread(target=self.on_poll_fail)
        self.__pollThread.name = "DummyEmitterThread"
        self.__pollThread.daemon = True
        self.__pollThread.start()


class TestPinPollFailEvent(object):
    """Test pin polling fail event."""

    def __fail_handler(self, failEvt):
        assert isinstance(failEvt, PinPollFailEvent)
        assert isinstance(failEvt.failure_cause, IOException)

    def test_pin_poll_fail_event(self):
        """Test event."""
        d = DummyEmitter()
        d.on("pinPollFailed", self.__fail_handler)
        d.poll()
