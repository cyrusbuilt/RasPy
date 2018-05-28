"""Tests PiFacePinFactory methods."""


import platform
from RasPy.IO import PiFacePins
from RasPy.IO import PinMode
if platform.system() != "Linux":
    print("WARNING: PiFaceGpioDigital requires Linux. Skipping tests...")
else:
    from RasPy.IO import PiFacePinFactory
    from RasPy.IO.PiFaceGpioDigital import PiFaceGpioDigital


def test_create_output_pin():
    """Test create_output_pin method."""
    if platform.system() != "Linux":
        assert True
        return

    output = PiFacePinFactory.create_output_pin(PiFacePins.OUTPUT00, "test1")
    assert isinstance(output, PiFaceGpioDigital)
    assert output.pin_address == PiFacePins.OUTPUT00.value
    assert output.mode == PinMode.OUT


def test_create_input_pin():
    """Test create_input_pin method."""
    if platform.system() != "Linux":
        assert True
        return

    inp = PiFacePinFactory.create_input_pin(PiFacePins.INPUT00, "test2")
    assert isinstance(inp, PiFaceGpioDigital)
    assert inp.pin_address == PiFacePins.INPUT00.value
    assert inp.mode == PinMode.INPUT
