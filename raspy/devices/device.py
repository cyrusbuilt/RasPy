"""This module contains the Device base type."""


from raspy.disposable import Disposable


class Device(Disposable):
    """A hardware abstraction device interface."""

    def __init__(self, props=None):
        """Initialize a new instance of Device.

        :param dict props: A list of component properties (optional).
        """
        Disposable.__init__(self)
        self.__name = ""
        self.__tag = None
        self.__props = props
        if self.__props is None:
            self.__props = dict()

    @property
    def device_name(self):
        """Get the device name.

        :returns: The device name.
        :rtype: str
        """
        return self.__name

    @device_name.setter
    def device_name(self, name):
        """Set the device name.

        :param str name: The device name.
        """
        self.__name = name

    @property
    def tag(self):
        """Get the object this device is tagged with.

        :returns: The tag.
        :rtype: object
        """
        return self.__tag

    @tag.setter
    def tag(self, the_tag):
        """Set the object this device should be tagged with.

        :param object the_tag: The object to tag this device with.
        """
        self.__tag = the_tag

    @property
    def property_collection(self):
        """Get the custom property collection.

        :returns: The custom property collection
        :rtype: dict
        """
        return self.__props

    def has_property(self, key):
        """Check to see if the property collection contains the specified key.

        :param str key: The key name of the property to check for.
        :returns: True if the property collection contains the key.
        :rtype: bool
        """
        return key in self.__props

    def set_property(self, key, value):
        """
        Set the value of the specified property.

        If the property does not already exist in the collection, it will be
        added.

        :param str key: The property name (key).
        :param str value: The property value.
        """
        self.__props[key] = value

    def __str__(self):
        """Get a string representation of this device.

        :returns: A string representation of the device.
        :rtype: str
        """
        return self.__name

    def dispose(self):
        """Dispose managed resources."""
        if Disposable.is_disposed.fget():
            return

        self.__props = None
        self.__tag = None
        self.__name = None
        Disposable.dispose(self)
