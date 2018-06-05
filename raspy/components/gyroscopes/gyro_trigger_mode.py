"""Possible triggers for reading data from a gyroscopes."""


READ_NOT_TRIGGERED = 0
"""The read will not be triggered."""

GET_ANGLE_TRIGGER_READ = 1
"""Trigger the device read when requesting the angle."""

GET_ANGULAR_VELOCITY_TRIGGER_READ = 2
"""Trigger the device read when requesting angular velocity."""

GET_RAW_VALUE_TRIGGER_READ = 4
"""Trigger the device read when requesting the raw value."""
