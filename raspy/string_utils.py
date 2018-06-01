"""This module provides utility methods and constants for working with strings."""

import itertools
from raspy.illegal_argument_exception import IllegalArgumentException


DEFAULT_PAD_CHAR = ' '
"""Default padding character"""

EMPTY = ""
"""Represents an empty string."""


def is_null_or_empty(string_val):
    """Null or empty string check.

    A utility method to check to see if the specified string is null or empty.

    :param str string_val: The value to check.
    :returns: True if null or empty; Otherwise, False.
    :rtype: bool
    """
    if string_val and string_val.strip():
        return False
    return True


def create(char, length):
    """Create a string.

    Create a string from the specified character or string.

    :param str char: The character or string to create the string from. If
    null or an empty string, then DEFAULT_PAD_CHAR is used instead.
    :param int length: The number of instances or the specified character of
    the specified character or string to construct the string from.
    :returns: The created string.
    :rtype: str
    """
    if is_null_or_empty(char):
        char = DEFAULT_PAD_CHAR

    string_buf = EMPTY
    for the_char in itertools.repeat(char, length):
        string_buf += the_char

    return string_buf


def pad_left(data, padding_char, length):
    """Pad the left side of the specified string.

    Adds the specified padding characters to the left side of the specified
    string.

    :param str data: The string to pad.
    :param str padding_char: The character or string to pad the specified
    string with. If null or empty string, the DEFAULT_PAD_CHAR will be used
    instead.
    :param int length: The number of pad characters or instances of string to
    inject.
    :returns: The padded version of the string.
    :rtype: str
    """
    if is_null_or_empty(padding_char):
        padding_char = DEFAULT_PAD_CHAR

    string_buf = EMPTY
    for the_char in itertools.repeat(padding_char, length):
        string_buf += the_char

    string_buf += data
    return string_buf


def pad_right(data, padding_char, length):
    """Pad the right side of the specified string.

    Adds the specified padding characters to the right side of the specified
    string.

    :param str data: The string to pad.
    :param str padding_char: The character or string to pad the specified
    string with. If null or empty string, DEFAULT_PAD_CHAR will be used
    instead.
    :param int length: The number of padding characters or instances of string
    to use.
    :returns: The padded version of the string.
    :rtype: str
    """
    if is_null_or_empty(padding_char):
        padding_char = DEFAULT_PAD_CHAR

    string_buf = data
    for the_char in itertools.repeat(padding_char, length):
        string_buf += the_char

    return string_buf


def pad(data, padding_char, length):
    """Pad the specified string on both sides.

    Adds the specified padding character(s) to both sides of the specified
    string.

    :param str data: The string to pad.
    :param str padding_char: The character or string to pad the specified
    string with. If null or empty string, DEFAULT_PAD_CHAR will be used
    instead.
    :param int length: The number of characters or instances of string to pad
    on both sides.
    :returns: The padded version of the string.
    :rtype: str
    """
    if is_null_or_empty(padding_char):
        padding_char = DEFAULT_PAD_CHAR

    padded = create(padding_char, length)
    string_buf = padded + data + padded
    return string_buf


def pad_center(data, char, length):
    """Pad the center of the specified string.

    Adds the specified padding character(s) to the center of the specified
    string.

    :param str data: The string to pad.
    :param str char: The character or string to pad the center of the
    specified string with. If null or empty string, DEFAULT_PAD_CHAR will be
    used instead.
    :param int length: The number of characters or instances of string to pad
    the center with.
    :returns: The padded version of the string.
    :rtype: str
    :raises raspy.illegal_argument_exception.IllegalArgumentException: if data
    param is null or not a string.
    """
    if is_null_or_empty(data):
        raise IllegalArgumentException("data param must be a string.")

    if is_null_or_empty(char):
        char = DEFAULT_PAD_CHAR

    if len(data) > 2 and length > 0:
        first_half = data[:len(data) / 2]
        second_half = data[len(data) / 2:len(data)]
        padding_char = create(char, length)
        string_buf = first_half + padding_char + second_half
        return string_buf

    return data


def ends_with(strn, suffix):
    """Check to see if the specified string ends with the suffix.

    Checks the specified string to see if it ends with the specified suffix.

    :param str strn: The string to check.
    :param str suffix: The suffix to search the specified string for.
    :returns: True if the string ends with the specified suffix; Otherwise,
    False.
    :rtype: bool
    """
    return strn.endswith(suffix)


def starts_with(strn, prefix):
    """Check to see if string begins with the prefix.

    Checks to see if the specified string begins with the specified prefix.

    :param str strn: The string to check.
    :param str prefix: The prefix to search the specified string for.
    :returns: True if the string starts with the specified prefix; Otherwise,
    False.
    :rtype: bool
    """
    return strn.startswith(prefix)


def trim(strn):
    """Trim whitespace from string.

    Trims all whitespace from the beginning and end of the specified string.

    :param str strn: The string to trim.
    :returns: The resulting (trimmed) string.
    :rtype: str
    """
    if is_null_or_empty(strn):
        return EMPTY

    return strn.strip()


def contains(strn, substr):
    """Check to see if string contains string.

    Checks to see if the specified string contains the specified substring.

    :param str strn: The string to check.
    :param str substr: The string to search for.
    :returns: True if at least one instance of the specified substring was
    found within the specified string; Otherwise, False.
    :rtype: bool
    """
    try:
        strn.index(substr)
        return True
    except ValueError:
        return False


def convert_string_to_byte(strn):
    """Convert string value to byte.

    Converts the specified string value to a bit array (byte).

    :param str strn: The string representing a byte value (ie. '00000000').
    :returns: The byte value.
    :rtype: array
    """
    result = []
    for _key, val in enumerate(strn):
        string_array = []
        char = ord(val)
        while char:
            string_array.append(char & 0xFF)
            char >>= 8
        result += reversed(string_array)

    return result
