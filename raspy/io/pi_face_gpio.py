"""This module provides the PiFaceGPIO type."""

from raspy import string_utils
from raspy.argument_null_exception import ArgumentNullException
from raspy.illegal_argument_exception import IllegalArgumentException
from raspy.io import gpio
from raspy.io import pi_face_pins
from raspy.io import pin_mode


class PiFaceGPIO(gpio.Gpio):
    """Implemented by classes that represent GPIO pins on the PiFace.

    The PiFace is an expansion board for the Raspberry Pi.
    """

    EVENT_STATE_CHANGED = "piFaceGpioStateChanged"
    """The name of the state changed event."""

    OUTPUTS = [
        pi_face_pins.Output00(),
        pi_face_pins.Output01(),
        pi_face_pins.Output02(),
        pi_face_pins.Output03(),
        pi_face_pins.Output04(),
        pi_face_pins.Output05(),
        pi_face_pins.Output06(),
        pi_face_pins.Output07()
    ]
    """An array of all the PiFace outputs."""

    INPUTS = [
        pi_face_pins.Input00(),
        pi_face_pins.Input01(),
        pi_face_pins.Input02(),
        pi_face_pins.Input03(),
        pi_face_pins.Input04(),
        pi_face_pins.Input05(),
        pi_face_pins.Input06(),
        pi_face_pins.Input07()
    ]
    """An array of all PiFace inputs."""

    def __init__(self, pn, initial_val, name):
        """Initialize a new instance of the raspy.io.PiFaceGPIO class.

        :param raspy.io.pi_face_pin.PiFacePin pn: The underlying PiFace pin.
        :param int initial_val: The initial pin value (state).
        :param string name: The pin name.
        :raises: raspy.argument_null_exception.ArgumentNullException if the
        specified pin is NonePin.
        :raises: raspy.illegal_argument_exception.IllegalArgumentException if
        the specified pin is not of type raspy.io.pi_face_pins.PiFacePin.
        """
        gpio.Gpio.__init__(self, pn, pin_mode.IN, initial_val)
        self.__pwm = 0
        self.__pwmRange = 0

        if pn is None:
            raise ArgumentNullException("pn param cannot be NonePin.")

        if not isinstance(pn, pi_face_pins.PiFacePin):
            err_msg = "pn param must be a PiFacePins member."
            raise IllegalArgumentException(err_msg)

        self.pin_name = name
        if string_utils.is_null_or_empty(self.pin_name):
            self.pin_name = pn.name

        if (pn == pi_face_pins.Input00 or pn == pi_face_pins.Input01 or
                pn == pi_face_pins.Input02 or pn == pi_face_pins.Input03 or
                pn == pi_face_pins.Input04 or pn == pi_face_pins.Input05 or
                pn == pi_face_pins.Input06 or pn == pi_face_pins.Input07):
            self.mode = pin_mode.IN
        elif (pn == pi_face_pins.Output00 or pn == pi_face_pins.Output01 or
              pn == pi_face_pins.Output02 or pn == pi_face_pins.Output03 or
              pn == pi_face_pins.Output04 or pn == pi_face_pins.Output05 or
              pn == pi_face_pins.Output06 or pn == pi_face_pins.Output07):
            self.mode = pin_mode.OUT

    @property
    def inner_pin(self):
        """Get the inner pin."""
        return pi_face_pins.NonePin

    def dispose(self):
        """Dispose managed resources.

        Performs application-defined tasks associated with freeing, releasing,
        or resetting resources.
        """
        if self.is_disposed:
            return

        self.__pwm = 0
        self.__pwmRange = 0
        gpio.Gpio.dispose(self)

    @property
    def pwm(self):
        """Get the PWM (pulse-width modulation) value.

        :returns: The PWM value.
        :rtype: int
        """
        return self.__pwm

    @pwm.setter
    def pwm(self, val):
        """Set the PWM (pulse-width modulation) value.

        :param int val: The PWM value.
        """
        self.__pwm = val

    @property
    def pwm_range(self):
        """Get the PWM (pulse-width modulation) range.

        :returns: The PWM range.
        :rtype: int
        """
        return self.__pwmRange

    @pwm_range.setter
    def pwm_range(self, rng):
        """Set the PWM (pulse-width modulation) range.

        :param int rng: The PWM range.
        """
        self.__pwmRange = rng
