"""This module contains the DeviceControllerTermConfig type."""


from raspy.illegal_argument_exception import IllegalArgumentException
from raspy.components.potentiometers.microchip import device_control_channel


class DeviceControllerTermConfig(object):
    """The device's terminal configuration for a certain channel."""

    def __init__(self, dcc=None, chan_enabled=False, pin_a_enabled=False,
                 pin_w_enabled=False, pin_b_enabled=False):
        """Initialize a new instance of DeviceControllerTermConfig.

        :param device_control_channel.DeviceControlChannel dcc: The device
        control channel.
        :param bool chan_enabled: Set True to enable the channel.
        :param bool pin_a_enabled: Set True to enable pin A.
        :param bool pin_w_enabled: Set True to enable pin W.
        :param bool pin_b_enabled: Set True to enable pin B.
        :raises: raspy.illegal_argument_exception.IllegalArgumentException if
        param dcc is not an instance of DeviceControlChannel.
        """
        instance = isinstance(dcc, device_control_channel.DeviceControlChannel)
        if dcc is not None and not instance:
            msg = "'dcc' param must be object of type DeviceControlChannel"
            raise IllegalArgumentException(msg)
        self.__channel = dcc
        self.__channelEnabled = chan_enabled
        self.__pinAEnabled = pin_a_enabled
        self.__pinWEnabled = pin_w_enabled
        self.__pinBEnabled = pin_b_enabled

    @property
    def channel(self):
        """Get the channel.

        :returns: The channel.
        :rtype: device_control_channel.DeviceControlChannel
        """
        return self.__channel

    @property
    def channel_enabled(self):
        """Get whether or not the channel is enabled.

        :returns: True if the channel is enabled.
        :rtype: bool
        """
        return self.__channelEnabled

    @property
    def pin_a_enabled(self):
        """Get whether or not pin A is enabled.

        :returns: True if pin A is enabled.
        :rtype: bool
        """
        return self.__pinAEnabled

    @property
    def pin_w_enabled(self):
        """Get whether or not pin W is enabled.

        :returns: True if pin W is enabled.
        :type: bool
        """
        return self.__pinWEnabled

    @property
    def pin_b_enabled(self):
        """Get whether or not pin B is enabled.

        :returns: True if pin B is enabled.
        :rtype: bool
        """
        return self.__pinBEnabled
