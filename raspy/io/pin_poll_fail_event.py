"""This module contains the PinPollFailEvent type."""


class PinPollFailEvent(object):
    """Pin poll failure event."""

    def __init__(self, cause):
        """Initialize a new instance of PinPollFailEvent.

        Initializes a new instance of the raspy.io.PinPollFailEvent class
        with the exception that is the cause of the event.

        :param Exception cause: The Error (exception) that is the cause of the event.
        """
        self.__cause = cause

    @property
    def failure_cause(self):
        """Get the exception that caused the event.

        :returns: The Error or Exception that caused the event.
        :rtype: Exception
        """
        return self.__cause
