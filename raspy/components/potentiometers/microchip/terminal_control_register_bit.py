"""Terminal control register bits."""


TCON_RH02HW = 1 << 3
"""Wiper 0 and 2, hardware config."""

TCON_RH02A = 1 << 2
"""Wiper 0 and 2, Pin A."""

TCON_RH02W = 1 << 1
"""Wiper 0 and 2, Pin W."""

TCON_RH02B = 1 << 0
"""Wiper 0 and 2, Pin B."""

TCON_RH13HW = 1 << 7
"""Wiper 1 and 3, hardware config."""

TCON_RH13A = 1 << 6
"""Wiper 1 and 3, Pin A."""

TCON_RH13W = 1 << 5
"""Wiper 1 and 3, Pin W."""

TCON_RH13B = 1 << 4
"""Wiper 1 and 3, Pin B."""

NONE = 0x00
"""Null bit."""
