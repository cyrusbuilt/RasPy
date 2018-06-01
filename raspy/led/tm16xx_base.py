"""This module provides the base class for the TM1638/TM1640 board."""


from raspy import string_utils
from raspy.argument_null_exception import ArgumentNullException
from raspy.disposable import Disposable
from raspy.io import pin_state


C_MAP = [
    [' ', string_utils.convert_string_to_byte("00000000")],
    ['!', string_utils.convert_string_to_byte("10000110")],
    ['"', string_utils.convert_string_to_byte("00100010")],
    ['#', string_utils.convert_string_to_byte("01111110")],
    ['$', string_utils.convert_string_to_byte("01101101")],
    ['%', string_utils.convert_string_to_byte("00000000")],
    ['&', string_utils.convert_string_to_byte("00000000")],
    ['\'', string_utils.convert_string_to_byte("00000010")],
    ['(', string_utils.convert_string_to_byte("00110000")],
    [')', string_utils.convert_string_to_byte("00000110")],
    ['*', string_utils.convert_string_to_byte("01100011")],
    ['+', string_utils.convert_string_to_byte("00000000")],
    [',', string_utils.convert_string_to_byte("00000100")],
    ['-', string_utils.convert_string_to_byte("01000000")],
    ['.', string_utils.convert_string_to_byte("10000000")],
    ['/', string_utils.convert_string_to_byte("01010010")],
    ['0', string_utils.convert_string_to_byte("00111111")],
    ['1', string_utils.convert_string_to_byte("00000110")],
    ['2', string_utils.convert_string_to_byte("01011011")],
    ['3', string_utils.convert_string_to_byte("01001111")],
    ['4', string_utils.convert_string_to_byte("01100110")],
    ['5', string_utils.convert_string_to_byte("01101101")],
    ['6', string_utils.convert_string_to_byte("01111101")],
    ['7', string_utils.convert_string_to_byte("00100111")],
    ['8', string_utils.convert_string_to_byte("01111111")],
    ['9', string_utils.convert_string_to_byte("01101111")],
    [':', string_utils.convert_string_to_byte("00000000")],
    [';', string_utils.convert_string_to_byte("00000000")],
    ['<', string_utils.convert_string_to_byte("00000000")],
    ['=', string_utils.convert_string_to_byte("01001000")],
    ['>', string_utils.convert_string_to_byte("00000000")],
    ['?', string_utils.convert_string_to_byte("01010011")],
    ['@', string_utils.convert_string_to_byte("01011111")],
    ['A', string_utils.convert_string_to_byte("01110111")],
    ['B', string_utils.convert_string_to_byte("01111111")],
    ['C', string_utils.convert_string_to_byte("00111001")],
    ['D', string_utils.convert_string_to_byte("00111111")],
    ['E', string_utils.convert_string_to_byte("01111001")],
    ['F', string_utils.convert_string_to_byte("01110001")],
    ['G', string_utils.convert_string_to_byte("00111101")],
    ['H', string_utils.convert_string_to_byte("01110110")],
    ['I', string_utils.convert_string_to_byte("00000110")],
    ['J', string_utils.convert_string_to_byte("00011111")],
    ['K', string_utils.convert_string_to_byte("01101001")],
    ['L', string_utils.convert_string_to_byte("00111000")],
    ['M', string_utils.convert_string_to_byte("00010101")],
    ['N', string_utils.convert_string_to_byte("00110111")],
    ['O', string_utils.convert_string_to_byte("00111111")],
    ['P', string_utils.convert_string_to_byte("01110011")],
    ['Q', string_utils.convert_string_to_byte("01100111")],
    ['R', string_utils.convert_string_to_byte("00110001")],
    ['S', string_utils.convert_string_to_byte("01101101")],
    ['T', string_utils.convert_string_to_byte("01111000")],
    ['U', string_utils.convert_string_to_byte("00111110")],
    ['V', string_utils.convert_string_to_byte("00101010")],
    ['W', string_utils.convert_string_to_byte("00011101")],
    ['X', string_utils.convert_string_to_byte("01110110")],
    ['Y', string_utils.convert_string_to_byte("01101110")],
    ['Z', string_utils.convert_string_to_byte("01011011")],
    ['[', string_utils.convert_string_to_byte("00111001")],
    ['\\', string_utils.convert_string_to_byte("01100100")],
    [']', string_utils.convert_string_to_byte("00001111")],
    ['^', string_utils.convert_string_to_byte("00000000")],
    ['_', string_utils.convert_string_to_byte("00001000")],
    ['`', string_utils.convert_string_to_byte("00100000")],
    ['a', string_utils.convert_string_to_byte("01011111")],
    ['b', string_utils.convert_string_to_byte("01111100")],
    ['c', string_utils.convert_string_to_byte("01011000")],
    ['d', string_utils.convert_string_to_byte("01011110")],
    ['e', string_utils.convert_string_to_byte("01111011")],
    ['f', string_utils.convert_string_to_byte("00110001")],
    ['g', string_utils.convert_string_to_byte("01101111")],
    ['h', string_utils.convert_string_to_byte("01110100")],
    ['i', string_utils.convert_string_to_byte("00000100")],
    ['j', string_utils.convert_string_to_byte("00001110")],
    ['k', string_utils.convert_string_to_byte("01110101")],
    ['l', string_utils.convert_string_to_byte("00110000")],
    ['m', string_utils.convert_string_to_byte("01010101")],
    ['n', string_utils.convert_string_to_byte("01010100")],
    ['o', string_utils.convert_string_to_byte("01011100")],
    ['p', string_utils.convert_string_to_byte("01110011")],
    ['q', string_utils.convert_string_to_byte("01100111")],
    ['r', string_utils.convert_string_to_byte("01010000")],
    ['s', string_utils.convert_string_to_byte("01101101")],
    ['t', string_utils.convert_string_to_byte("01111000")],
    ['u', string_utils.convert_string_to_byte("00011100")],
    ['v', string_utils.convert_string_to_byte("00101010")],
    ['w', string_utils.convert_string_to_byte("00011101")],
    ['x', string_utils.convert_string_to_byte("01110110")],
    ['y', string_utils.convert_string_to_byte("01101110")],
    ['z', string_utils.convert_string_to_byte("01000111")],
    ['{', string_utils.convert_string_to_byte("01000110")],
    ['|', string_utils.convert_string_to_byte("00000110")],
    ['}', string_utils.convert_string_to_byte("01110000")],
    ['~', string_utils.convert_string_to_byte("00000001")]
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
        """Initialize a new instance of the raspy.led.TM16XXBase class.

        Initializes the class with the data, clock, and strobe pins, the
        number of characters to display, whether or not the display should be
        activated on init, and the brightness level.

        :param raspy.io.raspi_gpio.RaspiGpio data: The data pin.
        :param raspy.io.raspi_gpio.RaspiGpio clock: The clock pin.
        :param raspy.io.raspi_gpio.RaspiGpio strobe: The strobe pin.
        :param int displays: The number of characters to display.
        :param bool activate: Set True to activate the display.
        :param int intensity: The display intensity (brightness) level.
        :raises: raspy.argument_null_exception.ArgumentNullException if the
        data, clock, or strobe pins are NonePin or undefined.
        """
        super(Disposable, self).__init__()
        self.__data = data
        if self.__data is None:
            raise ArgumentNullException("'data' param cannot be NonePin.")

        self.__clock = clock
        if self.__clock is None:
            raise ArgumentNullException("'clock' param cannot be NonePin.")

        self.__strobe = strobe
        if self.__strobe is None:
            raise ArgumentNullException("'strobe' param cannot be NonePin.")

        # TODO what is the acceptable range?
        self.__displays = displays

        self.__data.provision()
        self.__clock.provision()
        self.__strobe.provision()
        self.__strobe.write(pin_state.HIGH)
        self.__clock.write(pin_state.HIGH)

        # TODO what is the acceptable range of intensity?
        self.send_command(0x40)
        active_value = 0x00
        if activate:
            active_value = 0x08
        self.send_command((0x80 | active_value) | min(7, intensity))

        self.__strobe.write(pin_state.LOW)
        self.send(0xC0)
        for i in range(0, 15):
            self.send(0x00)

        self.__strobe.write(pin_state.HIGH)

    def send(self, data):
        """Send the specified data to the display.

        :param byte, int data: The byte of data to send.
        """
        for i in range(0, 7):
            self.__clock.write(pin_state.LOW)
            send_val = pin_state.LOW
            if (data & 1) > 0:
                send_val = pin_state.HIGH
            self.__data.write(send_val)
            data >>= 1
            self.__clock.write(pin_state.HIGH)

    def send_command(self, cmd):
        """Send the command.

        :param byte, int cmd: A byte representing the command.
        """
        self.__strobe.write(pin_state.LOW)
        self.send(cmd)
        self.__strobe.write(pin_state.HIGH)

    @property
    def is_active(self):
        """Get a value indicating whether or not the display is active.

        :returns: True if the display is active; Otherwise, False.
        :rtype: bool
        """
        return self.__is_active

    def _get_displays(self):
        """Get the number of display characters.

        :returns: The number of characters to display.
        :rtype: int
        """
        return self.__displays

    def _get_strobe(self):
        """Get the strobe pin.

        :returns: The strobe pin.
        :rtype: raspy.io.raspi_gpio.RaspiGpio
        """
        return self.__strobe

    def receive(self):
        """Receive data from the display driver.

        :returns: The byte received.
        :rtype: byte, int
        """
        # Pull up on.
        temp = 0
        self.__data.write(pin_state.HIGH)
        for i in range(0, 7):
            temp >>= 1
            self.__clock.write(pin_state.LOW)
            if self.__data.read() == pin_state.HIGH:
                temp |= 0x80

            self.__clock.write(pin_state.HIGH)

        self.__data.write(pin_state.LOW)
        return temp

    def send_data(self, address, data):
        """Send the specified data to the device.

        :param byte, int address: The address to write the data at.
        :param byte, int data: The data to send.
        """
        self.send_command(0x44)
        self.__strobe.write(pin_state.LOW)
        self.send(0xC0 | address)
        self.send(data)
        self.__strobe.write(pin_state.HIGH)

    def clear_display(self):
        """Clear the display."""
        for i in range(0, self.__displays - 1):
            self.send_data((i << 1), 0)

    def send_char(self, pos, data, dot):
        """Send the specified character to the display.

        :param byte, int pos: The position to set the character at.
        :param byte, int data: The character data to send.
        :param bool dot: Set True to enable the dot.
        """
        pass

    def set_display_to_string(self, string, dots=False, pos=0):
        """Set the display to the specified string.

        :param string string: The string to set the display to.
        :param bool dots: Set True to turn on dots.
        :param byte, int pos: The character position to start the string at.
        """
        if string_utils.is_null_or_empty(string):
            self.clear_display()
            return

        global C_MAP
        length = len(string)
        for i in range(0, self.__displays - 1):
            if i < length:
                l_pos = i + pos
                l_data = C_MAP[string[i]]
                l_dot = (dots & (1 << (self.__displays - i - 1))) != 0
                self.send_char(l_pos, l_data, l_dot)
            else:
                break

    def set_display(self, values, size):
        """Set the display to the specified value.

        :param list values: The values to set to the display (byte array).
        :param int size: The number of values in the specified array (starting
        at 0) to use. Just specify len(<values array>) to use the whole
        buffer.
        """
        for i in range(0, size - 1):
            self.send_char(i, values[i], False)

    def clear_display_digit(self, pos, dot):
        """Clear the display digit.

        :param byte, int pos: The position to start clearing the display at.
        :param bool dot: Set True to clear dots.
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

        :param byte, int digit: The digit to set.
        :param byte, int pos: The position to set the digit at.
        :param bool dot: Set True to turn on the dot.
        """
        global C_MAP
        char = str(digit).split()[0]
        if C_MAP[char]:
            self.send_char(pos, C_MAP[char], dot)

    def setup_display(self, active, intensity):
        """Set up the display.

        :param bool active: Set True to activate.
        :param int intensity: The display intensity level (brightness).
        """
        active_bit = 0
        if active:
            active_bit = 8
        self.send_command((0x80 | active_bit) | min(7, intensity))

        # Necessary for TM1640
        self.__strobe.write(pin_state.LOW)
        self.__clock.write(pin_state.LOW)
        self.__clock.write(pin_state.HIGH)
        self.__strobe.write(pin_state.HIGH)

    def activate_display(self, active):
        """Activate or deactivate the display.

        :param bool active: Set True to activate; False to deactivate.
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
