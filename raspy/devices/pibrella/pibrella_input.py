"""PiBrella inputs."""


from raspy.io import gpio_pins
from raspy.io import pin_mode
from raspy.io import pin_state
from raspy.io.gpio_standard import GpioStandard


A = GpioStandard(gpio_pins.Pin13(), pin_mode.IN, pin_state.LOW)
"""PiBrella input A."""

B = GpioStandard(gpio_pins.Gpio11(), pin_mode.IN, pin_state.LOW)
"""PiBrella input B."""

C = GpioStandard(gpio_pins.Gpio10(), pin_mode.IN, pin_state.LOW)
"""PiBrella input C."""

D = GpioStandard(gpio_pins.Pin12(), pin_mode.IN, pin_state.LOW)
"""PiBrella input D."""

BUTTON = GpioStandard(gpio_pins.Gpio14(), pin_mode.IN, pin_state.LOW)
"""PiBrella button input."""
