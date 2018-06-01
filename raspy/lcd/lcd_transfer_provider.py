"""Base type for LCD transfer providers."""

from raspy.disposable import Disposable


class LcdTransferProvider(Disposable):
    """LCD data transfer provider base type."""

    def __init__(self):
        """Initialize a new instance of the raspy.lcd.lcd_transfer_provider.LcdTransferProvider."""
        super(Disposable, self).__init__()

    def send(self, data, mode, back_light):
        """Send the specified data, mode, and backlight.

        :param byte, int data: The data to send.
        :param int mode: Mode for register-select pin (pin_state.HIGH = on,
        pin_state.LOW = off).
        :param bool back_light: Set True to turn on the backlight.
        """
        pass

    @property
    def is_four_bit_mode(self):
        """Get a value indicating whether this instance is in 4-bit mode.

        :returns: True if 4-bit mode; Otherwise, false.
        :rtype: bool
        """
        return False
