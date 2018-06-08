"""This module contains the LcdComponent type."""


from raspy.argument_null_exception import ArgumentNullException
from raspy.illegal_argument_exception import IllegalArgumentException
from raspy.components.lcd_display.lcd import Lcd
from raspy.lcd.lcd_module import LcdModule
from raspy.lcd.lcd_transfer_provider import LcdTransferProvider


class LcdComponent(Lcd):
    """An LCD display device abstraction component."""

    def __init__(self, provider, rows=0, columns=0):
        """Initialize a new instance of LcdComponent.

        :param raspy.lcd.lcd_transfer_provider.LcdTransferProvider provider: The
        LCD transfer provider.
        :param int rows: The number of rows in the display.
        :param int columns: The number of columns in the display.
        :raises: raspy.argument_null_exception.ArgumentNullException if the
        provider is None.
        :raises: raspy.illegal_argument_exception.IllegalArgumentException if
        the specified provider is not of LcdTransferProvider type.
        """
        Lcd.__init__(self)
        if provider is None:
            raise ArgumentNullException("'provider' cannot be None.")

        if not isinstance(provider, LcdTransferProvider):
            msg = "'provider' must be of type LcdTransferProvider "
            msg += "or derivative."
            raise IllegalArgumentException(msg)

        self.__module = LcdModule(provider)
        self.__module.begin(columns, rows)

    def dispose(self):
        """Dispose managed resources."""
        if self.is_disposed:
            return

        if self.__module is not None:
            self.__module.dispose()
            self.__module = None

        Lcd.dispose(self)

    @property
    def row_count(self):
        """Get the number of rows supported by the display.

        :returns: The number of supported rows.
        :rtype: int
        """
        return self.__module.rows

    @property
    def column_count(self):
        """Get the number of columns supported by the display.

        :returns: The number of supported columns.
        :rtype: int
        """
        return self.__module.columns

    def set_cursor_position(self, row=0, column=0):
        """Position the cursor at the specified column and row.

        If only the row is given, then the cursor is placed at the beginning
        of the specified row.

        :param int row: The number of the row to position the cursor in.
        :param int column: The number of the column in the specified row to
        position the cursor.
        """
        Lcd._validate_coordinates(self, row, column)
        self.__module.set_cursor_position(column, row)

    def write_single_byte(self, data):
        """Write a single byte of data to the display.

        :param int data: The byte to send.
        """
        self.__module.write_byte(data)

    def clear_display(self):
        """Clear the display."""
        self.__module.return_home()

    def set_cursor_home(self):
        """Set the cursor in the home position."""
        self.__module.return_home()
