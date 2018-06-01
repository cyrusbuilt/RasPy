"""This module provides the Controller class for the TM1638/TM1640 board."""


from raspy import string_utils
from raspy.io import pin_state
from raspy.led.tm16xx_base import TM16XXBase
from raspy.led.tm16xx_base import C_MAP


class TM1638(TM16XXBase):
    """Controller class for the TM1638/TM1640 board.

    It is a port of the TM1638 library by Ricardo Batista
    URL: http://code.google.com/p/tm1638-library/
    """

    def __init__(self, data, clock, strobe, active, intensity):
        """Initialize a new instance of the raspy.led.TM1638 class.

        Initialize with the pins for data, clock, and strobe, a flag
        indicating whether or not the display should be active, and
        the intensity level.

        :param RasPy.io.RaspiGpio.RaspiGpio data: The data pin.
        :param RasPy.io.RaspiGpio.RaspiGpio clock: The clock pin.
        :param RasPy.io.RaspiGpio.RaspiGpio strobe: The strobe pin.
        :param bool active: Set True to activate the display.
        :param int intensity: The display intensity (brightness) level.
        :raises: raspy.ArgumentNullException.ArgumentNullException if the
        data, clock, or strobe pins are NonePin or undefined.
        """
        TM16XXBase.__init__(self, data, clock, strobe, 8, active, intensity)

    def set_display_to_hex_number(self, number):
        """Set the display to a hex number.

        :param int number: An unsigned long number to display (gets converted
        to hex.
        """
        TM16XXBase.set_display_to_string(self, "{0:x}".format(number))

    def set_display_to_dec_number_at(self, number, dots, start_pos, leading_zeros):
        """Set the display to a decimal number at the starting position.

        :param int number: The number to display (if out of range, the display
        will be cleared).
        :param bool dots: Set True to turn on dots.
        :param int start_pos: The starting position to display the number at.
        :param bool leading_zeros: Set True to lead the number with zeros.
        """
        if number > 99999999:
            TM16XXBase.set_display_to_error(self)

        displays = TM16XXBase._get_displays(self)
        for i in range(0, (displays - start_pos) - 1):
            pos = (displays - i - 1)
            l_dot = ((dots & (1 << i)) != 0)
            if number != 0:
                digit = number % 10
                TM16XXBase.set_display_digit(self, digit, pos, l_dot)
                number /= 10
            else:
                if leading_zeros:
                    digit = 0
                    TM16XXBase.set_display_digit(self, digit, pos, l_dot)
                else:
                    TM16XXBase.clear_display_digit(self, pos, l_dot)

    def set_display_to_dec_number(self, number, dots, leading_zeros):
        """Set the display to a decimal number.

        :param int number: The number to display (if out of range, the display
        will be cleared).
        :param bool dots: Set True to turn on dots.
        :param bool leading_zeros: Set True to lead the number with zeros.
        """
        self.set_display_to_dec_number_at(number, dots, 0, leading_zeros)

    def send_char(self, pos, data, dot):
        """Send a character to the display.

        :param byte, int pos: The position at which to set the character.
        :param byte, int data: The data (character) to set in the display.
        :param bool dot: Set True to turn on the dots.
        """
        address = pos << 1
        one = string_utils.convert_string_to_byte("10000000")
        zero = string_utils.convert_string_to_byte("00000000")
        dot_char = zero
        if dot:
            dot_char = one

        l_data = data | dot_char
        TM16XXBase.send_data(self, address, l_data)

    def set_display_to_signed_dec_number(self, number, dots, leading_zeros):
        """Set the display to a signed decimal number.

        :param int number: The signed decimal number to set in the display.
        :param bool dots: Set True to turn on dots.
        :param bool leading_zeros: Set True to lead the number with zeros.
        """
        if number >= 0:
            self.set_display_to_dec_number_at(number, dots, 0, leading_zeros)
        else:
            number = -number
            if number > 9999999:
                TM16XXBase.set_display_to_error(self)
            else:
                self.set_display_to_dec_number_at(number, dots, 1, leading_zeros)
                self.send_char(0, C_MAP['-'], (dots & 0x80) != 0)

    def set_display_to_bin_number(self, number, dots):
        """Set the display to a binary number.

        :param byte, int number: The binary number to set in the display.
        :param bool dots: Set True to turn on dots.
        """
        displays = TM16XXBase._get_displays(self)
        for i in range(0, displays - 1):
            digit = 1
            if (number & (1 << i)) == 0:
                digit = 0

            pos = displays - i - 1
            ldot = (dots & (1 << i)) != 0
            TM16XXBase.set_display_digit(self, digit, pos, ldot)

    def set_color(self, color, pos):
        """Set the color of the character or digit at the specified position.

        :param int color: The color to set the character/digit to.
        :param int pos: The position of the character/digit to change the
        color of.
        """
        TM16XXBase.send_data(self, ((pos << 1) + 1), color)

    def get_push_buttons(self):
        """Get a byte representing the buttons pushed.

        :returns: The push buttons.
        :rtype: byte, int
        """
        keys = 0
        strobe = TM16XXBase._get_strobe(self)
        strobe.write(pin_state.HIGH)
        TM16XXBase.send(self, 0x42)
        for i in range(0, 3):
            keys |= TM16XXBase.receive(self) << i

        strobe.write(pin_state.LOW)
        return keys
