"""Provides utility methods and constants for working with strings.

StringUtils.py

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


import IllegalArgumentException


DEFAULT_PAD_CHAR = ' '
"""Default padding character"""

EMPTY = ""
"""Represents an empty string."""


def is_null_or_empty(stringVal):
    """Null or empty string check.

    A utility method to check to see if the specified string is null or empty.

    :param stringVal: The value to check.
    :type stringVal: string
    :returns: True if null or empty; Otherwise, False.
    :rtype: bool
    """
    if stringVal and stringVal.strip():
        return False
    return True


def create(c, length):
    """Create a string.

    Create a string from the specified character or string.

    :param c: The character or string to creat the string from. If null or an
    empty string, then DEFAULT_PAD_CHAR is used instead.
    :param length: The number of instances or the specified character of the
    specified character or string to construct the string from.
    :type c: string
    :type length: int
    :returns: The created string.
    :rtype: string
    """
    if is_null_or_empty(c):
        c = DEFAULT_PAD_CHAR

    sb = EMPTY
    for i in range(0, length):
        sb += c

    return sb


def pad_left(data, pad, length):
    """Pad the left side of the specified string.

    Adds the specified padding characters to the left side of the specified
    string.

    :param data: The string to pad.
    :param pad: The character or string to pad the specified string with. If
    null or empty string, the DEFAULT_PAD_CHAR will be used instead.
    :param length: The number of pad characters or instances of string to
    inject.
    :type data: string
    :type pad: string
    :type length: int
    :returns: The padded version of the string.
    :rtype: string
    """
    if is_null_or_empty(pad):
        pad = DEFAULT_PAD_CHAR

    sb = EMPTY
    for i in range(0, length):
        sb += pad

    sb += data
    return sb


def pad_right(data, pad, length):
    """Pad the right side of the specified string.

    Adds the specified padding characters to the right side of the specified
    string.

    :param data: The string to pad.
    :param pad: The character or string to pad the specifed string with. If
    null or empty string, DEFAULT_PAD_CHAR will be used instead.
    :param length: The number of padding characters or instances of string to
    use.
    :type data: string
    :type pad: string
    :type length: int
    :returns: The padded version of the string.
    :rtype: string
    """
    if is_null_or_empty(pad):
        pad = DEFAULT_PAD_CHAR

    sb = data
    for i in range(0, length):
        sb += pad

    return sb


def pad(data, pad, length):
    """Pad the specifed string on both sides.

    Adds the specified padding character(s) to both sides of the specified
    string.

    :param data: The string to pad.
    :param pad: The character or string to pad the specified string with. If
    null or empty string, DEFAULT_PAD_CHAR will be used instead.
    :param length: The number of characters or instances of string to pad on
    both sides.
    :type data: string
    :type pad: string
    :type length: int
    :returns: The padded version of the string.
    :rtype: string
    """
    if is_null_or_empty(pad):
        pad = DEFAULT_PAD_CHAR

    p = create(pad, length)
    sb = p + data + p
    return sb


def pad_center(data, c, length):
    """Pad the center of the specified string.

    Adds the specified padding character(s) to the center of the specified
    string.

    :param data: The string to pad.
    :param c: The character or string to pad the center of the specified string
    with. If null or empty string, DEFAULT_PAD_CHAR will be used instead.
    :param length: The number of characters or instances of string to pad the
    center with.
    :returns: The padded version of the string.
    :rtype: string
    :raises IllegalArgumentException: if data param is null or not a string.
    """
    if is_null_or_empty(data):
        raise IllegalArgumentException("data param must be a string.")

    if is_null_or_empty(c):
        c = DEFAULT_PAD_CHAR

    if len(data) > 2 and length > 0:
        firstHalf = data[:len(data) / 2]
        secondHalf = data[len(data) / 2:len(data)]
        pad = create(c, length)
        sb = firstHalf + pad + secondHalf
        return sb

    return data


def ends_with(str, suffix):
    """Check to see if the specified string ends with the suffix.

    Checks the specified string to see if it ends with the specified suffix.

    :param str: The string to check.
    :param suffix: The suffix to search the specified string for.
    :type str: string
    :type suffix: string
    :returns: True if the string ends with the specified suffix; Otherwise,
    False.
    :rtype: bool
    """
    return str.endswith(suffix)


def starts_with(str, prefix):
    """Check to see if string begins with the prefix.

    Checks to see if the specified string begins with the specified prefix.

    :param str: The string to check.
    :param prefix: The prefix to search the specified string for.
    :type str: string
    :type prefix: string
    :returns: True if the string starts with the specified prefix; Otherwise,
    False.
    :rtype: bool
    """
    return str.startswith(prefix)


def trim(str):
    """Trim whitespace from string.

    Trims all whitespace from the beginning and end of the specified string.

    :param str: The string to trim.
    :type str: string
    :returns: The resulting (trimmed) string.
    :rtype: string
    """
    if is_null_or_empty(str):
        return EMPTY

    return str.strip()


def contains(str, substr):
    """Check to see if string contains string.

    Checks to see if the specified string contains the specified substring.

    :param str: The string to check.
    :param substr: The string to search for.
    :type str: string
    :type substr: string
    :returns: True if at least one instance of the specified substring was
    found within the specified string; Otherwise, False.
    :rtype: bool
    """
    try:
        str.index(substr)
        return True
    except ValueError:
        return False


def convert_string_to_byte(str):
    """Convert string value to byte.

    Converts the specified string value to a bit array (byte).

    :param str: The string representing a byte value (ie. '00000000').
    :type str: string
    :returns: The byte value.
    :rtype: array
    """
    ch = 0
    st = []
    re = []
    for i in range(0, len(str)):
        st = []
        ch = ord(str[i])
        while ch:
            st.append(ch & 0xFF)
            ch >>= 8
        re += reversed(st)

    return re
