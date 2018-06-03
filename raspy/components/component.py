"""This module contains the base type for components."""


from raspy.disposable import Disposable


class Component(Disposable):
    """A hardware abstraction component base class."""

    __componentName = ""
    __tag = None
    __props = None

    def __init__(self, props):
        """Initialize a new instance of the Component class.

        :param dict props: A list of properties.
        """
        super(Disposable, self).__init__()
        self.__props = props
        if self.__props is None:
            self.__props = dict()

    @property
    def component_name(self):
        """Get the component name.

        :returns: The component name.
        :rtype: str
        """
        return self.__componentName

    @component_name.setter
    def component_name(self, name):
        """Set the component name.

        :param str name: The component name.
        """
        self.__componentName = name

    @property
    def tag(self):
        """Get the object this component is tagged with.

        :returns: The object this component is tagged with.
        :rtype: object
        """
        return self.__tag

    @tag.setter
    def tag(self, obj):
        """Set the object to tag this component with.

        :param object tag: The object to tag this component with.
        """
        self.__tag = obj

    @property
    def property_collection(self):
        """Get the property collection.

        :returns: The property collection. An empty list if no properties.
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
        """Get a string representation of this component.

        :returns: A string representation of the component.
        :rtype: str
        """
        return self.__componentName

    def dispose(self):
        """Dispose managed resources."""
        if Disposable.is_disposed.fget():
            return

        self.__props = None
        self.__tag = None
        self.__componentName = None
        Disposable.dispose(self)
