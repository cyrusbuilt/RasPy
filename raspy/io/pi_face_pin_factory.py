"""This module contains factory methods for creating PiFace digital I/O's."""

from raspy import string_utils
from raspy.io import pin_mode
from raspy.io import pin_state
from raspy.io import pin_pull_resistance
from raspy.io.pi_face_gpio_digital import PiFaceGpioDigital


def create_output_pin(pin, name):
    """Factory method for creating a PiFace digital output pin.

    :param raspy.io.pi_face_pins.PiFacePin pin: The pin to create an output
    for.
    :param str name: The name of the pin. If not specified, the default
    hardware name of the pin will be used instead.
    :returns: A PiFace digital output.
    :rtype: raspy.io.pi_face_gpio_digital.PiFaceGpioDigital
    :raises: raspy.io.io_exception.IOException if unable to communicate with
    the SPI bus.
    """
    if string_utils.is_null_or_empty(name):
        name = pin.name

    val = pin.value
    speed = PiFaceGpioDigital.BUS_SPEED
    pfgd = PiFaceGpioDigital(pin, pin_state.LOW, val, speed)
    pfgd.pin_name = name
    pfgd.mode = pin_mode.OUT
    pfgd.pull_resistance = pin_pull_resistance.Off
    return pfgd


def create_input_pin(pin, name):
    """Factory method for creating a PiFace digital input pin.

    Creates an input pin with the internal pull-up resistor enabled.

    :param raspy.io.pi_face_pins.PiFacePin pin: The pin to create an output
    for.
    :param str name: The name of the pin. If not specified, the default
    hardware name of the pin will be used instead.
    :returns: A PiFace digital input.
    :rtype: raspy.io.pi_face_gpio_digital.PiFaceGpioDigital
    :raises: raspy.io.io_exception.IOException if unable to communicate with
    the SPI bus.
    """
    if string_utils.is_null_or_empty(name):
        name = pin.name

    val = pin.value
    speed = PiFaceGpioDigital.BUS_SPEED
    pfgd = PiFaceGpioDigital(pin, pin_state.LOW, val, speed)
    pfgd.pin_name = name
    pfgd.mode = pin_mode.IN
    pfgd.pull_resistance = pin_pull_resistance.PullUp
    return pfgd
