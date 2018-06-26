"""This module provides utility methods for working with power components."""


from raspy.components.power import power_state


def get_power_state_name(state):
    """Get the name of the specified power state.

    :param int state: The state to get the name of.
    :returns: The name of the state or an empty string if invalid or empty.
    :rtype: str
    """
    if state is None or not type(state) == int:
        return ""

    name = ""
    if state == power_state.ON:
        name = "On"
    elif state == power_state.OFF:
        name = "Off"
    elif state == power_state.UNKNOWN:
        name = "Unknown"
    else:
        pass

    return name
