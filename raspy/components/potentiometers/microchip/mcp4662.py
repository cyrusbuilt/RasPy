"""This module contains the MCP4662 type."""


from raspy.components.potentiometers.microchip import microchip_pot_channel
from raspy.components.potentiometers.microchip import microchip_pot_non_volatile_mode as mode
from raspy.components.potentiometers.microchip import microchip_potentiometer as mcp


_SUPPORTED_CHANNELS = [
    microchip_pot_channel.A,
    microchip_pot_channel.B
]


class MCP4662(mcp.MicrochipPotentiometer):
    """Hardware device abstraction component for the Microchip MCP4662."""

    def __init__(self, device=None, pin_a0=False, pin_a1=False,
                 channel=microchip_pot_channel.NONE,
                 non_vol_mode=mode.VOLATILE_AND_NON_VOLATILE):
        """Initialize a new instance of the MCP4662.

        :param raspy.io.i2c.i2c_interface.I2CInterface device: The I2C bus
        device this instance is connected to.
        :param bool pin_a0: Set True if device's address pin A0 is high.
        :param bool pin_a1: Set True if device's address pin A1 is high.
        :param int channel: The potentiometer channel.
        :param int non_vol_mode: The non-volatility mode.
        :raises: raspy.argument_null_exception.ArgumentNullException if
        'device' param is None.
        :raises: raspy.io.io_exception.IOException if unable to open the
        I2C bus.
        """
        mcp.MicrochipPotentiometer.__init__(self, device, pin_a0, pin_a1,
                                            mcp.PIN_NOT_AVAILABLE,
                                            channel, non_vol_mode,
                                            mcp.INITIAL_VAL_LOADED_FROM_EEPROM)

    @property
    def is_non_volatile_wiper_capable(self):
        """Get whether or not this device is capable of non-volatile wipers.

        :returns: True if the device is capable of non-volatile wipers.
        :rtype: bool
        """
        return True

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
        return True

    @property
    def supported_channels(self):
        """Get the channels that are suppored by the underlying device.

        :returns: A list of `raspy.components.potentiometers.microchip.MicrochipPotChannel`
        that represent the supported channels by the underlying device.
        :rtype: list
        """
        return _SUPPORTED_CHANNELS
