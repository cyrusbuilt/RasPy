"""A Raspberry Pi GPIO Interface."""


from raspy import board_revision
from raspy.io import gpio_pins
from raspy.io.gpio import Gpio


class RaspiGpio(Gpio):
    """A Raspberry Pi GPIO interface."""

    def __init__(self):
        """Initialize a new instance of the raspy.io.raspi_gpio.RaspiGpio class."""
        super(Gpio, self).__init__()

    @property
    def revision(self):
        """Get the board revision.

        :returns: The board revision.
        :rtype: int
        """
        return board_revision.REV2

    @property
    def inner_pin(self):
        """Get the inner pin being represented by this instance.

        :returns: The underlying physical pin.
        :rtype: RasPy.io.GpioPins
        """
        return gpio_pins.GpioNone()

    def on_pin_state_change(self, psce):
        """Fire the pin state change event.

        :param raspy.io.pin_state_change_event.PinStateChangeEvent psce: The
        pin state change event.
        """
        pass
