"""Controller class for the TM1638/TM1640 board.

TM1638.py

Author:
      Chris Brunner <cyrusbuilt at gmail dot com>

  Copyright (c) 2015 CyrusBuilt

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
"""


from RasPy import StringUtils
from RasPy.IO import PinState
from RasPy.IO.RaspiGpio import RaspiGpio
from RasPy.LED.TM16XXBase import TM16XXBase
from RasPy.LED.TM16XXBase import C_MAP


class TM1638(TM16XXBase):
    """Controller class for the TM1638/TM1640 board.

    It is a port of the TM1638 library by Ricardo Batista
    URL: http://code.google.com/p/tm1638-library/
    """

    def __init__(self, data, clock, strobe, active, intensity):
        """Initialize a new instance of the RasPy.LED.TM1638 class.

        Initialize with the pins for data, clock, and strobe, a flag indicating
        whether or not the display should be active, and the intensity level.

        :param data: The data pin.
        :param clock: The clock pin.
        :param strobe: The strobe pin.
        :param active: Set True to activate the display.
        :param intensity: The display intensity (brightness) level.
        :type data: RasPy.IO.RaspiGpio.RaspiGpio
        :type clock: RasPy.IO.RaspiGpio.RaspiGpio
        :type strobe: RasPy.IO.RaspiGpio.RaspiGpio
        :type activate: boolean
        :type intensity: int
        :raises: RasPy.ArgumentNullException if the data, clock, or strobe pins
        are None or undefined.
        """
        TM16XXBase.__init__(self, data, clock, strobe, 8, active, intensity)

    def set_display_to_hex_number(self, number):
        """Set the display to a hex number.

        :param number: An unsigned long number to display (gets converted to
        hex.
        :type number: int
        """
        TM16XXBase.set_display_to_string(self, "{0:x}".format(number))

    def set_display_to_dec_number_at(self, number, dots, start_pos, leading_zeros):
        """Set the display to a decimal number at the starting positiion.

        :param number: The number to display (if out of range, the display will
        be cleared).
        :param dots: Set True to turn on dots.
        :param start_pos: The starting position to display the number at.
        :param leading_zeros: Set True to lead the number with zeroes.
        :type number: int
        :type dots: boolean
        :type start_pos: int
        :type leading_zeros: boolean
        """
        if number > 99999999:
            TM16XXBase.set_display_to_error(self)

        displays = TM16XXBase._get_displays(self)
        for i in range(0, (displays - start_pos) - 1):
            pos = (displays - i - 1)
            ldot = ((dots & (1 << i)) != 0)
            if number != 0:
                digit = number % 10
                TM16XXBase.set_display_digit(self, digit, pos, ldot)
                number /= 10
            else:
                if leading_zeros:
                    digit = 0
                    TM16XXBase.set_display_digit(self, digit, pos, ldot)
                else:
                    TM16XXBase.clear_display_digit(self, pos, ldot)

    def set_display_to_dec_number(self, number, dots, leading_zeros):
        """Set the display to a decimal number.

        :param number: The number to display (if out of range, the display will
        be cleared).
        :param dots: Set True to turn on dots.
        :param leading_zeros: Set True to lead the number with zeroes.
        :type number: int
        :type dots: boolean
        :type leading_zeros: boolean
        """
        self.set_display_to_dec_number_at(number, dots, 0, leading_zeros)

    def send_char(self, pos, data, dot):
        """Send a character to the display.

        :param pos: The position at which to set the character.
        :param data: The data (character) to set in the display.
        :param dot: Set True to turn on the dots.
        :type pos: byte, int
        :type data: byt, int
        :type dot: bool
        """
        address = pos << 1
        one = StringUtils.convert_string_to_byte("10000000")
        zero = StringUtils.convert_string_to_byte("00000000")
        dot_char = zero
        if dot:
            dot_char = one

        ldata = data | dot_char
        TM16XXBase.send_data(self, address, ldata)

    def set_display_to_signed_dec_number(self, number, dots, leading_zeros):
        """Set the display to a signed decimal number.

        :param number: The signed decimal number to set in the display.
        :param dots: Set True to turn on dots.
        :param leading_zeros: Set True to lead the number with zeros.
        :type number: int
        :type dots: bool
        :type leading_zeros: bool
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

        :param number:
        :param dots:
        :type number: byte, int
        :type dots: bool
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

        :param color: The color to set the character/digit to.
        :param pos: The position of the character/digit to change the color of.
        :type color: int
        :type pos: int
        """
        TM16XXBase.send_data(self, ((pos << 1) + 1), color)

    def get_push_buttons(self):
        """Get a byte representing the buttons pushed.

        :returns:
        :rtype:
        """