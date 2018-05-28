"""Base class for the TM1638/TM1640 board.

TM16XXBase.py

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
from RasPy.ArgumentNullException import ArgumentNullException
from RasPy.Disposable import Disposable
from RasPy.IO import PinState


C_MAP = [
    [' ', StringUtils.convert_string_to_byte("00000000")]
    ['!', StringUtils.convert_string_to_byte("10000110")],
    ['"', StringUtils.convert_string_to_byte("00100010")],
    ['#', StringUtils.convert_string_to_byte("01111110")],
    ['$', StringUtils.convert_string_to_byte("01101101")],
    ['%', StringUtils.convert_string_to_byte("00000000")],
    ['&', StringUtils.convert_string_to_byte("00000000")],
    ['\'', StringUtils.convert_string_to_byte("00000010")],
    ['(', StringUtils.convert_string_to_byte("00110000")],
    [')', StringUtils.convert_string_to_byte("00000110")],
    ['*', StringUtils.convert_string_to_byte("01100011")],
    ['+', StringUtils.convert_string_to_byte("00000000")],
    [',', StringUtils.convert_string_to_byte("00000100")],
    ['-', StringUtils.convert_string_to_byte("01000000")],
    ['.', StringUtils.convert_string_to_byte("10000000")],
    ['/', StringUtils.convert_string_to_byte("01010010")],
    ['0', StringUtils.convert_string_to_byte("00111111")],
    ['1', StringUtils.convert_string_to_byte("00000110")],
    ['2', StringUtils.convert_string_to_byte("01011011")],
    ['3', StringUtils.convert_string_to_byte("01001111")],
    ['4', StringUtils.convert_string_to_byte("01100110")],
    ['5', StringUtils.convert_string_to_byte("01101101")],
    ['6', StringUtils.convert_string_to_byte("01111101")],
    ['7', StringUtils.convert_string_to_byte("00100111")],
    ['8', StringUtils.convert_string_to_byte("01111111")],
    ['9', StringUtils.convert_string_to_byte("01101111")],
    [':', StringUtils.convert_string_to_byte("00000000")],
    [';', StringUtils.convert_string_to_byte("00000000")],
    ['<', StringUtils.convert_string_to_byte("00000000")],
    ['=', StringUtils.convert_string_to_byte("01001000")],
    ['>', StringUtils.convert_string_to_byte("00000000")],
    ['?', StringUtils.convert_string_to_byte("01010011")],
    ['@', StringUtils.convert_string_to_byte("01011111")],
    ['A', StringUtils.convert_string_to_byte("01110111")],
    ['B', StringUtils.convert_string_to_byte("01111111")],
    ['C', StringUtils.convert_string_to_byte("00111001")],
    ['D', StringUtils.convert_string_to_byte("00111111")],
    ['E', StringUtils.convert_string_to_byte("01111001")],
    ['F', StringUtils.convert_string_to_byte("01110001")],
    ['G', StringUtils.convert_string_to_byte("00111101")],
    ['H', StringUtils.convert_string_to_byte("01110110")],
    ['I', StringUtils.convert_string_to_byte("00000110")],
    ['J', StringUtils.convert_string_to_byte("00011111")],
    ['K', StringUtils.convert_string_to_byte("01101001")],
    ['L', StringUtils.convert_string_to_byte("00111000")],
    ['M', StringUtils.convert_string_to_byte("00010101")],
    ['N', StringUtils.convert_string_to_byte("00110111")],
    ['O', StringUtils.convert_string_to_byte("00111111")],
    ['P', StringUtils.convert_string_to_byte("01110011")],
    ['Q', StringUtils.convert_string_to_byte("01100111")],
    ['R', StringUtils.convert_string_to_byte("00110001")],
    ['S', StringUtils.convert_string_to_byte("01101101")],
    ['T', StringUtils.convert_string_to_byte("01111000")],
    ['U', StringUtils.convert_string_to_byte("00111110")],
    ['V', StringUtils.convert_string_to_byte("00101010")],
    ['W', StringUtils.convert_string_to_byte("00011101")],
    ['X', StringUtils.convert_string_to_byte("01110110")],
    ['Y', StringUtils.convert_string_to_byte("01101110")],
    ['Z', StringUtils.convert_string_to_byte("01011011")],
    ['[', StringUtils.convert_string_to_byte("00111001")],
    ['\\', StringUtils.convert_string_to_byte("01100100")],
    [']', StringUtils.convert_string_to_byte("00001111")],
    ['^', StringUtils.convert_string_to_byte("00000000")],
    ['_', StringUtils.convert_string_to_byte("00001000")],
    ['`', StringUtils.convert_string_to_byte("00100000")],
    ['a', StringUtils.convert_string_to_byte("01011111")],
    ['b', StringUtils.convert_string_to_byte("01111100")],
    ['c', StringUtils.convert_string_to_byte("01011000")],
    ['d', StringUtils.convert_string_to_byte("01011110")],
    ['e', StringUtils.convert_string_to_byte("01111011")],
    ['f', StringUtils.convert_string_to_byte("00110001")],
    ['g', StringUtils.convert_string_to_byte("01101111")],
    ['h', StringUtils.convert_string_to_byte("01110100")],
    ['i', StringUtils.convert_string_to_byte("00000100")],
    ['j', StringUtils.convert_string_to_byte("00001110")],
    ['k', StringUtils.convert_string_to_byte("01110101")],
    ['l', StringUtils.convert_string_to_byte("00110000")],
    ['m', StringUtils.convert_string_to_byte("01010101")],
    ['n', StringUtils.convert_string_to_byte("01010100")],
    ['o', StringUtils.convert_string_to_byte("01011100")],
    ['p', StringUtils.convert_string_to_byte("01110011")],
    ['q', StringUtils.convert_string_to_byte("01100111")],
    ['r', StringUtils.convert_string_to_byte("01010000")],
    ['s', StringUtils.convert_string_to_byte("01101101")],
    ['t', StringUtils.convert_string_to_byte("01111000")],
    ['u', StringUtils.convert_string_to_byte("00011100")],
    ['v', StringUtils.convert_string_to_byte("00101010")],
    ['w', StringUtils.convert_string_to_byte("00011101")],
    ['x', StringUtils.convert_string_to_byte("01110110")],
    ['y', StringUtils.convert_string_to_byte("01101110")],
    ['z', StringUtils.convert_string_to_byte("01000111")],
    ['{', StringUtils.convert_string_to_byte("01000110")],
    ['|', StringUtils.convert_string_to_byte("00000110")],
    ['}', StringUtils.convert_string_to_byte("01110000")],
    ['~', StringUtils.convert_string_to_byte("00000001")]
]
"""The character map for the seven segment display.

    The bits are displayed by mapping below:
    -- 0 --
    |     |
    5     1
    __ 6 __
    4     2
    |     |
    -- 3 -- .7
"""


class TM16XXBase(Disposable):
    """Base class for the TM1638/TM1640 board.

    This class is the base class for the TM1638/TM1640 board.
    It is a port of the TM1638 library by Ricardo Batista
    URL: http://code.google.com/p/tm1638-library/
    """

    __is_active = False
    __data = None
    __clock = None
    __strobe = None
    __displays = 0

    def __init__(self, data, clock, strobe, displays, activate, intensity):
        """Initializes a new instance of the RasPy.LED.TM16XXBase class.

        Initializes the class with the data, clock, and strobe pins, the number
        of characters to display, whether or not the display should be
        activated on init, and the brightness level.

        :param data: The data pin.
        :param clock: The clock pin.
        :param strobe: The strobe pin.
        :param displays: The number of characters to display.
        :param activate: Set True to activate the display.
        :param intensity: The display intensity (brightness) level.
        :type data: RasPy.IO.RaspiGpio.RaspiGpio
        :type clock: RasPy.IO.RaspiGpio.RaspiGpio
        :type strobe: RasPy.IO.RaspiGpio.RaspiGpio
        :type displays: int
        :type activate: boolean
        :type intensity: int
        :raises: RasPy.ArgumentNullException if the data, clock, or strobe pins
        are None or undefined.
        """
        super(Disposable, self).__init__()
        self.__data = data
        if self.__data is None:
            raise ArgumentNullException("'data' param cannot be None.")

        self.__clock = clock
        if self.__clock is None:
            raise ArgumentNullException("'clock' param cannot be None.")

        self.__strobe = strobe
        if self.__strobe is None:
            raise ArgumentNullException("'strobe' param cannot be None.")

        # TODO what is the acceptable range?
        self.__displays = displays

        self.__data.provision()
        self.__clock.provision()
        self.__strobe.provision()
        self.__strobe.write(PinState.HIGH)
        self.__clock.write(PinState.HIGH)

        # TODO what is the acceptable range of intensity?
        self.send_command(0x40)
        active_value = 0x00
        if activate:
            active_value = 0x08
        self.send_command((0x80 | active_value) | min(7, intensity))

        self.__strobe.write(PinState.LOW)
        self.send(0xC0)
        for i in range(0, 15):
            self.send(0x00)

        self.__strobe.write(PinState.HIGH)

    def send(self, data):
        """Send the specified data to the display

        :param data: The byte of data to send.
        :type data: byte, int
        """
        for i in range(0, 7):
            self.__clock.write(PinState.LOW)
            send_val = PinState.LOW
            if (data & 1) > 0:
                send_val = PinState.HIGH
            self.__data.write(send_val)
            data >>= 1
            self.__clock.write(PinState.HIGH)

    def send_command(self, cmd):
        """Send the command.

        :param cmd: A byte representing the command.
        :type cmd: byte, int
        """
        self.__strobe.write(PinState.LOW)
        self.send(cmd)
        self.__strobe.write(PinState.HIGH)

    @property
    def is_active(self):
        """Get a value indicating whether or not the display is active.

        :returns: True if the display is active; Otherwise, False.
        :rtype: boolean
        """
        return self.__is_active

    def _get_displays(self):
        """Get the number of display characters.

        :returns: The number of characters to display.
        :rtype: int
        """

    def _get_strobe(self):
        """Get the strobe pin.

        :returns: The strobe pin.
        :rtype: RasPy.IO.RaspiGpio.RaspiGpio
        """
        return self.__strobe

    def receive(self):
        """Receive data from the display driver.

        :returns: The byte received.
        :rtype: byte, int
        """
        # Pull up on.
        temp = 0
        self.__data.write(PinState.HIGH)
        for i in range(0, 7):
            temp >>= 1
            self.__clock.write(PinState.LOW)
            if self.__data.read() == PinState.HIGH:
                temp |= 0x80

            self.__clock.write(PinState.HIGH)

        self.__data.write(PinState.LOW)
        return temp

    def send_data(self, address, data):
        """Send the specified data to the device.

        :param address: The address to write the data at.
        :param data: The data to send.
        :type address: byte, int
        :type data: byte, int
        """
        self.send_command(0x44)
        self.__strobe.write(PinState.LOW)
        self.send(0xC0 | address)
        self.send(data)
        self.__strobe.write(PinState.HIGH)

    def clear_display(self):
        """Clear the display."""
        for i in range(0, self.__displays - 1):
            self.send_data((i << 1), 0)

    def send_char(self, pos, data, dot):
        """Send the specified character to the display.

        :param pos: The position to set the character at.
        :param data: The character data to send.
        :param dot: Set True to enable the dot.
        :type pos: byte, int
        :type data: byte, int
        :type dot: boolean
        """
        pass

    def set_display_to_string(self, string, dots=False, pos=0):
        """Set the display to the specified string.

        :param string: The string to set the display to.
        :param dots: Set True to turn on dots.
        :param pos: The character position to start the string at.
        :type string: string
        :type dots: boolean
        :type pos: byte, int
        """
        if StringUtils.is_null_or_empty(string):
            self.clear_display()
            return

        global C_MAP
        length = len(string)
        for i in range(0, self.__displays - 1):
            if i < length:
                lpos = i + pos
                ldata = C_MAP[string[i]]
                ldot = (dots & (1 << (self.__displays - i - 1))) != 0
                self.send_char(lpos, ldata, ldot)
            else:
                break

    def set_display(self, values, size):
        """Set the display to the specified value.

        :param values: The values to set to the display (byte array).
        :param size: The number of values in the specified array (starting at
        0) to use. Just specify len(<values array>) to use the whole buffer.
        :type values: list
        :type size: int
        """
        for i in range(0, size - 1):
            self.send_char(i, values[i], False)

    def clear_display_digit(self, pos, dot):
        """Clear the display digit.

        :param pos: The position to start clearing the display at.
        :param dot: Set True to clear dots.
        :type pos: byte, int
        :type dot: boolean
        """
        self.send_char(pos, 0, dot)

    def set_display_to_error(self):
        """Set the display to error."""
        global C_MAP
        err = [
            C_MAP['E'],
            C_MAP['r'],
            C_MAP['r'],
            C_MAP['o'],
            C_MAP['r']
        ]

        self.set_display(err, 5)
        for i in range(8, self.__displays - 1):
            self.clear_display_digit(i, False)

    def set_display_digit(self, digit, pos, dot):
        """Set the specified digit in the display.

        :param digit: The digit to set.
        :param pos: The position to set the digit at.
        :param dot: Set True to turn on the dot.
        :type digit: byte, int
        :type pos: byte, int
        :type dot: boolean
        """
        global C_MAP
        chr = str(digit).split()[0]
        if C_MAP[chr]:
            self.send_char(pos, C_MAP[chr], dot)

    def setup_display(self, active, intensity):
        """Set up the display.

        :param active: Set True to activate.
        :param intensity: The display intensity level (brightness).
        :type active: boolean
        :type intensity: int
        """
        active_bit = 0
        if active:
            active_bit = 8
        self.send_command((0x80 | active_bit) | min(7, intensity))

        # Necessary for TM1640
        self.__strobe.write(PinState.LOW)
        self.__clock.write(PinState.LOW)
        self.__clock.write(PinState.HIGH)
        self.__strobe.write(PinState.HIGH)

    def activate_display(self, active):
        """Activate or deactivate the display.

        :param active: Set True to activate; False to deactivate.
        :type active: boolean
        """
        if active:
            if not self.__is_active:
                self.send_command(0x80)
                self.__is_active = True
        else:
            if self.__is_active:
                self.send_command(0x80)
                self.__is_active = False

    def dispose(self):
        """Dispose managed resources.

        In a subclass, performs application-defined tasks associated with
        freeing, releasing, or resetting resources.
        """
        if self.is_disposed:
            return

        self.activate_display(False)
        if self.__clock is not None:
            self.__clock.dispose()
            self.__clock = None

        if self.__data is not None:
            self.__data.dispose()
            self.__data = None

        if self.__strobe is not None:
            self.__strobe.dispose()
            self.__strobe = None

        Disposable.dispose(self)
