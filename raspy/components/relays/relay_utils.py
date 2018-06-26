"""Relay utility methods."""


from raspy.components.relays import relay_state


def get_inverse_state(state):
    """Get the inverse of the specified state.

    :param int state: The relay state to invert.
    :returns: The inverse of the specified state.
    :rtype: int
    """
    if state == relay_state.OPEN:
        return relay_state.CLOSED
    return relay_state.OPEN
