"""Tests PiFacePinFactory methods."""


import platform
from raspy.io import pi_face_pins
from raspy.io import pin_mode
# if platform.system() != "Linux":
#     print("WARNING: PiFaceGpioDigital requires Linux. Skipping tests...")
# else:
from raspy.io import pi_face_pin_factory
from raspy.io.pi_face_gpio_digital import PiFaceGpioDigital


def test_create_output_pin():
    """Test create_output_pin method."""
    if platform.system() != "Linux":
        assert True
        return

    # noinspection PyTypeChecker
    output = pi_face_pin_factory.create_output_pin(pi_face_pins.Output00(), "test1")
    assert isinstance(output, PiFaceGpioDigital)
    assert output.address == pi_face_pins.Output00().value
    assert output.mode == pin_mode.OUT


def test_create_input_pin():
    """Test create_input_pin method."""
    if platform.system() != "Linux":
        assert True
        return

    # noinspection PyTypeChecker
    inp = pi_face_pin_factory.create_input_pin(pi_face_pins.Input00(), "test2")
    assert isinstance(inp, PiFaceGpioDigital)
    assert inp.address == pi_face_pins.Input00().value
    assert inp.mode == pin_mode.IN
