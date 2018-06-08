"""This module contains the DimmableLightComponent type."""


from raspy.argument_null_exception import ArgumentNullException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.lights.light_level_change_event import LightLevelChangeEvent
from raspy.components.lights.light_state_change_event import LightStateChangeEvent
from raspy.components.lights.dimmable_light import DimmableLight


class DimmableLightComponent(DimmableLight):
    """A component that is an abstraction of a dimmable light."""

    def __init__(self, pin, minimum=0, maximum=0):
        """Initialize a new instance of DimmableLightComponent.

        :param raspy.io.gpio.Gpio pin: The pin used to control the dimmable
        light.
        :param int minimum: The minimum brightness level.
        :param int maximum: The maximum brightness level.
        :raises: raspy.argument_null_exception.ArgumentNullException if the
        pin param is None.
        """
        DimmableLight.__init__(self)
        if pin is None:
            raise ArgumentNullException("'pin' param cannot be None.")

        self.__min = minimum
        self.__max = maximum
        self.__pin = pin
        self.__pin.provision()

    def dispose(self):
        """Release all resources used by this instance."""
        if self.is_disposed:
            return

        if self.__pin is not None:
            self.__pin.dispose()
            self.__pin = None

        self.remove_all_listeners()
        DimmableLight.dispose(self)

    @property
    def min_level(self):
        """Get the minimum brightness level.

        :returns: The minimum brightness level.
        :rtype: int
        """
        return self.__min

    @property
    def max_level(self):
        """Get the maximum brightness level.

        :returns: The maximum brightness level.
        :rtype: int
        """
        return self.__max

    @property
    def level(self):
        """Get the brightness level.

        :returns: The brightness level.
        :rtype: int
        """
        return self.__pin.pwm

    @level.setter
    def level(self, lev):
        """Set the brightness level.

        :param int lev: The brightness level.
        :raises: IndexError if the specified level is less than min_level or
        greater than max_level.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("DimmableLightComponent")

        if lev < self.__min:
            raise IndexError("Level cannot be less than min_level.")

        if lev > self.__max:
            raise IndexError("Level cannot be greater than max_level.")

        on_before_change = self.is_on
        self.__pin.pwm = lev
        on_after_change = self.is_on
        evt = LightLevelChangeEvent(lev)
        self.on_light_level_changed(evt)
        if on_before_change != on_after_change:
            evt2 = LightStateChangeEvent(on_after_change)
            self.on_light_state_changed(evt2)
