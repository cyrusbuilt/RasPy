"""Possible GPIO pins.

GpioPins.py

Author:
      Chris Brunner <cyrusbuilt at gmail dot com>

  Copyright (c) 2015 CyrusBuilt

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


 The various GPIO pins on the Raspberry Pi Revision 1.0 and 2.0 boards.
 Refer to http://elinux.org/Rpi_Low-level_peripherals for diagram.
 P1-01 = bottom left, P1-02 = top left
 pi connector P1 pin    = GPIOnum
                   P1-03 = GPIO0
                   P1-05 = GPIO1
                   P1-07 = GPIO4
                   P1-08 = GPIO14 - alt function (UART0_TXD) on boot-up
                   P1-10 = GPIO15 - alt function (UART0_TXD) on boot-up
                   P1-11 = GPIO17
                   P1-12 = GPIO18
                   P1-13 = GPIO21
                   P1-15 = GPIO22
                   P1-16 = GPIO23
                   P1-18 = GPIO24
                   P1-19 = GPIO10
                   P1-21 = GPIO9
                   P1-22 = GPIO25
                   P1-23 = GPIO11
                   P1-24 = GPIO8
                   P1-26 = GPIO7
 So to turn on Pin7 on the GPIO connector, pass in GpioPins.GPIO04 as
 the pin parameter.
"""


class GPIO_NONE:
    """No pin (null)."""

    value = -1
    name = "GPIO_NONE"


class GPIO00:
    """GPIO 00 (pin P1-03)."""

    value = 0
    name = "GPIO00"


class GPIO01:
    """GPIO 01 (pin P1-05)."""

    value = 1
    name = "GPIO01"


class GPIO04:
    """GPIO 04 (pin P1-07)."""

    value = 4
    name = "GPIO04"


class GPIO07:
    """GPIO 07 (pin P1-26)."""

    value = 7
    name = "GPIO07"


class GPIO08:
    """GPIO 08 (pin P1-24)."""

    value = 8
    name = "GPIO08"


class GPIO09:
    """GPIO 09 (pin P1-21)."""

    value = 9
    name = "GPIO09"


class GPIO10:
    """GPIO 10 (pin P1-19)."""

    value = 10
    name = "GPIO10"


class GPIO11:
    """GPIO 11 (pin P1-23)."""

    value = 11
    name = "GPIO11"


class GPIO14:
    """GPIO 14 (pin P1-08)."""

    value = 14
    name = "GPIO14"


class GPIO15:
    """GPIO 15 (pin P1-10)."""

    value = 15
    name = "GPIO15"


class GPIO17:
    """GPIO 17 (pin P1-11)."""

    value = 17
    name = "GPIO17"


class GPIO18:
    """GPIO 18 (pin P1-12)."""

    value = 18
    name = "GPIO18"


class GPIO21:
    """GPIO 21 (pin P1-13)."""

    value = 21
    name = "GPIO21"


class GPIO22:
    """GPIO 22 (pin P1-15)."""

    value = 22
    name = "GPIO22"


class GPIO23:
    """GPIO 23 (pin P1-16)."""

    value = 23
    name = "GPIO23"


class GPIO24:
    """GPIO 24 (pin P1-18)."""

    value = 24
    name = "GPIO24"


class GPIO25:
    """GPIO 25 (pin P1-22)."""

    value = 25
    name = "GPIO25"


class PIN03:
    """Pin 3."""

    value = 0
    name = "Pin03"


class PIN05:
    """Pin 5."""

    value = 1
    name = "Pin05"


class PIN07:
    """Pin 7."""

    value = 4
    name = "Pin07"


class PIN08:
    """Pin 8."""

    value = 14
    name = "Pin08"


class PIN10:
    """Pin 10."""

    value = 15
    name = "Pin10"


class PIN11:
    """Pin 11."""

    value = 17
    name = "Pin11"


class PIN12:
    """Pin 12."""

    value = 18
    name = "Pin12"


class PIN13:
    """Pin 13."""

    value = 21
    name = "Pin13"


class PIN15:
    """Pin 15."""

    value = 22
    name = "Pin15"


class PIN16:
    """Pin 16."""

    value = 23
    name = "Pin16"


class PIN18:
    """Pin 18."""

    value = 24
    name = "Pin18"


class PIN19:
    """Pin 19."""

    value = 10
    name = "Pin19"


class PIN21:
    """Pin 21."""

    value = 9
    name = "Pin21"


class PIN22:
    """Pin 22."""

    value = 25
    name = "Pin22"


class PIN23:
    """Pin 23."""

    value = 11
    name = "Pin23"


class PIN24:
    """Pin 24."""

    value = 8
    name = "Pin24"


class PIN26:
    """Pin 26."""

    value = 7
    name = "Pin26"


class LED:
    """LED driver pin."""

    value = 16
    name = "LED"


class V2_GPIO02:
    """Rev 2 GPIO 02 (P1-03)."""

    value = 2
    name = "V2_GPIO02"


class V2_GPIO04:
    """Rev 2 GPIO 04 (pin P1-07)."""

    value = 4
    name = "V2_GPIO04"


class V2_GPIO07:
    """Rev 2 GPIO 07 (pin P1-26)."""

    value = 7
    name = "V2_GPIO07"


class V2_GPIO08:
    """Rev 2 GPIO 08 (pin P1-24)."""

    value = 8
    name = "V2_GPIO08"


class V2_GPIO09:
    """Rev GPIO 09 (pin P1-21)."""

    value = 9
    name = "V2_GPIO09"


class V2_GPIO10:
    """Rev 2 GPIO 10 (pin P1-19)."""

    value = 10
    name = "V2_GPIO10"


class V2_GPIO11:
    """Rev 2 GPIO 11 (pin P1-23)."""

    value = 11
    name = "V2_GPIO11"


class V2_GPIO14:
    """Rev 2 GPIO 14 (pin P1-08)."""

    value = 14
    name = "V2_GPIO14"


class V2_GPIO15:
    """Rev 2 GPIO 15 (pin P1-10)."""

    value = 15
    name = "V2_GPIO15"


class V2_GPIO17:
    """Rev 2 GPIO 17 (pin P1-11)."""

    value = 17
    name = "V2_GPIO17"


class V2_GPIO18:
    """Rev 2 GPIO 18 (pin P1-12)."""

    value = 18
    name = "V2_GPIO18"


class V2_GPIO22:
    """Rev 2 GPIO 22 (pin P1-15)."""

    value = 22
    name = "V2_GPIO22"


class V2_GPIO23:
    """Rev 2 GPIO 23 (pin P1-16)."""

    value = 23
    name = "V2_GPIO23"


class V2_GPIO24:
    """Rev 2 GPIO 24 (pin P1-18)."""

    value = 24
    name = "V2_GPIO24"


class V2_GPIO25:
    """Rev 2 GPIO 25 (pin P1-22)."""

    value = 25
    name = "V2_GPIO25"


class V2_GPIO27:
    """Rev 2 GPIO 27 (pin P1 - 13)."""

    value = 27
    name = "V2_GPIO27"


class V2_PIN03:
    """Rev 2 Pin 3 (GPIO 02)."""

    value = 2
    name = "V2_PIN03"


class V2_PIN05:
    """Rev 2 Pin 05 (GPIO 03)."""

    value = 3
    name = "V2_PIN05"


class V2_PIN07:
    """Rev 2 Pin 01 (GPIO 04)."""

    value = 4
    name = "V2_PIN07"


class V2_PIN08:
    """Rev 2 Pin 08 (GPIO 14)."""

    value = 14
    name = "V2_PIN08"


class V2_PIN10:
    """Rev 2 Pin 10 (GPIO 15)."""

    value = 15
    name = "V2_PIN10"


class V2_PIN11:
    """Rev 2 Pin 11 (GPIO 17)."""

    value = 17
    name = "V2_PIN11"


class V2_PIN12:
    """Rev 2 Pin 12 (GPIO 18)."""

    value = 18
    name = "V2_PIN12"


class V2_PIN13:
    """Rev 2 Pin 13 (GPIO 27)."""

    value = 27
    name = "V2_PIN13"


class V2_PIN15:
    """Rev 2 Pin 15 (GPIO 22)."""

    value = 22
    name = "V2_PIN15"


class V2_PINT16:
    """Rev 2 Pin 16 (GPIO 23)."""

    value = 23
    name = "V2_PINT16"


class V2_PIN18:
    """Rev 2 Pin 18 (GPIO 24)."""

    value = 24
    name = "V2_PIN18"


class V2_PIN19:
    """Rev 2 Pin 19 (GPIO 10)."""

    value = 10
    name = "V2_PIN19"


class V2_PIN21:
    """Rev 2 Pin 21 (GPIO 09)."""

    value = 9
    name = "V2_PIN21"


class V2_PIN22:
    """Rev 2 Pin 22 (GPIO 25)."""

    value = 25
    name = "V2_PIN22"


class V2_PIN23:
    """Rev 2 Pin 23 (GPIO 11)."""

    value = 11
    name = "V2_PIN23"


class V2_PIN24:
    """Rev 2 Pin 24 (GPIO 08)."""

    value = 8
    name = "V2_PIN24"


class V2_PIN26:
    """Rev 2 Pin 26 (GPIO 07)."""

    value = 7
    name = "V2_PIN26"


class V2_P5_PIN03:
    """Rev 2 P5 header GPIO 28 (P5-03)."""

    value = 28
    name = "V2_P5_PIN03"


class V2_P5_PIN04:
    """Rev 2 P5 header GPIO 29 (P5-04)."""

    value = 29
    name = "V2_P5_PIN04"


class V2_P5_PIN05:
    """Rev 2 P5 header GPIO 30 (P5-05)."""

    value = 30
    name = "V2_P5_PIN05"


class V2_P5_PIN06:
    """Rev 2 P5 header GPIO 31 (P5-06)."""

    value = 31
    name = "V2_P5_PIN06"
