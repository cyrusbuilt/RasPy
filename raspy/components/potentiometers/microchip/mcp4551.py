"""This module contains the MCP4551 type."""


from raspy.components.potentiometers.microchip import microchip_pot_channel
from raspy.components.potentiometers.microchip import microchip_pot_non_volatile_mode as mode
from raspy.components.potentiometers.microchip import microchip_potentiometer as mcp


_SUPPORTED_CHANNELS = [
    microchip_pot_channel.A
]


class MCP4551(mcp.MicrochipPotentiometer):
    """Hardware device abstraction component for the Microchip MCP4551."""

    def __init__(self, device=None, pin_a0=False, pin_a1=False, init_val=0):
        """Initialize a new instance of MCP4551.

        :param raspy.io.i2c.i2c_interface.I2CInterface device: The I2C bus
        device this instance is connected to.
        :param bool pin_a0: Set True if device's address pin A0 is high.
        :param bool pin_a1: Set True if device's address pin A1 is high.
        :param int init_val: The initial value to set.
        :raises: raspy.argument_null_exception.ArgumentNullException if
        'device' param is None.
        :raises: raspy.io.io_exception.IOException if unable to open the
        I2C bus.
        """
        mcp.MicrochipPotentiometer.__init__(self, device, pin_a0, pin_a1,
                                            mcp.PIN_NOT_AVAILABLE,
                                            microchip_pot_channel.A,
                                            mode.VOLATILE_ONLY,
                                            init_val)

    @property
    def is_non_volatile_wiper_capable(self):
        """Get whether or not this device is capable of non-volatile wipers.

        :returns: True if the device is capable of non-volatile wipers.
        :rtype: bool
        """
        return False

    @property
    def max_value(self):
        """Get the maximum wiper-value supported by the device.

        :returns: The max wiper value.
        :rtype: int
        """
        return 256

    @property
    def is_rheostat(self):
        """Get whether the device is a potentiometer or rheostat.

        :returns: True if this instance is a rheostat.
        :rtype: bool
        """
        return False

    @property
    def supported_channels(self):
        """Get the channels that are suppored by the underlying device.

        :returns: A list of `raspy.components.potentiometers.microchip.MicrochipPotChannel`
        that represent the supported channels by the underlying device.
        :rtype: list
        """
        return _SUPPORTED_CHANNELS
