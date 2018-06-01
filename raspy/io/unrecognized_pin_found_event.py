"""Unrecognized pin found event."""


class UnrecognizedPinFoundEvent(object):
    """Unrecognized pin found event."""

    def __init__(self, message):
        """Initialize a new instance of the UnrecognizedPinFoundEvent class.

        Initializes a new instance of the raspy.io.UnrecognizedPinFoundEvent
        class with a message describing the event.

        :param string message: A message describing the event.
        """
        self.__message = message

    @property
    def event_message(self):
        """Get the message describing the event.

        :returns: The event message.
        :rtype: string
        """
        return self.__message
