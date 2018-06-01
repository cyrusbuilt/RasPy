"""Flags for LCD commands."""


CLEAR_DISPLAY = 0x01
"""Clears the display."""

RETURN_HOME = 0x02
"""Return the cursor to the home position."""

ENTRY_MODE_SET = 0x04
"""Set entry mode."""

DISPLAY_CONTROL = 0x08
"""Display control."""

CURSOR_SHIFT = 0x10
"""Shift the cursor."""

FUNCTION_SET = 0x20
"""Set function."""

SET_CG_RAM_ADDR = 0x40
"""Set CG RAM address."""

SET_DD_RAM_ADDR = 0x80
"""Set DD RAM address."""
