"""Pin pull up/down resistance definitions."""


class PinPullResistance:
    """Base type for pin pull resistance values."""

    def __init__(self):
        """ctor."""
        pass

    value = -1
    name = ""


class Off(PinPullResistance):
    """Off. No resistance change."""

    def __init__(self):
        """ctor."""
        PinPullResistance.__init__(self)

    value = 0
    name = "off"


class PullDown(PinPullResistance):
    """Enable pull-down resistor."""

    def __init__(self):
        """ctor."""
        PinPullResistance.__init__(self)

    value = 1
    name = "down"


class PullUp(PinPullResistance):
    """Enable pull-up resistor."""

    def __init__(self):
        """ctor."""
        PinPullResistance.__init__(self)

    value = 2
    name = "up"
