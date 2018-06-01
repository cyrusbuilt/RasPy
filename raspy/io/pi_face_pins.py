"""PiFace I/O pins."""


class PiFacePin:
    """Base type for all PiFace Pins."""

    def __init__(self):
        """ctor."""
        pass

    value = -1
    name = ""


class Output00(PiFacePin):
    """Output pin 1 (relay 1)."""

    def __init__(self):
        """ctor."""
        PiFacePin.__init__(self)

    value = 1
    name = "Output 1 (RELAY 1)"


class Output01(PiFacePin):
    """Output pin 2 (RELAY 2)."""

    def __init__(self):
        """ctor."""
        PiFacePin.__init__(self)

    value = 2
    name = "Output 2 (RELAY 2)"


class Output02(PiFacePin):
    """Output pin 3."""

    def __init__(self):
        """ctor."""
        PiFacePin.__init__(self)

    value = 4
    name = "Output 3"


class Output03(PiFacePin):
    """Output pin 4."""

    def __init__(self):
        """ctor."""
        PiFacePin.__init__(self)

    value = 8
    name = "Output 4"


class Output04(PiFacePin):
    """Output pin 5."""

    def __init__(self):
        """ctor."""
        PiFacePin.__init__(self)

    value = 16
    name = "Output 5"


class Output05(PiFacePin):
    """Output pin 6."""

    def __init__(self):
        """ctor."""
        PiFacePin.__init__(self)

    value = 32
    name = "Output 6"


class Output06(PiFacePin):
    """Output pin 7."""

    def __init__(self):
        """ctor."""
        PiFacePin.__init__(self)

    value = 64
    name = "Output 7"


class Output07(PiFacePin):
    """Output pin 8."""

    def __init__(self):
        """ctor."""
        PiFacePin.__init__(self)

    value = 128
    name = "Output 8"


class Input00(PiFacePin):
    """Input pin 1 (switch 1)."""

    def __init__(self):
        """ctor."""
        PiFacePin.__init__(self)

    value = 1001
    name = "Input 1 (SWITCH 1)"


class Input01(PiFacePin):
    """Input pin 2 (switch 2)."""

    def __init__(self):
        """ctor."""
        PiFacePin.__init__(self)

    value = 1002
    name = "Input 2 (SWITCH 2)"


class Input02(PiFacePin):
    """Input pin 3 (switch 3)."""

    def __init__(self):
        """ctor."""
        PiFacePin.__init__(self)

    value = 1004
    name = "Input 3 (SWITCH 3)"


class Input03(PiFacePin):
    """Input pin 4 (switch 4)."""

    def __init__(self):
        """ctor."""
        PiFacePin.__init__(self)

    value = 1008
    name = "Input 4 (SWITCH 4)"


class Input04(PiFacePin):
    """Input pin 5."""

    def __init__(self):
        """ctor."""
        PiFacePin.__init__(self)

    value = 1016
    name = "Input 5"


class Input05(PiFacePin):
    """Input pin 6."""

    def __init__(self):
        """ctor."""
        PiFacePin.__init__(self)

    value = 1032
    name = "Input 6"


class Input06(PiFacePin):
    """Input pin 7."""

    def __init__(self):
        """ctor."""
        PiFacePin.__init__(self)

    value = 1064
    name = "Input 7"


class Input07(PiFacePin):
    """Input pin 8."""

    def __init__(self):
        """ctor."""
        PiFacePin.__init__(self)

    value = 1128
    name = "Input 8"


class NonePin(PiFacePin):
    """No pin assignment."""

    def __init__(self):
        """ctor."""
        PiFacePin.__init__(self)

    value = 0
    name = "NonePin"
