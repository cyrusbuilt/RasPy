"""This module contains the PiBrellaInterface type."""


from raspy.devices.device import Device
from raspy.devices.pibrella import pibrella_input
from raspy.devices.pibrella import pibrella_output
from raspy.components.buttons.button_component import ButtonComponent
from raspy.components.buzzers.buzzer_component import BuzzerComponent
from raspy.components.lights.led_component import LedComponent
from raspy.io import pin_state


class PiBrellaInterface(Device):
    """PiBrella device abstraction interface/base type."""

    def __init__(self):
        """Initialize a new instance of PiBrellaInterface."""
        Device.__init__(self)
        self.__inputs = [
            pibrella_input.A,
            pibrella_input.B,
            pibrella_input.C,
            pibrella_input.D,
            pibrella_input.BUTTON
        ]
        self.__inputs[0].pin_name = "INPUT A"
        self.__inputs[1].pin_name = "INPUT B"
        self.__inputs[2].pin_name = "INPUT C"
        self.__inputs[3].pin_name = "INPUT D"
        self.__inputs[4].pin_name = "BUTTON"
        for inp in self.__inputs:
            inp.provision()

        self.__outputs = [
            pibrella_output.E,
            pibrella_output.F,
            pibrella_output.G,
            pibrella_output.H,
            pibrella_output.LED_RED,
            pibrella_output.LED_YELLOW,
            pibrella_output.LED_GREEN
        ]
        self.__outputs[0].pin_name = "OUTPUT E"
        self.__outputs[1].pin_name = "OUTPUT F"
        self.__outputs[2].pin_name = "OUTPUT G"
        self.__outputs[3].pin_name = "OUTPUT H"
        self.__outputs[4].pin_name = "RED LED"
        self.__outputs[5].pin_name = "YELLOW LED"
        self.__outputs[6].pin_name = "GREEN LED"
        for out in self.__outputs:
            out.provision()

        self.__leds = [
            LedComponent(self.__outputs[4]),
            LedComponent(self.__outputs[5]),
            LedComponent(self.__outputs[6])
        ]

        self.__button = ButtonComponent(self.__inputs[4])
        self.__buzzer = BuzzerComponent(pibrella_output.BUZZER)
        self.__buzzer.component_name = "PIBRELLA BUZZER"
        self.__buzzer.stop()

    def dispose(self):
        """Release managed resources used by this component."""
        if self.is_disposed:
            return

        for out in self.__outputs:
            out.write(pin_state.LOW)

        self.__inputs = None
        self.__outputs = None
        self.__leds = None
        self.__button = None
        self.__buzzer = None
        Device.dispose(self)

    @property
    def red_led(self):
        """Get the red LED.

        :returns: The red LED.
        :rtype: raspy.io.gpio_standard.GpioStandard
        """
        return self.__leds[0]

    @property
    def yellow_led(self):
        """Get the yellow LED.

        :returns: The yellow LED.
        :rtype: raspy.io.gpio_standard.GpioStandard
        """
        return self.__leds[1]

    @property
    def green_led(self):
        """Get the green LED.

        :returns: The green LED.
        :rtype: raspy.io.gpio_standard.GpioStandard
        """
        return self.__leds[2]

    @property
    def leds(self):
        """Get the LEDs (list of GpioStandard output objects).

        :returns: A list of GpioStandard objects representing the LEDs.
        :rtype: list
        """
        return self.__leds

    @property
    def button(self):
        """Get the PiBrella button input.

        :returns: The button input.
        :rtype: raspy.io.gpio_standard.GpioStandard
        """
        return self.__button

    @property
    def buzzer(self):
        """Get the buzzer output.

        :returns: The buzzer output.
        :rtype: raspy.io.gpio_standard.GpioStandard
        """
        return self.__buzzer

    @property
    def input_a(self):
        """Get PiBrella input A.

        :returns: Input A.
        :rtype: raspy.io.gpio_standard.GpioStandard
        """
        return self.__inputs[0]

    @property
    def input_b(self):
        """Get PiBrella input B.

        :returns: Input B.
        :rtype: raspy.io.gpio_standard.GpioStandard
        """
        return self.__inputs[1]

    @property
    def input_c(self):
        """Get PiBrella input C.

        :returns: Input C.
        :rtype: raspy.io.gpio_standard.GpioStandard
        """
        return self.__inputs[2]

    @property
    def input_d(self):
        """Get PiBrella input D.

        :returns: Input D.
        :rtype: raspy.io.gpio_standard.GpioStandard
        """
        return self.__inputs[3]

    @property
    def inputs(self):
        """Get all the PiBrella inputs.

        This is a list of GpioStandard input objects.

        :returns: A list of all of the inputs.
        :rtype: list
        """
        return self.__inputs

    @property
    def output_e(self):
        """Get PiBrella output E.

        :returns: Output E.
        :rtype: raspy.io.gpio_standard.GpioStandard
        """
        return self.__outputs[0]

    @property
    def output_f(self):
        """Get PiBrella output F.

        :returns: Output F.
        :rtype: raspy.io.gpio_standard.GpioStandard
        """
        return self.__outputs[1]

    @property
    def output_g(self):
        """Get PiBrella output G.

        :returns: Output G.
        :rtype: raspy.io.gpio_standard.GpioStandard
        """
        return self.__outputs[2]

    @property
    def output_h(self):
        """Get PiBrella output H.

        :returns: Output H.
        :rtype: raspy.io.gpio_standard.GpioStandard
        """
        return self.__outputs[3]

    @property
    def outputs(self):
        """Get all the PiBrella outputs.

        This is a list of GpioStandard output objects.

        :returns: A list of all the outputs.
        :rtype: list
        """
        return self.__outputs
