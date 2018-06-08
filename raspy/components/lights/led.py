"""This module contains the LED type."""


from raspy.components.lights.light import Light


class Led(Light):
    """A base class for LED abstraction components."""

    def __init__(self):
        """Initialize a new Led instance."""
        Light.__init__(self)

    def toggle(self):
        """Toggle the state of the LED."""
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()

    def blink(self, delay=0.0, duration=0.0):
        """Blink the LED.

        :param int delay: The delay between state change.
        :param int duration: The amount of time to blink the LED (in millis).
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        msg = "Method blink(delay, duration) not implemented."
        raise NotImplementedError(msg)

    def pulse(self, duration):
        """Pulse the state of the LED.

        :param int duration: The amount of time to pulse the LED (in millis).
        """
        raise NotImplementedError("Method pulse(duration) not implemented.")
