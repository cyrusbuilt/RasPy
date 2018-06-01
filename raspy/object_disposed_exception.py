"""This module contains the ObjectDisposedException exception class."""


class ObjectDisposedException(Exception):
    """Object disposed exception.

    The exception that is thrown when an object is referenced that has been
    disposed.
    """

    def __init__(self, obj_name):
        """Initialize a new instance of raspy.object_disposed_exception.ObjectDisposedException.

        Initializes with the object that has been disposed.

        :param str obj_name: The name of the object that has been disposed.
        """
        msg = obj_name + " has been disposed and can no longer be referenced."
        Exception.__init__(self, msg)
