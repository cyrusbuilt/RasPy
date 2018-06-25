"""This module contains the MicrochipPotentiometer base type."""


from pyee import EventEmitter
from raspy.argument_null_exception import ArgumentNullException
from raspy.illegal_argument_exception import IllegalArgumentException
from raspy.invalid_operation_exception import InvalidOperationException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.potentiometers.potentiometer import Potentiometer
from raspy.components.potentiometers.microchip import device_control_channel
from raspy.components.potentiometers.microchip.device_controller_term_config \
    import DeviceControllerTermConfig
from raspy.components.potentiometers.microchip import mcp_device_controller
from raspy.components.potentiometers.microchip.microchip_pot_dev_status import MicrochipPotDevStatus
from raspy.components.potentiometers.microchip.mcp_terminal_config import MCPTerminalConfiguration
from raspy.components.potentiometers.microchip import microchip_pot_channel
from raspy.components.potentiometers.microchip import microchip_pot_non_volatile_mode


EVENT_WIPER_ACTION = "wiperActionEvent"
PIN_NOT_AVAILABLE = True
INITIAL_VAL_LOADED_FROM_EEPROM = 0


class WiperEvent(object):
    """Wiper event info class."""

    def __init__(self, channel=None, controller=None, val=0):
        """Initialize a new instance of WiperEvent.

        :param DeviceControlChannel channel: The control channel for the wiper.
        :param MCPDeviceController controller: The device controller.
        :param int val: The device reading value.
        """
        self.__chan = channel
        self.__ctlr = controller
        self.__value = val

    def set_channel_value(self, non_vol=False):
        """Set the channel value.

        :param bool non_vol: Set True if setting the channel value of a
        non-volatile wiper, or False for a volatile wiper.
        """
        self.__ctlr.set_value(self.__chan, self.__value, non_vol)


class MicrochipPotentiometer(Potentiometer):
    """An MCP45XX or MCP46XX IC device abstraction base type."""

    def __init__(self, device=None, pin_a0=False, pin_a1=False, pin_a2=False,
                 channel=microchip_pot_channel.NONE,
                 non_vol_mode=microchip_pot_non_volatile_mode.VOLATILE_AND_NON_VOLATILE,
                 init_non_vol_wiper_val=0):
        """Initialize a new instance of MicrochipPotentiometer.

        :param raspy.io.i2c.i2c_interface.I2CInterface device: The I2C bus
        device this instance is connected to.
        :param bool pin_a0: Set True if device's address pin A0 is high.
        :param bool pin_a1: Set True if device's address pin A1 is high.
        :param bool pin_a2: Set True if device's address pin A2 is high.
        :param int channel: The potentiometer channel.
        :param int non_vol_mode: The non-volatility mode.
        :param int init_non_vol_wiper_val: The initial value to set.
        :raises: raspy.argument_null_exception.ArgumentNullException if
        'device' param is None.
        :raises: raspy.illegal_argument_exception.IllegalArgumentException if
        the specified channel is not supported by the device.
        :raises: raspy.io.io_exception.IOException if unable to open the
        I2C bus.
        """
        Potentiometer.__init__(self)
        if device is None:
            msg = "Param 'device' cannot be None."
            raise ArgumentNullException(msg)

        if not self.is_channel_supported(channel):
            msg = "Specified channel not supported by device."
            raise IllegalArgumentException(msg)

        self.__emitter = EventEmitter()
        self.__channel = channel
        self.__currentValue = 0
        self.__nonVolMode = non_vol_mode
        device_addr = MicrochipPotentiometer._build_i2c_address(pin_a0, pin_a1, pin_a2)
        self.__controller = mcp_device_controller.MCPDeviceController(device, device_addr)
        self.__emitter.on(EVENT_WIPER_ACTION,
                          lambda wiper_evt: self._on_wiper_action_event(wiper_evt))
        self._initialize(init_non_vol_wiper_val)

    @staticmethod
    def _build_i2c_address(pin_a0=False, pin_a1=False, pin_a2=False):
        """Build the I2C bus address of the device based on which pins are set.

        :param bool pin_a0: Set True if the device's address pinA0 is high.
        :param bool pin_a1: Set True if the device's address pinA1 is high.
        :param bool pin_a2: Set True if the device's address pinA2 is high.
        :returns: The I2C address based on address pins given.
        :rtype: int
        """
        # Constant component.
        i2c_addr = 0x0101000

        # Dynamic component if device knows A0.
        if pin_a0:
            i2c_addr |= 0x0000001

        # Dynamic component if device knows A1.
        if pin_a1:
            i2c_addr |= 0x0000010

        # Dynamic component if device knows A2.
        if pin_a2:
            i2c_addr |= 0x0000100
        return i2c_addr

    def _get_value_according_boundaries(self, val=0):
        """Adjust the given value according to the boundaries (0 and max_val).

        :param int val: The wiper's value to be set.
        :returns: A valid wiper value.
        :rtype: int
        """
        if val is None or not type(val) == int or val < 0:
            val = 0
            new_val = val
        elif val > self.max_value:
            new_val = self.max_value
        else:
            new_val = val
        return new_val

    def _initialize(self, init_val):
        """Initialize the wiper to a defined status.

        For devices capable of non-volatile wipers, the non-volatile value is
        loaded. For devices not capable, the given value is set in the device.

        :param int init_val: The initial value for devices not capable of
        non-volatile wipers.
        :raises: raspy.io.io_exception.IOException if communication with the
        device failed or a malformed result.
        """
        chan = device_control_channel.value_of(self.__channel)
        if self.is_non_volatile_wiper_capable:
            self.__currentValue = self.__controller.get_value(chan, True)
        else:
            new_init_val = self._get_value_according_boundaries(init_val)
            vol = mcp_device_controller.VOLATILE_WIPER
            self.__controller.set_value(chan, new_init_val, vol)
            self.__currentValue = new_init_val

    def _on_wiper_action_event(self, wiper_evt=None):
        """Handle the internal EVENT_WIPER_ACTION.

        :param WiperEvent wiper_evt: The event info.
        """
        # Do nothing if no event specified.
        if wiper_evt is None:
            return

        # For volatile wiper.
        if (self.__nonVolMode == microchip_pot_non_volatile_mode.VOLATILE_ONLY or
                self.__nonVolMode == microchip_pot_non_volatile_mode.VOLATILE_AND_NON_VOLATILE):
            wiper_evt.set_channel_value(mcp_device_controller.VOLATILE_WIPER)

        # For non-volatile wiper.
        if (self.__nonVolMode == microchip_pot_non_volatile_mode.NON_VOLATILE_ONLY or
                self.__nonVolMode == microchip_pot_non_volatile_mode.VOLATILE_AND_NON_VOLATILE):
            wiper_evt.set_channel_value(mcp_device_controller.NON_VOLATILE_WIPER)

    def on(self, evt, callback):
        """Register an event with a callback to handle it.

        :param str evt: The name of the event to register a handler for.
        :param function callback: The callback to execute when the event
        fires.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance is disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("MicrochipPotentiometer")

        self.__emitter.on(evt, callback)

    def emit(self, evt, args):
        """Emit the specified event to all registered listeners.

        :param str evt: The name of the event to emit.
        :param object args: The arguments to pass to the event handlers
        (listeners).
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance is disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("MicrochipPotentiometer")

        self.__emitter.emit(evt, args)

    def remove_all_listeners(self):
        """Remove all registered event listeners."""
        if self.is_disposed:
            return

        if self.__emitter is not None:
            self.__emitter.remove_all_listeners()

    def dispose(self):
        """Dispose managed resources."""
        if self.is_disposed:
            return

        if self.__controller is not None:
            self.__controller.dispose()
            self.__controller = None

        self.__emitter.remove_all_listeners()
        self.__emitter = None
        self.__currentValue = -1
        self.__nonVolMode = microchip_pot_non_volatile_mode.VOLATILE_AND_NON_VOLATILE
        Potentiometer.dispose(self)

    def _fire_wiper_action_event(self, wiper_evt):
        """Fire the EVENT_WIPER_ACTION event.

        :param WiperEvent wiper_evt: The event info.
        """
        if self.is_disposed:
            raise ObjectDisposedException("MicrochipPotentiometer")
        self.emit(EVENT_WIPER_ACTION, wiper_evt)

    @property
    def current_value(self):
        """Get the wiper's current value.

        :returns: The current value. Values from 0 to max_value are valid.
        Values above or below these boundaries should be corrected quietly.
        :rtype: int
        """
        return self.__currentValue

    @current_value.setter
    def current_value(self, value):
        """Set the wiper's current value.

        :param int value: The wiper value to set.
        """
        # Check bounds.
        new_val = self._get_value_according_boundaries(value)

        # Set wipers according to mode.
        chan = device_control_channel.value_of(self.channel)
        evt = WiperEvent(chan, self.__controller, new_val)
        self._fire_wiper_action_event(evt)

        # Set value only if volatile wiper is affected.
        if self.__nonVolMode == microchip_pot_non_volatile_mode.NON_VOLATILE_ONLY:
            return
        self.__currentValue = new_val

    @property
    def channel(self):
        """Get the channel this device is configured for.

        :returns: The device channel.
        :rtype: int
        """
        return microchip_pot_channel.NONE

    @property
    def is_non_volatile_wiper_capable(self):
        """Get whether or not this device is capable of non-volatile wipers.

        :returns: True if the device is capable of non-volatile wipers.
        :rtype: bool
        """
        return False

    @property
    def non_volatile_mode(self):
        """Get the way non-volatile reads and/or writes are done.

        :returns: The non-volatile mode.
        :rtype: int
        """
        return microchip_pot_non_volatile_mode.VOLATILE_AND_NON_VOLATILE

    @property
    def supported_channels(self):
        """Get the channels that are suppored by the underlying device.

        :returns: A list of `raspy.components.potentiometers.microchip.MicrochipPotChannel`
        that represent the supported channels by the underlying device.
        :rtype: list
        """
        return list()

    @property
    def device_status(self):
        """Get the device and wiper status.

        :returns: The device status.
        :rtype: raspy.components.potentiometers.microchip.MicrochipPotDeviceStatus.
        :raises: raspy.io.io_exception.IOException if communication with the
        device fails.
        """
        dev_stat = self.__controller.device_status
        wipe_lock_act = dev_stat.channel_b_locked
        if self.__channel == microchip_pot_channel.A:
            wipe_lock_act = dev_stat.channel_a_locked
        write_act = dev_stat.eeprom_write_active
        write_prot = dev_stat.eeprom_write_protected
        return MicrochipPotDevStatus(self.__channel, write_act, write_prot, wipe_lock_act)

    @property
    def terminal_configuration(self):
        """Get the current terminal configuration.

        :returns: The terminal configuration.
        :rtype: raspy.components.potentiometers.microchip.MCPTerminalConfiguration
        :raises: raspy.io.io_exception.IOException if communication with
        the device fails.
        """
        chan = device_control_channel.value_of(self.__channel)
        tcon = self.__controller.get_terminal_config(chan)
        chan_enable = tcon.channel_enabled
        pin_a = tcon.pin_a_enabled
        pin_w = tcon.pin_w_enabled
        pin_b = tcon.pin_b_enabled
        return MCPTerminalConfiguration(self.__channel, chan_enable, pin_a, pin_w, pin_b)

    @terminal_configuration.setter
    def terminal_configuration(self, config):
        """Set the terminal configuration.

        :param MCPTerminalConfiguration config:
        The terminal configuration.
        :raises: raspy.io.io_exception.IOException if communication with
        the device fails.
        """
        if config is None:
            raise ArgumentNullException("config value cannot be None.")

        if config.channel != self.__channel:
            msg = "Setting a configuration with a channel that is not the "
            msg += "potentiometer's channel is not supported."
            raise IllegalArgumentException(msg)

        chan = device_control_channel.value_of(self.__channel)
        chan_enable = config.is_channel_enabled
        pin_a = config.is_pin_a_enabled
        pin_w = config.is_pin_w_enabled
        pin_b = config.is_pin_b_enabled
        dev_con = DeviceControllerTermConfig(chan, chan_enable, pin_a, pin_w, pin_b)
        self.__controller.set_terminal_config(dev_con)

    def _set_non_volatile_mode(self, mode):
        """Set the non-volatility mode.

        :param int mode: The way non-volatile reads or writes are done.
        :raises: raspy.invalid_operation_exception.InvalidOperationException if
        this device is not capable of non-volatile wipers.
        """
        vol_only = microchip_pot_non_volatile_mode.VOLATILE_ONLY
        if (not self.is_non_volatile_wiper_capable and
                self.__nonVolMode != vol_only):
            msg = "This device is not capable of non-volatile wipers."
            msg += "You *must* use microchip_pot_non_volatile_mode.VOLATILE_ONLY"
            raise InvalidOperationException(msg)
        self.__nonVolMode = mode

    def _get_non_volatile_value(self):
        """Get the non-volatile wiper's value.

        :returns: The non-volatile wiper's value.
        :rtype: int
        :raises: raspy.invalid_operation_exception.InvalidOperationException if
        this device is not capable of non-volatile wipers.
        """
        if self.is_non_volatile_wiper_capable:
            msg = "This device is not capable of non-volatile wipers."
            raise InvalidOperationException(msg)
        chan = device_control_channel.value_of(self.__channel)
        return self.__controller.get_value(chan, True)

    def update_cache_from_device(self):
        """Update the cache from the wiper's value.

        :returns: The wiper's current value.
        :rtype: int
        :raises: raspy.io.io_exception.IOException if communication with
        the device fails.
        """
        chan = device_control_channel.value_of(self.__channel)
        self.__currentValue = self.__controller.get_value(chan, False)
        return self.__currentValue

    def is_channel_supported(self, channel):
        """Get whether or not the specified channel is supported by the device.

        :param int channel: The channel to check.
        :returns: True if the channel is supported.
        :rtype: bool
        """
        supported = False
        for chan in self.supported_channels:
            if chan == channel:
                supported = True
                break
        return supported

    def decrease(self, steps=0):
        """Decrease the wiper's value by the specified number of steps.

        It is not an error if the wiper hits or already hit the lower
        boundary (0). In such situations, the wiper sticks to the lower
        boundary or doesn't change.

        :param int steps: The number of steps to decrease by. If not
        specified or zero, then defaults to 1.
        :raises: raspy.io.io_exception.IOException if communication with the
        device failed.
        """
        if self.__currentValue == 0:
            return

        if steps < 0:
            msg = "Only positive integer values are permitted."
            raise IllegalArgumentException(msg)

        if self.non_volatile_mode != microchip_pot_non_volatile_mode.VOLATILE_ONLY:
            msg = "Decrease is only permitted on volatile-only wipers."
            raise InvalidOperationException(msg)

        # Check bounds:
        actual_steps = steps
        if steps > self.__currentValue:
            actual_steps = self.__currentValue

        new_val = self.__currentValue - actual_steps
        if new_val == 0 or steps > 5:
            self.__currentValue = new_val
        else:
            chan = device_control_channel.value_of(self.__channel)
            self.__controller.decrease(chan, actual_steps)
            self.__currentValue = new_val

    def increase(self, steps=0):
        """Increase the wiper's value bye the specified number of steps.

        It is not an error if the wiper hits or already hit the upper
        boundary. In such situations, the wiper sticks to the upper boundary
        or doesn't change.
        :param int steps: How many steps to increase. If not specified or
        zero, then defaults to 1. If the current value is equal to the max
        value, then nothing happens. If steps is less than zero, then an
        exception is thrown.
        :raises: raspy.io.io_exception.IOException if communication with the
        device failed.
        """
        max_val = self.max_value
        if self.__currentValue == max_val:
            return

        if steps < 0:
            msg = "Only positive integer values are permitted."
            raise IllegalArgumentException(msg)

        vol_only = microchip_pot_non_volatile_mode.VOLATILE_ONLY
        if self.non_volatile_mode != vol_only:
            msg = "Increase is only permitted for volatile-only wipers."
            raise InvalidOperationException(msg)

        # Check bounds.
        actual_steps = steps
        if (steps + self.__currentValue) > max_val:
            actual_steps = max_val - self.__currentValue

        new_val = self.__currentValue + actual_steps
        if new_val == max_val or steps > 5:
            self.__currentValue = new_val
        else:
            chan = device_control_channel.value_of(self.__channel)
            self.__controller.increase(chan, actual_steps)
            self.__currentValue = new_val

    def set_wiper_lock(self, enabled=False):
        """Enable or disable the wiper lock.

        :param bool enabled: Set True to enable the wiper lock.
        :raises: raspy.io.io_exception.IOException if communication with
        the device fails.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("MicrochipPotentiometer")
        chan = device_control_channel.value_of(self.__channel)
        self.__controller.set_wiper_lock(chan, enabled)

    def set_write_protection(self, enabled=False):
        """Enable or disable write protection for devices with non-vol memory.

        Enabling write-protection does not only protect non-volatile wipers,
        it also protects any other non-volatile information stored (ie.
        wiper-locks).

        :param bool enabled: Set True to enable.
        :raises: raspy.io.io_exception.IOException if communication with
        the device fails.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("MicrochipPotentiometer")
        self.__controller.set_write_protection(enabled)
