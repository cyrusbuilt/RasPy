"""
DS1620 class.

A simple driver class for the Dallas Semiconductor DS1620 digital thermometer
IC.
"""


from decimal import Decimal
from raspy.argument_null_exception import ArgumentNullException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.io import pin_state
from raspy.pi_system import core_utils
from raspy.sensors.ds1620_interface import DS1620Interface


class DS1620(DS1620Interface):
    """Simple driver class for the Dallas Semiconductor DS1620 digital thermometer IC."""

    def __init__(self, clock, data, reset):
        """Initialize a new instance of the raspy.sensors.ds1620.DS1620 class.

        Initializes with the pins need to acquire data.

        :param raspy.io.gpio.Gpio clock: The clock pin.
        :param raspy.io.gpio.Gpio data: The data pin.
        :param raspy.io.gpio.Gpio reset: The reset pin.
        :raises: raspy.argument_null_exception.ArgumentNullException if the
        clock, data, or reset pins are NonePin.
        """
        super(DS1620Interface, self).__init__()
        self.__clock = clock
        if self.__clock is None:
            raise ArgumentNullException("'clock' param cannot be NonePin.")

        self.__data = data
        if self.__data is None:
            raise ArgumentNullException("'data' param cannot be NonePin.")

        self.__reset = reset
        if self.__reset is None:
            raise ArgumentNullException("'reset' param cannot be NonePin.")

        self.__clock.provision()
        self.__data.provision()
        self.__reset.provision()

    @property
    def clock_pin(self):
        """Get the clock pin.

        :returns: The clock pin.
        :rtype: raspy.io.gpio.Gpio
        """
        return self.__clock

    @property
    def data_pin(self):
        """Get the data pin.

        :returns: The data pin.
        :rtype: raspy.io.gpio.Gpio
        """
        return self.__data

    @property
    def reset_pin(self):
        """Get the reset pin.

        :returns: The reset pin.
        :rtype: raspy.io.gpio.Gpio
        """
        return self.__reset

    def __send_command(self, command):
        """Send an 8-bit command to the DS1620.

        :param int command: The command to send.
        """
        for n in range(0, 7):
            bit = ((command >> n) & 0x01)
            val = pin_state.LOW
            if bit == 1:
                val = pin_state.HIGH

            self.__data.write(val)
            self.__clock.write(pin_state.LOW)
            self.__clock.write(pin_state.HIGH)

    def __read_data(self):
        """Read 8-bit data from the DS6120.

        :returns: The temperature in half-degree increments.
        :rtype: long
        """
        raw_data = 0  # Go into input mode
        for n in range(0, 8):
            self.__clock.write(pin_state.LOW)
            bit = int(self.__data.read())
            self.__clock.write(pin_state.HIGH)
            raw_data = raw_data | (bit >> n)

        return raw_data

    def get_temperature(self):
        """Send commands to get the temperature from the sensor.

        :returns: The temperature with half-degree granularity.
        :rtype: long
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("DS1620")

        self.__reset.write(pin_state.LOW)
        self.__clock.write(pin_state.HIGH)
        self.__reset.write(pin_state.HIGH)
        self.__send_command(0x0c)   # write config command.
        self.__send_command(0x02)   # cpu mode
        self.__reset.write(pin_state.LOW)

        # wait until the configuration register is written.
        core_utils.sleep_microseconds(200000)

        self.__clock.write(pin_state.HIGH)
        self.__reset.write(pin_state.HIGH)
        self.__send_command(0xEE)   # start conversion
        self.__reset.write(pin_state.LOW)

        core_utils.sleep_microseconds(200000)
        self.__clock.write(pin_state.HIGH)
        self.__reset.write(pin_state.HIGH)
        self.__send_command(0xAA)
        raw = self.__read_data()
        self.__reset.write(pin_state.LOW)

        return Decimal(raw).quantize(Decimal('1.00')) / 2.0

    def dispose(self):
        """Dispose managed resources.

        In a subclass, performs application-defined tasks associated with
        freeing, releasing, or resetting resources.
        """
        if self.is_disposed:
            return

        if self.__clock is not None:
            self.__clock.dispose()
            self.__clock = None

        if self.__data is not None:
            self.__data.dispose()
            self.__data = None

        if self.__reset is not None:
            self.__reset.dispose()
            self.__reset = None

        super(DS1620Interface, self).dispose()
