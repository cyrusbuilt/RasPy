"""Hitachi HD44780-based LCD module control class."""


import itertools
from raspy.disposable import Disposable
from raspy.illegal_argument_exception import IllegalArgumentException
from raspy.lcd import display_entry_modes
from raspy.lcd import display_on_off_control
from raspy.lcd import function_set_flags
from raspy.lcd import lcd_commands
from raspy.lcd.lcd_transfer_provider import LcdTransferProvider
from raspy.io import pin_state
from raspy.pi_system import core_utils


class LcdModule(Disposable):
    """Hitachi HD44780-based LCD module control class.

    This is largely derived from:
    Micro Liquid Crystal Library
    http://microliquidcrystal.codeplex.com
    Apache License Version 2.0
    This class uses the LcdTransferProvider to provide
    an interface between the Raspberry Pi and the LCD
    module via GPIO.
    """

    __rowOffsets = [0x00, 0x40, 0x14, 0x54]
    __provider = None
    __showCursor = True
    __blinkCursor = True
    __visible = True
    __backlight = True
    __numLines = 0
    __numColumns = 0
    __displayFunction = 0
    __sendQueue = list()
    __ready = False
    # __autoScroll = False  # TODO implement this?
    # __currLine = 0        # TODO implement this?

    def __init__(self, provider):
        """Initialize a new instance of raspy.lcd.lcd_module.LcdModule class.

        :param raspy.lcd.lcd_transfer_provider.LcdTransferProvider provider:
        The transfer provider to use to send data and commands to the display.
        :raises: raspy.illegal_argument_exception.IllegalArgumentException if
        the provider is None or not an instance of LcdTransferProvider.
        """
        super(Disposable, self).__init__()
        if provider is None or not isinstance(provider, LcdTransferProvider):
            msg = "'provider' param bust be an LcdTransferProvider"
            raise IllegalArgumentException(msg)

        self.__provider = provider
        if self.__provider.is_four_bit_mode:
            self.__displayFunction = (function_set_flags.FOUR_BIT_MODE |
                                      function_set_flags.ONE_LINE |
                                      function_set_flags.FIVE_BY_EIGHT_DOTS)
        else:
            self.__displayFunction = (function_set_flags.EIGHT_BIT_MODE |
                                      function_set_flags.ONE_LINE |
                                      function_set_flags.FIVE_BY_EIGHT_DOTS)

    @property
    def rows(self):
        """Get the number of rows.

        :returns: The number of rows.
        :rtype: int
        """
        return self.__numLines

    @property
    def columns(self):
        """Get the number of columns.

        :returns: The number of columns.
        :rtype: int
        """
        return self.__numColumns

    @property
    def provider(self):
        """Get the LCD transfer provider.

        :returns: The data transfer provider.
        :rtype: raspy.lcd.lcd_transfer_provider.LcdTransferProvider
        """
        return self.__provider

    def send_command(self, data):
        """Send a command to the display.

        :param byte, int data: The data or command to send.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        self.__provider.send(data, pin_state.LOW, self.__backlight)

    def _update_display_control(self):
        """Update the display control.

        This method should be called whenever any of the display properties
        are changed.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        command = lcd_commands.DISPLAY_CONTROL
        if self.__visible:
            command |= display_on_off_control.DISPLAY_ON
        else:
            command |= display_on_off_control.DISPLAY_OFF

        if self.__showCursor:
            command |= display_on_off_control.CURSOR_ON
        else:
            command |= display_on_off_control.CURSOR_OFF

        if self.__blinkCursor:
            command |= display_on_off_control.BLINK_ON
        else:
            command |= display_on_off_control.BLINK_OFF

        # NOTE backlight is updated with each command.
        self.send_command(command)

    @property
    def show_cursor(self):
        """Get a flag indicating whether or not to show the cursor.

        :returns: True if the cursor is shown: Otherwise, False.
        :rtype: bool
        """
        return self.__showCursor

    @show_cursor.setter
    def show_cursor(self, show):
        """Set a flag indicating whether or not to show the cursor.

        :param bool show: Set True to show the cursor.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.__showCursor != show:
            self.__showCursor = show
            self._update_display_control()

    @property
    def blink_cursor(self):
        """Get a flag indicating whether or not to blink the cursor.

        :returns: True if cursor blink is enabled.
        :rtype: bool
        """
        return self.__blinkCursor

    @blink_cursor.setter
    def blink_cursor(self, blink):
        """Set a flag indicating whether or not to blink the cursor.

        :param bool blink: Set True to enable cursor blink.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.__blinkCursor != blink:
            self.__blinkCursor = blink
            self._update_display_control()

    @property
    def visible(self):
        """Get a flag indicating whether or not the display is turned on.

        :returns: True if the display is on.
        :rtype: bool
        """
        return self.__visible

    @visible.setter
    def visible(self, vis):
        """Set a flag indicating whether or not the display should be on.

        :param bool vis: Set True to turn the display on.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.__visible != vis:
            self.__visible = vis
            self._update_display_control()

    @property
    def backlight_enable(self):
        """Get a flag indicating whether or not the backligh is enabled.

        :returns: True if the backlight is enabled.
        :rtype: bool
        """
        return self.__backlight

    @backlight_enable.setter
    def backlight_enable(self, enabled):
        """Set a flag indicating whether or not the backlight is enabled.

        :param bool enabled: Set True to enable the backlight.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.__backlight != enabled:
            self.__backlight = enabled
            self._update_display_control()

    def write_byte(self, data):
        """Send data byte to the display.

        :param: byte, int data: The data to send.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        self.__provider.send(data, pin_state.HIGH, self.__backlight)

    def create_char(self, location, char_map, offset):
        """Create a custom character (glyph) for use on the LCD.

        Up to eight characters of 5x8 pixels are supported (numbered 0 - 7).
        The appearance of each custom character is specified by an array of
        eight bytes, one for each row. The five least significant bits of
        each byte determine the pixels in that row. To display a custom
        character on the screen, call write_byte() and pass its number.

        :param int location: Which character to create (0 - 7).
        :param list char_map: The character's pixel data.
        :param int offset: Offset in the char_map where character data is
        found.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        location &= 0x07  # We only have 8 locations (0 - 7).
        if offset is None:
            offset = 0

        cmd = lcd_commands.SET_CG_RAM_ADDR | (location << 3)
        self.send_command(cmd)
        for i in range(0, 7):
            self.write_byte(char_map[offset + i])

    def write(self, buf, offset, count):
        """Write a specified number of bytes to the LCD using a data buffer.

        :param list buf: The byte array containing data to write to the
        display.
        :param int offset: The zero-based byte offset in the buffer at which
        to begin copying data.
        :param int count: The number of bytes to write.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        len = offset + count
        for i in range(offset, len):
            self.write_byte(buf[i])

    def write_string(self, string):
        """Write text to the LCD.

        :param str string: The text to display.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        buf = [elem.encode("hex") for elem in string]
        self.write(buf, 0, len(buf))

    def move_cursor(self, right):
        """Move the cursor left or right.

        :param bool right: Set True to move the cursor right; False to move
        left.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        pos = 0x00
        if right:
            pos = 0x04

        self.send_command(0x10 | pos)

    def scroll_display_right(self):
        """Scroll the display (text and cursor) one space right.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        self.send_command(0x18 | 0x04)

    def scroll_display_left(self):
        """Scroll the display (text and cursor) one space left.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        self.send_command(0x18 | 0x00)

    def set_cursor_position(self, column, row):
        """Position the LCD cursor.

        Set the location at which subsequent text written to the LCD will be
        displayed.

        :param int column: The column position.
        :param int row: The row position.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if row > self.__numLines:
            row = self.__numLines - 1

        address = column + self.__rowOffsets[row]
        self.send_command(lcd_commands.SET_DD_RAM_ADDR | address)

    def return_home(self):
        """Position the cursor in the upper-left of the LCD (home position).

        Use the home position in outputting subsequent text to the display.
        To also clear the display, use the clear() method instead.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        self.send_command(lcd_commands.RETURN_HOME)
        core_utils.sleep_microseconds(2000)   # This command takes some time.

    def clear(self):
        """Clear the LCD screen and return the cursor to home position.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        self.send_command(lcd_commands.CLEAR_DISPLAY)
        core_utils.sleep_microseconds(2000)   # This command takes some time.

    def _process_send_queue(self, timeout):
        """Process commands to be sent from the queue synchronously.

        Commands are sent sequentially.

        :param int timeout: The amount of time to wait between executions
        in milliseconds.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if (not self.__ready or
                self.__sendQueue is None or
                len(self.__sendQueue) == 0):
            return

        self.__ready = False
        if timeout is None:
            timeout = 0

        # TODO should we do this in a thread?
        for _ in itertools.repeat(None, len(self.__sendQueue)):
            cmd = self.__sendQueue.pop(0)   # Grab the first item in the queue.
            if cmd is not None:
                self.send_command(cmd)
                core_utils.sleep(timeout)

        self.__ready = True

    def _enqueue_command(self, cmd, timeout):
        """Queue a command to be sent to the display.

        :param byte, int cmd: The command or data to send.
        :param int timeout: The amount of time in milliseconds to wait before
        executing the command.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.__sendQueue is None:
            self.__sendQueue = list()

        self.__sendQueue.append(cmd)
        self._process_send_queue(timeout)

    def begin(self, columns, lines, left_to_right, dot_size):
        """Initialize the LCD.

        This also specifies dimensions (width and height) of the display.

        :param int columns: The number of columns that the display has.
        :param int lines: The number of rows the display has.
        :param bool left_to_right: Is set True, left to right versus right to
        left.
        :param bool dot_size: If set True and only one line set, then the
        font size will be set 10px high.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if lines > 1:
            self.__displayFunction |= function_set_flags.TWO_LINE

        if left_to_right is None:
            left_to_right = True

        if dot_size is None:
            dot_size = False

        self.__numLines = lines
        self.__numColumns = columns

        # For some 1 line displays, you can select 10px high font.
        if dot_size and lines == 1:
            self.__displayFunction |= function_set_flags.FIVE_BY_EIGHT_DOTS

        # LCD controller needs time to warm-up.
        self._enqueue_command(None, 50)

        # rs, rw, and enable should be low by default.
        if self.__provider.is_four_bit_mode:
            # This is according to the Hitachi HD44780 datasheet.
            # figure 24, pg 46

            # we start in 8-bit mode, try to set to 4-bit mode.
            self.send_command(0x03)
            self._enqueue_command(0x03, 5)  # Wait minimum 4.1 ms.
            self._enqueue_command(0x03, 5)
            self._enqueue_command(0x02, 5)  # Finally, set to 4-bit interface.
        else:
            # This is according to the Hitachi HD44780 datasheet
            # page 45, figure 23

            # Send function set command sequence.
            cmd = lcd_commands.FUNCTION_SET | self.__displayFunction
            self.send_command(cmd)
            self._enqueue_command(cmd, 5)
            self._enqueue_command(cmd, 5)

        # Finally, set # of lines, font size, etc.
        cmd = lcd_commands.FUNCTION_SET | self.__displayFunction
        self._enqueue_command(cmd, 0)

        # Turn the display on with no cursor or blinking by default.
        self.__visible = True
        self.__showCursor = False
        self.__blinkCursor = False
        self.__backlight = True
        self._update_display_control()

        # Clear it off.
        self.clear()

        # Set entry mode.
        display_mode = display_entry_modes.ENTRY_RIGHT
        if left_to_right:
            display_mode = display_entry_modes.ENTRY_LEFT

        display_mode |= display_entry_modes.ENTRY_SHIFT_DECREMENT
        self.send_command(lcd_commands.ENTRY_MODE_SET | display_mode)

    def dispose(self):
        """Release all managed resources used by this instance."""
        if self.is_disposed:
            return

        if self.__provider is not None:
            self.__provider.dispose()
            self.__provider = None

        Disposable.dispose(self)
