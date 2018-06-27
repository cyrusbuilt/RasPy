"""This module contains the MotionDetectedEvent type."""


from datetime import datetime


class MotionDetectedEvent(object):
    """The event that fires when motion is detected."""

    def __init__(self, motion=False, timestamp=None):
        """Initialize a new instance of MotionDetectedEvent.

        :param bool motion: Set True if motion detected.
        :param datetime timestamp: The timestamp of when state changed.
        """
        self.__motionDetected = motion
        if self.__motionDetected is None:
            self.__motionDetected = False

        self.__timestamp = timestamp
        if self.__timestamp is None:
            self.__timestamp = datetime.now()

    @property
    def is_motion_detected(self):
        """Get whether or not motion was detected.

        :returns: True if motion detected.
        :rtype: bool
        """
        return self.__motionDetected

    @property
    def timestamp(self):
        """Get the timestamp of when motion was detected.

        :returns: The timestamp of when the event occurred.
        :rtype: datetime
        """
        return self.__timestamp
