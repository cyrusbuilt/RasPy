"""This module provides the LCD base type."""


from raspy import string_utils
from raspy.invalid_operation_exception import InvalidOperationException
from raspy.components.component import Component
from raspy.components.lcd_display import lcd_text_alignment


class Lcd(Component):
    """An LCD display device abstraction component base type."""

    def __init__(self):
        """Initialize a new instance of Lcd."""
        Component.__init__(self)

    @property
    def row_count(self):
        """Get the number of rows supported by the display.

        :returns: The number of supported rows.
        :rtype: int
        """
        return 0

    @property
    def column_count(self):
        """Get the number of columns supported by the display.

        :returns: The number of supported columns.
        :rtype: int
        """
        return 0

    def _validate_row_index(self, row=0):
        """Validate the index of the specified row.

        :param int row: The index of the row to validate.
        :raises: raspy.invalid_operation_exception.InvalidOperationException if
        the row index is invalid for the display.
        """
        if row >= self.row_count or row < 0:
            raise InvalidOperationException("Invalid row index.")

    def _validate_column_index(self, column=0):
        """Validate the index of the specified column.

        :param int column: The index of the column to validate.
        :raises: raspy.invalid_operation_exception.InvalidOperationException if
        the column index is invalid for the display.
        """
        if column >= self.column_count or column < 0:
            raise InvalidOperationException("Invalid column index.")

    def _validate_coordinates(self, row, column):
        """Validate the specified coordinates.

        :param int row: The index of the row to validate.
        :param int column: The index of the column to validate.
        :raises: raspy.invalid_operation_exception.InvalidOperationException if
        the row or column index is invalid for the display.
        """
        self._validate_row_index(row)
        self._validate_column_index(column)

    def clear(self, row=None, column=None, length=None):
        """Clear one or more characters starting at the specified position.

        Can also be used to clear an entire row or the entire display. If
        only the row is specified, then just that row will be cleared. If
        no parameters are given, then the whole display is cleared.

        :param int row: The number of the row (zero-based) to clear the
        character(s) from.
        :param int column: The column (zero-based) that is the starting
        position.
        :param int length: The number of characters to clear. If zero or not
        specified, then assumes remainder of the row.
        """
        if row is None or row < 0:
            row = 0

        if column is None or column < 0:
            column = 0

        if column:
            pass  # TODO doesn't look like we actually use this.

        if length is None or length < 0:
            length = self.column_count

        sb = string_utils.EMPTY
        for i in range(row, length):
            sb += " "

        self._validate_row_index(row)
        for j in range(row, self.row_count):
            self.write_string(j, sb, lcd_text_alignment.LEFT)

    def set_cursor_position(self, row=0, column=0):
        """Position the cursor at the specified column and row.

        If only the row is given, then the cursor is placed at the beginning
        of the specified row.

        :param int row: The number of the row to position the cursor in.
        :param int column: The number of the column in the specified row to
        position the cursor.
        """
        msg = "Method set_cursor_position(row, column) not implemented."
        raise NotImplementedError(msg)

    def send_cursor_home(self):
        """Sends the cursor to the home position.

        The home position is in the top-left corner (column 0, row 0).
        """
        self.set_cursor_position(0, 0)

    def write_single_byte(self, data):
        """Write a single byte of data to the display.

        :param int data: The byte to send.
        """
        msg = "Method write_single_byte(data) not implemented."
        raise NotImplementedError(msg)

    def write_single_char(self, char):
        """Write a single character to the display.

        :param chr char: A single character to write.
        """
        self.write_single_byte(ord(char))

    def write_byte(self, row, column, data):
        """Write the specified byte to the display at the specified position.

        :param int row: The row to position the data in.
        :param int column: The column within the row to start the write.
        :param int data: The byte to write.
        :raises: raspy.invalid_operation_exception.InvalidOperationException if
        the row or column index is invalid for the display.
        """
        self._validate_coordinates(row, column)
        self.set_cursor_position(row, column)
        self.write_single_byte(data)

    def write_bytes(self, row, column, data_buf):
        """Write the specified byte buffer to the display.

        The buffer is written to the display at the specified position.

        :param int row: The row to position the data in.
        :param int column: The column within the row to start the write.
        :param list data_buf: The list of bytes to write to the display.
        :raises: raspy.invalid_operation_exception.InvalidOperationException if
        the row or column index is invalid for the display.
        """
        self._validate_coordinates(row, column)
        self.set_cursor_position(row, column)
        for i in range(0, len(data_buf) - 1):
            self.write_single_byte(data_buf[i])

    def write_char(self, row, column, char):
        """Write a single character to the display at the specified position.

        :param int row: The row to position the character in.
        :param int column: The column within the row to start the write.
        :param chr char: The character to write.
        :raises: raspy.invalid_operation_exception.InvalidOperationException if
        the row or column index is invalid for the display.
        """
        self._validate_coordinates(row, column)
        self.set_cursor_position(row, column)
        self.write_single_char(char)

    def write_chars(self, row, column, char_buf):
        """Write the specified character buffer to the display.

        :param int row: The row to position the data in.
        :param int column: The column within the row to start the write.
        :param list char_buf: The list of characters to write to the display.
        :raises: raspy.invalid_operation_exception.InvalidOperationException if
        the row or column index is invalid for the display.
        """
        self._validate_coordinates(row, column)
        self.set_cursor_position(row, column)
        for char in char_buf:
            self.write_single_char(char)

    def write_string(self, row, string, alignment):
        """Write text to the display in the specified row.

        :param int row: The row to write the text in.
        :param str string: The text string to write.
        :param int alignment: The text alignment within the row.
        :raises: raspy.invalid_operation_exception.InvalidOperationException if
        the row or column index is invalid for the display.
        """
        # Compute column index.
        col_index = 0
        if (alignment != lcd_text_alignment.LEFT and
            len(string) < self.column_count):
            remaining = self.column_count - len(string)
            if alignment == lcd_text_alignment.RIGHT:
                col_index = remaining
            elif alignment == lcd_text_alignment.CENTER:
                col_index = remaining / 2

        # Validate and set cursor position.
        self._validate_coordinates(row, col_index)
        self.set_cursor_position(row, col_index)

        # Write out each character of the string.
        chars = string.split()
        for char in chars:
            self.write_single_char(char)

    def write_line_aligned(self, row, string, alignment):
        """Write the specified string to the display then carriage returns.

        :param int row: The row to write the string in.
        :param str string: The text string to write.
        :param int alignment: The text alignment within the row.
        :raises: raspy.invalid_operation_exception.InvalidOperationException if
        the row or column index is invalid for the display.
        """
        self.write_string(row, string, alignment)
        self.set_cursor_position(row + 1, 0)

    def write_line(self, row, string):
        """Write the data to the display (aligned left) then carriage returns.

        :param int row: The row to write the string in.
        :param str string: The text string to write.
        :raises: raspy.invalid_operation_exception.InvalidOperationException if
        the row or column index is invalid for the display.
        """
        self.write_line_aligned(row, string, lcd_text_alignment.LEFT)
