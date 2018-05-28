"""PiFace I/O pins.

PiFacePins.py

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
"""


class OUTPUT00:
    """Output pin 1 (relay 1)."""

    value = 1
    name = "Output 1 (RELAY 1)"


class OUTPUT01:
    """Output pin 2 (RELAY 2)."""

    value = 2
    name = "Output 2 (RELAY 2)"


class OUTPUT02:
    """Output pin 3."""

    value = 4
    name = "Output 3"


class OUTPUT03:
    """Output pin 4."""

    value = 8
    name = "Output 4"


class OUTPUT04:
    """Output pin 5."""

    value = 16
    name = "Output 5"


class OUTPUT05:
    """Output pin 6."""

    value = 32
    name = "Output 6"


class OUTPUT06:
    """Output pin 7."""

    value = 64
    name = "Output 7"


class OUTPUT07:
    """Output pin 8."""

    value = 128
    name = "Output 8"


class INPUT00:
    """Input pin 1 (switch 1)."""

    value = 1001
    name = "Input 1 (SWITCH 1)"


class INPUT01:
    """Input pin 2 (switch 2)."""

    value = 1002
    name = "Input 2 (SWITCH 2)"


class INPUT02:
    """Input pin 3 (switch 3)."""

    value = 1004
    name = "Input 3 (SWITCH 3)"


class INPUT03:
    """Input pin 4 (switch 4)."""

    value = 1008
    name = "Input 4 (SWITCH 4)"


class INPUT04:
    """Input pin 5."""

    value = 1016
    name = "Input 5"


class INPUT05:
    """Input pin 6."""

    value = 1032
    name = "Input 6"


class INPUT06:
    """Input pin 7."""

    value = 1064
    name = "Input 7"


class INPUT07:
    """Input pin 8."""

    value = 1128
    name = "Input 8"


class NONE:
    """No pin assignment."""

    value = 0
    name = "None"
