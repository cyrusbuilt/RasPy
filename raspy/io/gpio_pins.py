"""
Possible GPIO pins.

The various GPIO pins on the Raspberry Pi Revision 1.0 and 2.0 boards.
Refer to http://elinux.org/Rpi_Low-level_peripherals for diagram.
P1-01 = bottom left, P1-02 = top left
pi connector P1 pin    = GPIOnum
                P1-03 = GPIO0
                P1-05 = GPIO1
                P1-07 = GPIO4
                P1-08 = Gpio14 - alt function (UART0_TXD) on boot-up
                P1-10 = Gpio15 - alt function (UART0_TXD) on boot-up
                P1-11 = Gpio17
                P1-12 = Gpio18
                P1-13 = Gpio21
                P1-15 = Gpio22
                P1-16 = Gpio23
                P1-18 = Gpio24
                P1-19 = Gpio10
                P1-21 = GPIO9
                P1-22 = Gpio25
                P1-23 = Gpio11
                P1-24 = GPIO8
                P1-26 = GPIO7
So to turn on Pin7 on the GPIO connector, pass in GpioPins.Gpio04 as
the pin parameter.
"""


class GpioPin:
    """Base type for GPIO pins."""

    def __init__(self):
        """ctor."""
        pass

    value = -1
    name = ""


class GpioNone(GpioPin):
    """No pin (null)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = -1
    name = "GpioNone"


class Gpio00(GpioPin):
    """GPIO 00 (pin P1-03)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 0
    name = "Gpio00"


class Gpio01(GpioPin):
    """GPIO 01 (pin P1-05)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 1
    name = "Gpio01"


class Gpio04(GpioPin):
    """GPIO 04 (pin P1-07)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 4
    name = "Gpio04"


class Gpio07(GpioPin):
    """GPIO 07 (pin P1-26)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 7
    name = "Gpio07"


class Gpio08(GpioPin):
    """GPIO 08 (pin P1-24)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 8
    name = "Gpio08"


class Gpio09(GpioPin):
    """GPIO 09 (pin P1-21)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 9
    name = "Gpio09"


class Gpio10(GpioPin):
    """GPIO 10 (pin P1-19)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 10
    name = "Gpio10"


class Gpio11(GpioPin):
    """GPIO 11 (pin P1-23)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 11
    name = "Gpio11"


class Gpio14(GpioPin):
    """GPIO 14 (pin P1-08)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 14
    name = "Gpio14"


class Gpio15(GpioPin):
    """GPIO 15 (pin P1-10)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 15
    name = "Gpio15"


class Gpio17(GpioPin):
    """GPIO 17 (pin P1-11)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 17
    name = "Gpio17"


class Gpio18(GpioPin):
    """GPIO 18 (pin P1-12)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 18
    name = "Gpio18"


class Gpio21(GpioPin):
    """GPIO 21 (pin P1-13)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 21
    name = "Gpio21"


class Gpio22(GpioPin):
    """GPIO 22 (pin P1-15)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 22
    name = "Gpio22"


class Gpio23(GpioPin):
    """GPIO 23 (pin P1-16)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 23
    name = "Gpio23"


class Gpio24(GpioPin):
    """GPIO 24 (pin P1-18)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 24
    name = "Gpio24"


class Gpio25(GpioPin):
    """GPIO 25 (pin P1-22)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 25
    name = "Gpio25"


class Pin03(GpioPin):
    """Pin 3."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 0
    name = "Pin03"


class Pin05(GpioPin):
    """Pin 5."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 1
    name = "Pin05"


class Pin07(GpioPin):
    """Pin 7."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 4
    name = "Pin07"


class Pin08(GpioPin):
    """Pin 8."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 14
    name = "Pin08"


class Pin10(GpioPin):
    """Pin 10."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 15
    name = "Pin10"


class Pin11(GpioPin):
    """Pin 11."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 17
    name = "Pin11"


class Pin12(GpioPin):
    """Pin 12."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 18
    name = "Pin12"


class Pin13(GpioPin):
    """Pin 13."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 21
    name = "Pin13"


class Pin15(GpioPin):
    """Pin 15."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 22
    name = "Pin15"


class Pin16(GpioPin):
    """Pin 16."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 23
    name = "Pin16"


class Pin18(GpioPin):
    """Pin 18."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 24
    name = "Pin18"


class Pin19(GpioPin):
    """Pin 19."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 10
    name = "Pin19"


class Pin21(GpioPin):
    """Pin 21."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 9
    name = "Pin21"


class Pin22(GpioPin):
    """Pin 22."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 25
    name = "Pin22"


class Pin23(GpioPin):
    """Pin 23."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 11
    name = "Pin23"


class Pin24(GpioPin):
    """Pin 24."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 8
    name = "Pin24"


class Pin26(GpioPin):
    """Pin 26."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 7
    name = "Pin26"


class Led(GpioPin):
    """led driver pin."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 16
    name = "led"


class V2Gpio02(GpioPin):
    """Rev 2 GPIO 02 (P1-03)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 2
    name = "V2Gpio02"


class V2Gpio04(GpioPin):
    """Rev 2 GPIO 04 (pin P1-07)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 4
    name = "V2Gpio04"


class V2Gpio07(GpioPin):
    """Rev 2 GPIO 07 (pin P1-26)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 7
    name = "V2Gpio07"


class V2Gpio08(GpioPin):
    """Rev 2 GPIO 08 (pin P1-24)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 8
    name = "V2Gpio08"


class V2Gpio09(GpioPin):
    """Rev GPIO 09 (pin P1-21)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 9
    name = "V2Gpio09"


class V2Gpio10(GpioPin):
    """Rev 2 GPIO 10 (pin P1-19)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 10
    name = "V2Gpio10"


class V2Gpio11(GpioPin):
    """Rev 2 GPIO 11 (pin P1-23)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 11
    name = "V2Gpio11"


class V2Gpio14(GpioPin):
    """Rev 2 GPIO 14 (pin P1-08)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 14
    name = "V2Gpio14"


class V2Gpio15(GpioPin):
    """Rev 2 GPIO 15 (pin P1-10)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 15
    name = "V2Gpio15"


class V2Gpio17(GpioPin):
    """Rev 2 GPIO 17 (pin P1-11)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 17
    name = "V2Gpio17"


class V2Gpio18(GpioPin):
    """Rev 2 GPIO 18 (pin P1-12)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 18
    name = "V2Gpio18"


class V2Gpio22(GpioPin):
    """Rev 2 GPIO 22 (pin P1-15)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 22
    name = "V2Gpio22"


class V2Gpio23(GpioPin):
    """Rev 2 GPIO 23 (pin P1-16)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 23
    name = "V2Gpio23"


class V2Gpio24(GpioPin):
    """Rev 2 GPIO 24 (pin P1-18)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 24
    name = "V2Gpio24"


class V2Gpio25(GpioPin):
    """Rev 2 GPIO 25 (pin P1-22)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 25
    name = "V2Gpio25"


class V2Gpio27(GpioPin):
    """Rev 2 GPIO 27 (pin P1 - 13)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 27
    name = "V2Gpio27"


class V2Pin03(GpioPin):
    """Rev 2 Pin 3 (GPIO 02)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 2
    name = "V2Pin03"


class V2Pin05(GpioPin):
    """Rev 2 Pin 05 (GPIO 03)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 3
    name = "V2Pin05"


class V2Pin07(GpioPin):
    """Rev 2 Pin 01 (GPIO 04)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 4
    name = "V2Pin07"


class V2Pin08(GpioPin):
    """Rev 2 Pin 08 (GPIO 14)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 14
    name = "V2Pin08"


class V2Pin10(GpioPin):
    """Rev 2 Pin 10 (GPIO 15)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 15
    name = "V2Pin10"


class V2Pin11(GpioPin):
    """Rev 2 Pin 11 (GPIO 17)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 17
    name = "V2Pin11"


class V2Pin12(GpioPin):
    """Rev 2 Pin 12 (GPIO 18)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 18
    name = "V2Pin12"


class V2Pin13(GpioPin):
    """Rev 2 Pin 13 (GPIO 27)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 27
    name = "V2Pin13"


class V2Pin15(GpioPin):
    """Rev 2 Pin 15 (GPIO 22)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 22
    name = "V2Pin15"


class V2Pin16(GpioPin):
    """Rev 2 Pin 16 (GPIO 23)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 23
    name = "V2Pin16"


class V2Pin18(GpioPin):
    """Rev 2 Pin 18 (GPIO 24)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 24
    name = "V2Pin18"


class V2Pin19(GpioPin):
    """Rev 2 Pin 19 (GPIO 10)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 10
    name = "V2Pin19"


class V2Pin21(GpioPin):
    """Rev 2 Pin 21 (GPIO 09)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 9
    name = "V2Pin21"


class V2Pin22(GpioPin):
    """Rev 2 Pin 22 (GPIO 25)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 25
    name = "V2Pin22"


class V2Pin23(GpioPin):
    """Rev 2 Pin 23 (GPIO 11)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 11
    name = "V2Pin23"


class V2Pin24(GpioPin):
    """Rev 2 Pin 24 (GPIO 08)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 8
    name = "V2Pin24"


class V2Pin26(GpioPin):
    """Rev 2 Pin 26 (GPIO 07)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 7
    name = "V2Pin26"


class V2P5Pin03(GpioPin):
    """Rev 2 P5 header GPIO 28 (P5-03)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 28
    name = "V2P5Pin03"


class V2P5Pin04(GpioPin):
    """Rev 2 P5 header GPIO 29 (P5-04)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 29
    name = "V2P5Pin04"


class V2P5Pin05(GpioPin):
    """Rev 2 P5 header GPIO 30 (P5-05)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 30
    name = "V2P5Pin05"


class V2P5Pin06(GpioPin):
    """Rev 2 P5 header GPIO 31 (P5-06)."""

    def __init__(self):
        """ctor."""
        GpioPin.__init__(self)

    value = 31
    name = "V2P5Pin06"
