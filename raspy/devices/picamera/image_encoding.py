"""Image encoding formats."""


JPEG = 0
"""JPEG image encoding.

NOTE: This is the only supported format that is hardware accelerated. All
other image types will take much longer to save because the are not
accelerated.
"""

BITMAP = 1
"""Bitmap image encoding."""

GIF = 2
"""GIF image encoding."""

PNG = 3
"""PNG image encoding."""
