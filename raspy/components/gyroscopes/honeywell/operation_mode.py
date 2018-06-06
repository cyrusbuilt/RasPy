"""Possible operation modes for the Honeywell gyro."""


CONTINUOUS = 0
"""Continuous sample mode. Continuously takes measurements."""

SINGLE_SAMPLE = 1
"""Single sample mode. Default power-up mode.

In this mode, the gyro will take a single sample and then switch to idle mode.
"""

IDLE = 2
"""Idle mode (no sampling)."""
