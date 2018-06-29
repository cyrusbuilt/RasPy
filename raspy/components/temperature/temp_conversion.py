"""Temperature conversion utilities."""


from raspy.components.temperature import temp_scale


ABSOLUTE_ZERO_CELCIUS = -273.15
"""Absolute zero temperature in Celcius scale."""

ABSOLUTE_ZERO_FARENHEIT = -459.67
"""Absolute zero temperature in Farenheit scale."""

ABSOLUTE_ZERO_KELVIN = 0
"""Absolute zero temperature in Kelvin scale."""

ABSOLUTE_ZERO_RANKINGE = 0
"""Absolute zero temperature in Rankine scale."""


def convert_rankine_to_kelvin(temp):
    """Convert the temperature from Rankine to Kelvin scale.

    :param float temp: The temperature in degrees Rankine.
    :returns: The temperature in degrees Kelvin.
    :rtype: float
    """
    return (temp * 5) / 9


def convert_rankine_to_celcius(temp):
    """Convert the temperature from Rankine to Celcius scale.

    :param float temp: The temperature in degrees Rankine.
    :returns: The temperature in degrees Celcius.
    :rtype: float
    """
    return ((temp - 491.67) * 5) / 9


def convert_rankine_to_farenheit(temp):
    """Convert the temperature from Rankine to Farenheit scale.

    :param float temp: The temperature in degrees Rankine.
    :returns: The temperature in degrees Farenheit.
    :rtype: float
    """
    return temp - 459.67


def convert_kelvin_to_rankine(temp):
    """Convert the temperature from Kelvin to Rankine scale.

    :param float temp: The temperature in degrees Kelvin.
    :returns: The temperature in degrees Rankine.
    :rtype: float
    """
    return (temp * 9) / 5


def convert_kelvin_to_farenheit(temp):
    """Convert the temperature from Kelvin to Farenheit scale.

    :param float temp: The temperature in degrees Kelvin.
    :returns: The temperature in degrees Farenheit.
    :rtype: float
    """
    return ((temp * 9) / 5) - 459.67


def convert_kelvin_to_celcius(temp):
    """Convert the temperature from Kelvin to Celcius scale.

    :param float temp: The temperature in degrees Kelvin.
    :returns: The temperature in degrees Celcius.
    :rtype: float
    """
    return temp + ABSOLUTE_ZERO_CELCIUS


def convert_celcius_to_rankine(temp):
    """Convert the temperature from Celcius to Rankine scale.

    :param float temp: The temperature in degrees Celcius.
    :returns: The temperature in degrees Rankine.
    :rtype: float
    """
    return ((temp - ABSOLUTE_ZERO_CELCIUS) * 9) / 5


def convert_celcius_to_kelvin(temp):
    """Convert the temperature from Celcius to Kelvin scale.

    :param float temp: The temperature in degrees Celcius.
    :returns: The temperature in degrees Kelvin.
    :rtype: float
    """
    return temp - ABSOLUTE_ZERO_CELCIUS


def convert_celcius_to_farenheit(temp):
    """Convert the temperature from Celcius to Farenheit scale.

    :param float temp: The temperature in degrees Celcius.
    :returns: The temperature in degrees Farenheit.
    :rtype: float
    """
    return ((temp * 9) / 5) + 32


def convert_farenheit_to_rankine(temp):
    """Convert the temperature from Farenheit to Rankine scale.

    :param float temp: The temperature in degrees Farenheit.
    :returns: The temperature in degrees Rankine.
    :rtype: float
    """
    return temp + 459.67


def convert_farenheit_to_kelvin(temp):
    """Convert the temperature from Farenheit to Kelvin scale.

    :param float temp: The temperature in degrees Farenheit.
    :returns: The temperature in degrees Kelvin.
    :rtype: float
    """
    return ((temp + 459.67) * 5) / 9


def convert_farenheit_to_celcius(temp):
    """Convert the temperature from Farenheit to Celcius scale.

    :param float temp: The temperature in degrees Farenheit.
    :returns: The temperature in degrees Celcius.
    :rtype: float
    """
    return (temp - 32) * 5 / 9


def convert_to_rankine(scale, temp):
    """Convert the specified temperature value to Rankine scale.

    :param int scale: The temperature scale to convert from.
    :param float temp: The temperature value to convert to Rankine scale.
    :returns: The temperature in degrees Rankine.
    :rtype: float
    """
    if scale == temp_scale.FARENHEIT:
        return convert_farenheit_to_rankine(temp)
    elif scale == temp_scale.CELCIUS:
        return convert_celcius_to_rankine(temp)
    elif scale == temp_scale.KELVIN:
        return convert_kelvin_to_rankine(temp)
    elif scale == temp_scale.RANKINE:
        return temp
    else:
        return 0.0


def convert_from_rankine(scale, temp):
    """Convert the specified temperature in Rankine to the specified scale.

    :param int scale: The scale to convert the specified Rankine value to.
    :param float temp: The temperature value in degrees Rankine.
    :returns: The temperature value in the specified scale.
    :rtype: float
    """
    if scale == temp_scale.FARENHEIT:
        return convert_rankine_to_farenheit(temp)
    elif scale == temp_scale.CELCIUS:
        return convert_rankine_to_celcius(temp)
    elif scale == temp_scale.KELVIN:
        return convert_rankine_to_kelvin(temp)
    elif scale == temp_scale.RANKINE:
        return temp
    else:
        return 0.0


def convert_to_kelvin(scale, temp):
    """Convert the specified value from the specified scale to degrees Kelvin.

    :param int scale: The temperature scale to convert the value from.
    :param float temp: The temperature value to convert.
    :returns: The temperature value in degrees Kelvin.
    :rtype: float
    """
    if scale == temp_scale.FARENHEIT:
        return convert_farenheit_to_kelvin(temp)
    elif scale == temp_scale.CELCIUS:
        return convert_celcius_to_kelvin(temp)
    elif scale == temp_scale.KELVIN:
        return temp
    elif scale == temp_scale.RANKINE:
        return convert_rankine_to_kelvin(temp)
    else:
        return 0.0


def convert_from_kelvin(scale, temp):
    """Convert the specified temperature from Kelvin to the specified scale.

    :param int scale: The temperature scale to convert the value from.
    :param float temp: The temperature in degrees Kelvin.
    :returns: The temperature value in the specified scale.
    :rtype: float
    """
    if scale == temp_scale.FARENHEIT:
        return convert_kelvin_to_farenheit(temp)
    elif scale == temp_scale.CELCIUS:
        return convert_kelvin_to_celcius(temp)
    elif scale == temp_scale.KELVIN:
        return temp
    elif scale == temp_scale.RANKINE:
        return convert_kelvin_to_rankine(temp)
    else:
        return 0.0


def convert_to_celcius(scale, temp):
    """Convert the specified temperature to Celcius scale.

    :param int scale: The scale to convert to Celcius.
    :param float temp: The temperature value to convert.
    :returns: The temperature in degrees Celcius.
    :rtype: float
    """
    if scale == temp_scale.FARENHEIT:
        return convert_farenheit_to_celcius(temp)
    elif scale == temp_scale.CELCIUS:
        return temp
    elif scale == temp_scale.KELVIN:
        return convert_kelvin_to_celcius(temp)
    elif scale == temp_scale.RANKINE:
        return convert_rankine_to_celcius(temp)
    else:
        return 0.0


def convert_from_celcius(scale, temp):
    """Convert the specified temperature value in Celcius to the scale.

    :param int scale: The scale to convert the temperature value to.
    :param float temp: The temperature in degrees Celcius.
    :returns: The temperature value in the specified scale.
    :rtype: float
    """
    if scale == temp_scale.FARENHEIT:
        return convert_celcius_to_farenheit(temp)
    elif scale == temp_scale.CELCIUS:
        return temp
    elif scale == temp_scale.KELVIN:
        return convert_celcius_to_kelvin(temp)
    elif scale == temp_scale.RANKINE:
        return convert_celcius_to_rankine(temp)
    else:
        return 0.0


def convert_to_farenheit(scale, temp):
    """Convert the specified temperature value to Farenheit scale.

    :param int scale: The scale to convert the temperature from.
    :param float temp: The temperature value in the specified scale.
    :returns: The temperature in degrees Farenheit.
    :rtype: float
    """
    if scale == temp_scale.FARENHEIT:
        return temp
    elif scale == temp_scale.CELCIUS:
        return convert_celcius_to_farenheit(temp)
    elif scale == temp_scale.KELVIN:
        return convert_celcius_to_farenheit(temp)
    elif scale == temp_scale.RANKINE:
        return convert_rankine_to_farenheit(temp)
    else:
        return 0.0


def convert_from_farenheit(scale, temp):
    """Convert the temperature in degrees Farenheit to the specified scale.

    :param int scale: The scale to convert to.
    :param float temp: The temperature in degrees Farenheit.
    :returns: The temperature value in the specified scale.
    :rtype: float
    """
    if scale == temp_scale.FARENHEIT:
        return temp
    elif scale == temp_scale.CELCIUS:
        return convert_farenheit_to_celcius(temp)
    elif scale == temp_scale.KELVIN:
        return convert_farenheit_to_kelvin(temp)
    elif scale == temp_scale.RANKINE:
        return convert_farenheit_to_rankine(temp)
    else:
        return 0.0


def convert(from_scale, to_scale, temp):
    """Convert the specified temperature from one scale to another.

    :param int from_scale: The scale to convert from.
    :param int to_scale: The scale to convert to.
    :param float temp: The temperature value to convert.
    :returns: The temperature in degrees matching the 'to' scale.
    :rtype: float
    """
    if from_scale == temp_scale.FARENHEIT:
        return convert_from_farenheit(to_scale, temp)
    elif from_scale == temp_scale.CELCIUS:
        return convert_from_celcius(to_scale, temp)
    elif from_scale == temp_scale.KELVIN:
        return convert_from_kelvin(to_scale, temp)
    elif from_scale == temp_scale.RANKINE:
        return convert_from_rankine(to_scale, temp)
    else:
        return 0.0
