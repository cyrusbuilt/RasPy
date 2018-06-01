"""This module provides the base class for defining a disposable type."""


class Disposable(object):
    """Base class for a disposable type.

    Defines a type which provides a mechanism for releasing unmanaged
    resources.
    """

    __is_disposed = False

    def __init__(self):
        """Constructor."""
        pass

    def dispose(self):
        """Dispose managed resources.

        In a subclass, performs application-defined tasks associated with
        freeing, releasing, or resetting resources.
        """
        self.__is_disposed = True

    @property
    def is_disposed(self):
        """Determine if instance has been disposed.

        In a subclass, determines whether or not the current instance has been
        disposed.

        :returns: True if disposed; Otherwise, False.
        :rtype: bool
        """
        return self.__is_disposed
