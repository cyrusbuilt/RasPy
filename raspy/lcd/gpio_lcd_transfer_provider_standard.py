"""This module provides the GpioLcdTransferProviderStandard class."""


from raspy.illegal_argument_exception import IllegalArgumentException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.io import gpio_pins
from raspy.io import pin_mode
from raspy.io import pin_state
from raspy.io.gpio_standard import GpioStandard
from raspy.lcd.lcd_transfer_provider import LcdTransferProvider


class GpioLcdTransferProviderStandard(LcdTransferProvider):
    """Raspberry Pi GPIO (via filesystem) provider.

    This is for the Micro Liquid Crystal Display.
    """

    __fourBitMode = False
    __registerSelectPort = None
    __readWritePort = None
    __enablePort = None
    __dataPorts = None

    def __init__(self, d0, d1, d2, d3, d4, d5, d6, d7, four_bit_mode, rs, rw, enable):
        """Initialize a new instance of the GpioLcdTransferProviderStandard.

        Initializes with all the necessary pins and whether or not to use
        4-bit mode.

        :param raspy.io.gpio_pins.GpioPin d0:
        :param raspy.io.gpio_pins.GpioPin d1:
        :param raspy.io.gpio_pins.GpioPin d2:
        :param raspy.io.gpio_pins.GpioPin d3:
        :param raspy.io.gpio_pins.GpioPin d4:
        :param raspy.io.gpio_pins.GpioPin d5:
        :param raspy.io.gpio_pins.GpioPin d6:
        :param raspy.io.gpio_pins.GpioPin d7:
        :param bool four_bit_mode:
        :param raspy.io.gpio_pins.GpioPin rs:
        :param raspy.io.gpio_pins.GpioPin rw:
        :param raspy.io.gpio_pins.GpioPin enable:
        :raises:raspy.illegal_argument_exception.IllegalArgumentException if
        'rs' or 'enable' params are None, not a GpioPin type, or is
        raspy.io.gpio_pins.GpioNone.
        """
        super(LcdTransferProvider, self).__init__()
        self.__fourBitMode = four_bit_mode
        if self.__fourBitMode is None:
            self.__fourBitMode = True

        if rs == gpio_pins.GpioNone() or rs is None:
            msg = "'rs' param must be a GpioPin other than GpioNone."
            raise IllegalArgumentException(msg)

        self.__registerSelectPort = GpioStandard(rs, pin_mode.OUT, pin_state.LOW)
        self.__registerSelectPort.provision()

        # We can save 1 pin by not using RW. Indicate this by passing
        # gpio_pins.GpioNone() instead of pin num.
        self.__readWritePort = gpio_pins.GpioNone()
        if rw != gpio_pins.GpioNone():
            self.__readWritePort = GpioStandard(rw, pin_mode.OUT, pin_state.LOW)
            self.__readWritePort.provision()

        if enable is None or enable == gpio_pins.GpioNone():
            msg = "'enable' param must be a GpioPin other than GpioNone"
            raise IllegalArgumentException(msg)

        self.__enablePort = GpioStandard(enable, pin_mode.OUT, pin_state.LOW)
        self.__enablePort.provision()

        data_pins = [
            d0,
            d1,
            d2,
            d3,
            d4,
            d5,
            d6,
            d7
        ]

        self.__dataPorts = list()
        for i in range(0, len(data_pins) - 1):
            if (data_pins[i] is None or
                    not isinstance(data_pins[i], gpio_pins.GpioPin)):
                data_pins[i] = gpio_pins.GpioNone()

            if data_pins[i] != gpio_pins.GpioNone():
                pin = GpioStandard(data_pins[i], pin_mode.OUT, pin_state.LOW)
                pin.provision()
                self.__dataPorts.append(pin)

    @property
    def is_four_bit_mode(self):
        """Get a value indicating whether this instance is in 4-bit mode.

        :returns: True if 4-bit mode; Otherwise, false.
        :rtype: bool
        """
        return self.__fourBitMode

    def _pulse_enable(self):
        """Pulse the enable pin."""
        self.__enablePort.write(pin_state.LOW)
        self.__enablePort.write(pin_state.HIGH)  # enable pulse must be > 450 ns.
        self.__enablePort.write(pin_state.LOW)   # Command needs 37 us to settle.

    def write_4_bits(self, value):
        """
        Write the command or data in 4-bit mode (the last 4 data lines).

        :param byte, int value: The command or data to write.
        """
        for i in range(0, 3):
            val = pin_state.LOW
            if ((value >> i) & 0x01) == 0x01:
                val = pin_state.HIGH
            self.__dataPorts[i + 4].write(val)
        self._pulse_enable()

    def write_8_bits(self, value):
        """Write the command or data in 8-bit mode (all 8 data lines).

        :param byte, int value: The command or data to write.
        """
        for i in range(0, 7):
            val = pin_state.LOW
            if ((value >> i) & 0x01) == 0x01:
                val = pin_state.HIGH
            self.__dataPorts[i].write(val)
        self._pulse_enable()

    def send(self, data, mode, back_light):
        """Send the specified data, mode, and backlight.

        :param byte, int data: The data to send.
        :param int mode: Mode for register-select pin (pin_state.HIGH = on,
        pin_state.LOW = off).
        :param bool back_light: Set True to turn on the backlight.
        """
        if LcdTransferProvider.is_disposed.fget():
            raise ObjectDisposedException("GpioLcdTransferProviderStandard")

        # TODO set backlight.

        self.__registerSelectPort.write(mode)

        # If there is a RW pin indicated, set it low to write.
        if self.__readWritePort is not None:
            self.__readWritePort.write(pin_state.LOW)

        if self.__fourBitMode:
            self.write_4_bits(data >> 4)
            self.write_4_bits(data)
        else:
            self.write_8_bits(data)

    def dispose(self):
        """Dispose this instance."""
        if LcdTransferProvider.is_disposed.fget():
            return

        if self.__registerSelectPort is not None:
            self.__registerSelectPort.dispose()
            self.__registerSelectPort = None

        if self.__readWritePort is not None:
            self.__readWritePort.dispose()
            self.__readWritePort = None

        if self.__enablePort is not None:
            self.__enablePort.dispose()
            self.__enablePort = None

        if self.__dataPorts is not None and len(self.__dataPorts) > 0:
            for i, port in enumerate(self.__dataPorts):
                if port is not None:
                    port.dispose()

        self.__dataPorts = None
        LcdTransferProvider.dispose(self)
