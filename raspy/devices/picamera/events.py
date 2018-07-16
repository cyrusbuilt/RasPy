"""This module contains capture events."""


class CaptureDoneEvent(object):
    """The event that fires when an image capture finishes."""

    def __init__(self, exit_code=0):
        """Intialize a new instance of CaptureDoneEvent.

        :param int exit_code: The exit code of the capture process.
        """
        self.__exitCode = exit_code

    @property
    def exit_code(self):
        """Get the exit code of the capture process.

        :returns: The exit code of the image capture process.
        :rtype: int
        """
        return self.__exitCode


class CaptureOutputEvent(object):
    """The event that fires when output is received from the capture process."""

    def __init__(self, output=""):
        """Initialize a new instance of CaptureOutputEvent.

        :param str output: The process output.
        """
        self.__output = output

    @property
    def output(self):
        """Get the process output.

        :returns: The output from the image capture process.
        :rtype: str
        """
        return self.__output


class CaptureStartEvent(object):
    """The event that fires when an image capture starts."""

    def __init__(self, pid=-1):
        """Initialize a new instance of CaptureStartEvent.

        :param int pid: The process ID of the image capture process.
        """
        self.__pid = pid

    @property
    def pid(self):
        """Get the process ID of the image capture process.

        :returns: The process ID of the image capture process or -1 if the
        process failed to start.
        :rtype: int
        """
        return self.__pid
