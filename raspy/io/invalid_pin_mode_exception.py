"""This module provides the InvalidPinModeException exception class."""


class InvalidPinModeException(Exception):
    """Invalid pin mode exception.

    The exception that is thrown when an invalid pin mode is used.
    """

    def __init__(self, message, pn):
        """Initialize new instance of raspy.io.invalid_pin_mode_exception.InvalidPinModeException.

        Initializes a new instance of the InvalidPinModeException class with
        the pin that has the incorrect mode and a message describing the
        exception.

        :param string message: The message describing the exception.
        :param raspy.io.pin.Pin pn: The pin that is the cause of the
        exception.
        """
        super(InvalidPinModeException, self).__init__(message)
        self.__pin = pn

    @property
    def pin(self):
        """Get the pin that is the cause of the exception.

        :returns: The pin that is configured with the incorrect mode.
        :rtype: raspy.io.pin.Pin
        """
        return self.__pin
