"""Device status bits."""


RESERVED_MASK = 0x0000111110000
"""Reserved mask."""

RESERVED_VALUE = 0x0000111110000
"""Reserved value."""

EEPROM_WRITE_ACTIVE = 0x1000
"""EEPROM write is active."""

WIPER_LOCK1 = 0x0100
"""Wiper lock 1 active."""

WIPER_LOCK0 = 0x0010
"""Wiper lock 0 active."""

EEPROM_WRITE_PROTECTION = 0x0001
"""EEPROM write protection."""

NONE = 0x00
"""Null bit."""
