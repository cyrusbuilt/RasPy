"""This module contains the MCPTerminalConfig type."""


from raspy.components.potentiometers.microchip import microchip_pot_channel


class MCPTerminalConfiguration(object):
    """Terminal configuration settings for the channel."""

    def __init__(self, chan=microchip_pot_channel.NONE,
                 chan_enabled=False, pin_a_enabled=False,
                 pin_w_enabled=False, pin_b_enabled=False):
        """Initialize a new instance of MCPTerminalConfiguration.

        :param int chan: The channel this terminal configuration represents.
        :param bool chan_enabled: Set True to enable the channel.
        :param bool pin_a_enabled: Set True to enable pin A.
        :param bool pin_w_enabled: Set True to enable pin W.
        :param bool pin_b_enabled: Set True to enable pin B.
        """
        self.__channel = chan
        self.__channelEnabled = chan_enabled
        self.__pinAEnabled = pin_a_enabled
        self.__pinWEnabled = pin_w_enabled
        self.__pinBEnabled = pin_b_enabled

    @property
    def channel(self):
        """Get the channel.

        :returns: The channel.
        :rtype: int
        """
        return self.__channel

    @property
    def is_channel_enabled(self):
        """Get whether or not the channel is enabled.

        :returns: True if the channel is enabled.
        :rtype: bool
        """
        return self.__channelEnabled

    @property
    def is_pin_a_enabled(self):
        """Get whether or not pin A is enabled.

        :returns: True if pin A is enabled.
        :rtype: bool
        """
        return self.__pinAEnabled

    @property
    def is_pin_w_enabled(self):
        """Get whether or not pin W is enabled.

        :returns: True if pin W is enabled.
        :rtype: bool
        """
        return self.__pinWEnabled

    @property
    def is_pin_b_enabled(self):
        """Get whether or not pin B is enabled.

        :returns: True if pin B is enabled.
        :rtype: bool
        """
        return self.__pinBEnabled
