"""This module contains the DeviceControllerStatus type."""


class DeviceControllerStatus(object):
    """The device's status."""

    def __init__(self, write_active=False, write_prot=False,
                 chan_a_lock=False, chan_b_lock=False):
        """Initialize a new instance of DeviceControllerStatus.

        :param bool write_active: Set True if actively writing to EEPROM.
        :param bool write_prot: Set True if the EEPROM is write-protected.
        :param bool chan_a_lock: Set True if channel A is locked.
        :param bool chan_b_lock: Set True if channel B is locked.
        """
        self.__writeActive = write_active
        self.__writeProtected = write_prot
        self.__channelALocked = chan_a_lock
        self.__channelBLocked = chan_b_lock

    @property
    def eeprom_write_active(self):
        """Get a value indicating whether the EEPROM is actively writing.

        :returns: True if the EEPROM is actively writing.
        :rtype: bool
        """
        return self.__writeActive

    @property
    def eeprom_write_protected(self):
        """Get a value indicating whether the EEPROM is write-protected.

        :returns: True if the EEPROM is write-protected.
        :rtype: bool
        """
        return self.__writeProtected

    @property
    def channel_a_locked(self):
        """Get whether or not channel A is locked.

        :returns: True if channel A is locked.
        :rtype: bool
        """
        return self.__channelALocked

    @property
    def channel_b_locked(self):
        """Get whether or not channel B is locked.

        :returns: True if channel B is locked.
        :rtype: bool
        """
        return self.__channelBLocked
