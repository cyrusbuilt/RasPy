"""This module contains the Gate type."""


from raspy.devices.access.opener import Opener


class Gate(Opener):
    """Garage door opener abstraction interface/base type."""

    def __init__(self):
        """Initialize a new instance of Gate."""
        Opener.__init__(self)

    @property
    def is_locked(self):
        """Get a flag indicating whether this gate is locked.

        :returns: True if locked; Otherwise, False.
        :rtype: bool
        """
        return False

    def open(self):
        """Instruct the device to open.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        raise NotImplementedError("Method 'open()' not implemented.")

    def close(self):
        """Instruct the device to close.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        raise NotImplementedError("Method 'close()' not implemented.")
