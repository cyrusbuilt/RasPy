"""PiBrella outputs."""


from raspy.io import gpio_pins
from raspy.io import pin_mode
from raspy.io import pin_state
from raspy.io.gpio_standard import GpioStandard


E = GpioStandard(gpio_pins.V2Gpio03(), pin_mode.OUT, pin_state.LOW)
"""PiBrella output E."""

F = GpioStandard(gpio_pins.Gpio04(), pin_mode.OUT, pin_state.LOW)
"""PiBrella output F."""

G = GpioStandard(gpio_pins.Pin05(), pin_mode.OUT, pin_state.LOW)
"""PiBrella output G."""

H = GpioStandard(gpio_pins.V2P5Pin06(), pin_mode.OUT, pin_state.LOW)
"""PiBrella output H."""

LED_RED = GpioStandard(gpio_pins.V2Gpio02(), pin_mode.OUT, pin_state.LOW)
"""PiBrella red LED."""

LED_YELLOW = GpioStandard(gpio_pins.Gpio00(), pin_mode.OUT, pin_state.LOW)
"""PiBrella yellow LED."""

LED_GREEN = GpioStandard(gpio_pins.Gpio07(), pin_mode.OUT, pin_state.LOW)
"""PiBrella green LED."""

BUZZER = GpioStandard(gpio_pins.Gpio01(), pin_mode.PWM, pin_state.LOW)
"""PiBrella buzzer."""
