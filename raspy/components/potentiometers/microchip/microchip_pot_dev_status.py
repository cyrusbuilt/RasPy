"""This module contains the MicroChipPotDevStatus type."""


from raspy.components.potentiometers.microchip import microchip_pot_channel


class MicrochipPotDevStatus(object):
    """The device status concerning the channel."""

    def __init__(self, chan=microchip_pot_channel.NONE, write_active=False,
                 write_prot=False, wiper_locked=False):
        """Initialize a new instance of MicrochipPotDevStatus.

        :param int chan: The wiper-lock channel.
        :param bool write_active: Set True if currently writing to the EEPROM.
        :param bool write_prot: Set True if the EEPROM is write-protected.
        :param bool wiper_locked: Set True if the wiper is locked.
        """
        self.__wipe_lock_channel = chan
        self.__write_active = write_active
        self.__write_protected = write_prot
        self.__wiper_locked = wiper_locked

    @property
    def is_eeprom_write_active(self):
        """Get whether or not the device is writing to EEPROM.

        :returns: True if the device is writing to EEPROM.
        :rtype: bool
        """
        return self.__write_active

    @property
    def is_eeprom_write_protected(self):
        """Get whether or not the EEPROM is write-protected.

        :returns: True if the EEPROM is write-protected.
        :rtype: bool
        """
        return self.__write_protected

    @property
    def wiper_lock_channel(self):
        """Get the channel the wiper-lock-active status is for.

        :returns: The wiper lock channel.
        :rtype: int
        """
        return self.__wipe_lock_channel

    @property
    def is_wiper_lock_active(self):
        """Get whether or not the wiper's lock is active.

        :returns: True if the wiper lock is active.
        :rtype: bool
        """
        return self.__wiper_locked
