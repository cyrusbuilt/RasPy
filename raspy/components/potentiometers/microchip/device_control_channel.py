"""This module contains the DeviceControlChannel type."""


from raspy import string_utils
from raspy.components.potentiometers.microchip import microchip_pot_channel
from raspy.components.potentiometers.microchip import register_memory_address
from raspy.components.potentiometers.microchip import terminal_control_register_bit


class DeviceControlChannel(object):
    """Represents the wiper. Used for devices knowing multiple wipers."""

    def __init__(self, vol_mem_addr=register_memory_address.NONE,
                 non_vol_mem_addr=register_memory_address.NONE,
                 term_con_addr=register_memory_address.NONE,
                 hw_config_ctrl_bit=terminal_control_register_bit.NONE,
                 term_a_conn_ctrl_bit=terminal_control_register_bit.NONE,
                 term_b_conn_ctrl_bit=terminal_control_register_bit.NONE,
                 wiper_conn_ctrl_bit=terminal_control_register_bit.NONE,
                 chan=microchip_pot_channel.NONE):
        """Initialize a new instance of DeviceControlChannel.

        :param int vol_mem_addr: The volatile memory address.
        :param int non_vol_mem_addr: The non-volatile memory address.
        :param int term_con_addr: The terminal control address.
        :param int hw_config_ctrl_bit: The hardware config control bit.
        :param int term_a_conn_ctrl_bit: The terminal A connection control bit.
        :param int term_b_conn_ctrl_bit: The terminal B connection control bit.
        :param int wiper_conn_ctrl_bit: The wiper connection control bit.
        :param int chan: The MCP potentiometer channel.
        """
        self.__volMemAddr = vol_mem_addr
        self.__nonVolMemAddr = non_vol_mem_addr
        self.__termConAddr = term_con_addr
        self.__hwConfigCtrlBit = hw_config_ctrl_bit
        self.__termAConnCtrlBit = term_a_conn_ctrl_bit
        self.__termBConnCtrlBit = term_b_conn_ctrl_bit
        self.__wiperConnCtrlBit = wiper_conn_ctrl_bit
        self.__chan = chan

    @property
    def volatile_mem_address(self):
        """Get the volatile memory address.

        :returns: The volatile memory address.
        :rtype: int
        """
        return self.__volMemAddr

    @property
    def non_volatile_mem_address(self):
        """Get the non-volatile memory address.

        :returns: The non-volatile memory address.
        :rtype: int
        """
        return self.__nonVolMemAddr

    @property
    def term_control_address(self):
        """Get the terminal control address.

        :returns: The terminal control address.
        :rtype: int
        """
        return self.__termConAddr

    @property
    def hardware_config_ctrl_bit(self):
        """Get the hardware config control bit.

        :returns: The hardware config control bit.
        :rtype: int
        """
        return self.__hwConfigCtrlBit

    @property
    def term_a_connection_ctrl_bit(self):
        """Get the terminal A connection control bit.

        :returns: The terminal A connection control bit.
        :rtype: int
        """
        return self.__termAConnCtrlBit

    @property
    def term_b_connection_ctrl_bit(self):
        """Get the terminal B connection control bit.

        :returns: The terminal B connection control bit.
        :rtype: int
        """
        return self.__termBConnCtrlBit

    @property
    def wiper_connection_ctrl_bit(self):
        """Get the wiper connection control bit.

        :returns: The wiper connection control bit.
        :rtype: int
        """
        return self.__wiperConnCtrlBit

    @property
    def channel(self):
        """Get the channel.

        :returns: The channel.
        :rtype: int
        """
        return self.__chan

    @property
    def name(self):
        """Get the name.

        :returns: The name. If no channel specified, then an empty string.
        :rtype: str
        """
        if self.__chan is None or self.__chan == microchip_pot_channel.NONE:
            return string_utils.EMPTY

        if self.__chan == microchip_pot_channel.A:
            return "A"
        elif self.__chan == microchip_pot_channel.B:
            return "B"
        elif self.__chan == microchip_pot_channel.C:
            return "C"
        elif self.__chan == microchip_pot_channel.D:
            return "D"
        else:
            return string_utils.EMPTY


A = DeviceControlChannel(register_memory_address.WIPER0,
                         register_memory_address.WIPER0_NV,
                         register_memory_address.TCON01,
                         terminal_control_register_bit.TCON_RH02HW,
                         terminal_control_register_bit.TCON_RH02A,
                         terminal_control_register_bit.TCON_RH02B,
                         terminal_control_register_bit.TCON_RH02W,
                         microchip_pot_channel.A)
"""Device control channel A."""

B = DeviceControlChannel(register_memory_address.WIPER1,
                         register_memory_address.WIPER1_NV,
                         register_memory_address.TCON01,
                         terminal_control_register_bit.TCON_RH13HW,
                         terminal_control_register_bit.TCON_RH13A,
                         terminal_control_register_bit.TCON_RH13B,
                         terminal_control_register_bit.TCON_RH13W,
                         microchip_pot_channel.B)
"""Device control channel B."""

C = DeviceControlChannel(register_memory_address.WIPER2,
                         register_memory_address.WIPER2_NV,
                         register_memory_address.TCON23,
                         terminal_control_register_bit.TCON_RH02HW,
                         terminal_control_register_bit.TCON_RH02A,
                         terminal_control_register_bit.TCON_RH02B,
                         terminal_control_register_bit.TCON_RH02W,
                         microchip_pot_channel.C)
"""Device control channel C."""

D = DeviceControlChannel(register_memory_address.WIPER3,
                         register_memory_address.WIPER3_NV,
                         register_memory_address.TCON23,
                         terminal_control_register_bit.TCON_RH13HW,
                         terminal_control_register_bit.TCON_RH13A,
                         terminal_control_register_bit.TCON_RH13B,
                         terminal_control_register_bit.TCON_RH13W,
                         microchip_pot_channel.D)
"""Device control channel D."""

ALL = (A, B, C, D)
"""All device control channels."""


def value_of(channel):
    """Factory method for creating a device control channel.

    :param int channel: The MCP potentiometer channel.
    :returns: A new instance of DeviceControlChannel. If no channel was
    specified of is invalid, then returns None.
    :rtype: raspy.components.potentiometers.microchip.device_control_channel.DeviceControlChannel
    """
    if (channel is None or
            type(channel) is not int or
            channel == microchip_pot_channel.NONE):
        return None

    chan_name = string_utils.EMPTY
    if channel == microchip_pot_channel.A:
        chan_name = "A"
    elif channel == microchip_pot_channel.B:
        chan_name = "B"
    elif channel == microchip_pot_channel.C:
        chan_name = "C"
    elif channel == microchip_pot_channel.D:
        chan_name = "D"
    else:
        pass

    result = None
    for dc in ALL:
        if dc.name == chan_name:
            result = dc
            break

    return result
