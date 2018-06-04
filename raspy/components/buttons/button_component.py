"""This module contains the ButtonComponent type."""


import threading
from raspy.argument_null_exception import ArgumentNullException
from raspy.invalid_operation_exception import InvalidOperationException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.buttons import button
from raspy.components.buttons import button_state
from raspy.components.buttons.button_event import ButtonEvent
from raspy.io import pin_state
from raspy.io import gpio
from raspy.pi_system import core_utils


class ButtonComponent(button.Button):
    """A component that is an abstraction of a button."""

    PRESSED_STATE = pin_state.HIGH
    RELEASED_STATE = pin_state.LOW

    def __init__(self, pin):
        """Initialize a new instance of the ButtonComponent.

        Initializes with the pin it is attached to.

        :param raspy.io.gpio.Gpio pin: The input pin the button is wired to.
        :raises: raspy.argument_null_exception.ArgumentNullException if the
        'pin' param is None.
        """
        button.Button.__init__(self)
        if pin is None:
            raise ArgumentNullException("'pin' param cannot be None.")

        self.__pollThread = None
        self.__pollRunning = False
        self.__stopEvent = threading.Event()
        self.__stopEvent.set()
        self.__pin = pin
        self.__pin.provision()
        self.__pin.on(gpio.EVENT_GPIO_STATE_CHANGED,
                      lambda psce: self._on_pin_state_changed(psce))

    def _on_pin_state_changed(self, psce):
        """Handle the pin state change event.

        This verifies the state has actually changed, then fires the button
        state change event.

        :param raspy.io.pin_state_change_event.PinStateChangeEvent psce: The pin
        state change event info.
        """
        if psce is not None and psce.new_state != psce.old_state:
            self._set_state(psce.new_state)
            evt = ButtonEvent(self)
            self.on_state_changed(evt)

    @property
    def pin(self):
        """Get the underlying pin the button is attached to.

        :returns: The underlying physical pin.
        :rtype: raspy.io.gpio.Gpio
        """
        return self.__pin

    @property
    def state(self):
        """Get the button state.

        :returns: The button state.
        :rtype: int
        """
        global PRESSED_STATE
        if self.__pin.state == PRESSED_STATE:
            return button_state.PRESSED
        return button_state.RELEASED

    @property
    def is_polling(self):
        """Check to see if the button is in poll mode.

        Poll mode is where it reads the button state every 500ms and fires
        state change events when the state changes.

        :returns: True if the button is polling; Otherwise, False.
        :rtype: bool
        """
        return self.__pollRunning

    def _execute_poll(self):
        """Execute the poll cycle."""
        while not self.__stopEvent.is_set():
            self.__pin.read()
            core_utils.sleep(500)

    def interrupt_poll(self):
        """Interrupt the poll cycle."""
        if not self.__pollRunning or self.is_disposed:
            return

        if self.__stopEvent.is_set() or self.__pollThread is None:
            return

        self.__stopEvent.set()
        self.__pollRunning = False

    def poll(self):
        """Start a button state poll cycle.

        This will monitor the button state in a poll loop on a separate thread
        and fire events when the button state changes.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        :raises: raspy.invalid_operation_exception.InvalidOperationException
        if the poll thread is already running.
        """
        if self.is_disposed:
            raise ObjectDisposedException("ButtonComponent")

        if self.__pollRunning:
            raise InvalidOperationException("Poll thread already running.")

        self.__stopEvent.clear()
        self.__pollRunning = True
        self.__pollThread = threading.Thread(target=self._execute_poll)
        self.__pollThread.name = "ButtonComponentPollThread"
        self.__pollThread.daemon = True
        self.__pollThread.start()

    def dispose(self):
        """Dispose managed resources.

        Performs application-defined tasks associated with freeing, releasing,
        or resetting resources.
        """
        if self.is_disposed:
            return

        self.interrupt_poll()
        if self.__pin is not None:
            self.__pin.dispose()
            self.__pin = None

        button.Button.dispose(self)
