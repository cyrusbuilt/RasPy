"""MCP45XX and MCP46XX commands."""


WRITE = 0x00 << 2
"""Writes to the device."""

INCREASE = 0x01 << 2
"""Increase the resistance."""

DECREASE = 0x02 << 2
"""Decrease the resistance."""

READ = 0x03 << 2
"""Read the current value."""
