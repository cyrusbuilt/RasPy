"""This module contains utility methods for working with pins."""


from raspy import string_utils
from raspy.io import pin_mode
from raspy.io.io_exception import IOException


def get_pin_mode_name(mode):
    """Convert the specified mode to its name string.

    :param int mode: The mode to get the name of.
    :returns: The mode name.
    :rtype: string
    """
    if not isinstance(mode, (int, long)):
        return string_utils.EMPTY

    if mode == pin_mode.IN:
        return "IN"

    elif mode == pin_mode.OUT:
        return "OUT"

    elif mode == pin_mode.PWM:
        return "PWM"

    elif mode == pin_mode.CLOCK:
        return "CLOCK"

    elif mode == pin_mode.UP:
        return "UP"

    elif mode == pin_mode.DOWN:
        return "DOWN"

    elif mode == pin_mode.TRI:
        return "TRI"

    else:
        return string_utils.EMPTY


def write_fs_pin(pin_path, val_string):
    """Write the specified string to the specified pin.

    :param string pin_path: The full path to the pin to write to.
    :param string val_string: The value string to write to the pin.
    :raises: raspy.io.io_exception.IOException if an IOError occurred while
    accessing the pin.
    """
    try:
        target = open(pin_path, 'w')
        target.write(val_string)
        target.close()
    except IOError as ex:
        raise IOException(ex.strerror)


def read_fs_pin(pin_path):
    """Read the value from the specified pin.

    :param string pin_path: The full path to the pin to write to.
    :returns: The value read from the pin.
    :rtype: int
    :raises: raspy.io.io_exception.IOException if an IOError occurred while
    accessing the pin.
    """
    try:
        target = open(pin_path, 'r')
        read_string = target.read()
        val = int(read_string[0:1])
        target.close()
    except IOError as ex:
        raise IOException(ex.strerror)

    return val
