"""This module contains the MotorRotateEvent type."""


class MotorRotateEvent(object):
    """The event that gets fired when a motor rotation occurs."""

    def __init__(self, steps=0):
        """Initialize  a new instance of MotorRotateEvent.

        :param int steps: The steps being taken. 0 steps = stopped. Greater
        than 0 = the number of steps forward. Less than 0 = the number of
        steps moving backward.
        """
        self.__steps = steps

    @property
    def steps(self):
        """Get the number of steps.

        :returns: The number of steps rotated.
        :rtype: int
        """
        return self.__steps
