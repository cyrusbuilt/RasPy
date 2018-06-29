"""Temperature scale utility methods."""


from raspy import string_utils
from raspy.components.temperature import temp_scale


def get_scale_name(scale):
    """Get the name of the specified scale.

    :param int scale: The scale to get the name of.
    :returns: The name of the scale or an empty string if specified scale is
    invalid or unknown.
    :rtype: str
    """
    if scale == temp_scale.CELCIUS:
        return "Celcius"
    elif scale == temp_scale.FARENHEIT:
        return "Farenheit"
    elif scale == temp_scale.KELVIN:
        return "Kelvin"
    elif scale == temp_scale.RANKINE:
        return "Rankine"
    else:
        return string_utils.EMPTY


def get_scale_postfix(scale):
    """Get the scale postfix.

    :param int scale: The scale to get the postfix for.
    :returns: The scale postfix or an empty string if the specified scale is
    invalid or unknown.
    :rtype: str
    """
    name = get_scale_name(scale)
    if string_utils.is_null_or_empty(name):
        return string_utils.EMPTY
    return name[0]
