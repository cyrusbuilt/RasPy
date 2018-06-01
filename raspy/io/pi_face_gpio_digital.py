"""PiFace GPIO pin implementing SPI."""

import threading
from raspy.invalid_operation_exception import InvalidOperationException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.io import pin_state
from raspy.io import pin_mode
from raspy.io import pin_pull_resistance
from raspy.io.io_exception import IOException
from raspy.io.pi_face_gpio import PiFaceGPIO
from raspy.io.pin_state_change_event import PinStateChangeEvent

try:
    from spidev import SpiDev
except ImportError:
    msg = "WARNING: spidev not installed or could not be imported "
    msg += "(possibly not running on a Raspberry Pi (Linux) host?\n"
    msg += "WARNING: Using mock SpiDev instead."
    print(msg)

    class SpiDev(object):
        """A mock SpiDev class to use when not found (ie. unit tests)."""

        __dev = None
        __bus = None
        __speed = None
        __maxSpeed = 0
        __buf = list()

        def __init__(self):
            """Constructor."""
            pass

        def open(self, dev, bus):
            """Open the SPI bus connection.

            :param int dev: The device ID.
            :param int bus: The bus ID.
            """
            self.__dev = dev
            self.__bus = bus

        def writebytes(self, buf):
            """Write a buffer of values to the bus.

            :param list buf: The buffer to write.
            """
            self.__buf = buf

        def xfer(self, buf, speed):
            """Transfer a buffer of values and read the result.

            :param list buf: The buffer to send.
            :param int speed: The transfer speed.
            :returns: The result buffer.
            :rtype: tuple
            """
            self.__buf = buf
            self.__speed = speed
            ret_tup = ()
            for i in range(0, len(self.__buf)):
                lst = list()
                lst.append(self.__buf[i])
                new_tup = tuple(lst)
                ret_tup += new_tup
            return ret_tup

        @property
        def max_speed_hz(self):
            """Get the maximum bus speed in hz.

            :returns: The max bus speed.
            :rtype: int
            """
            return self.__maxSpeed

        @max_speed_hz.setter
        def max_speed_hz(self, speed):
            """Set the max bus speed in hz.

            :param int speed: The max speed.
            """
            self.__maxSpeed = speed


class PiFaceGpioDigital(PiFaceGPIO):
    """PiFace GPIO pin implementing SPI."""

    ADDR_0 = 0x01000000  # 0x40 [0100 0000]
    ADDR_1 = 0x01000010  # 0x42 [0100 0010]
    ADDR_2 = 0x01000100  # 0x44 [0100 0100]
    ADDR_3 = 0x01000110  # 0x46 [0100 0110]
    DEF_ADDR = ADDR_0

    REGISTER_IODIR_A = 0x00
    REGISTER_IODIR_B = 0x01
    REGISTER_GPINTEN_A = 0x04
    REGISTER_GPINTEN_B = 0x05
    REGISTER_DEFVAL_A = 0x06
    REGISTER_DEFVAL_B = 0x07
    REGISTER_INTCON_A = 0x08
    REGISTER_INTCON_B = 0x09
    REGISTER_IOCON_A = 0x0A
    REGISTER_IOCON_B = 0x0B
    REGISTER_GPPU_A = 0x0C
    REGISTER_GPPU_B = 0x0D
    REGISTER_INTF_A = 0x0E
    REGISTER_INTF_B = 0x0F
    REGISTER_INTCAP_A = 0x10
    REGISTER_INTCAP_B = 0x11
    REGISTER_GPIO_A = 0x12
    REGISTER_GPIO_B = 0x13

    GPIO_A_OFFSET = 0
    GPIO_B_OFFSET = 1000

    IOCON_UNUSED = 0x01
    IOCON_INTPOL = 0x02
    IOCON_ODR = 0x04
    IOCON_HAEN = 0x08
    IOCON_DISSLW = 0x10
    IOCON_SEQOP = 0x20
    IOCON_MIRROR = 0x40
    IOCON_BANK_MODE = 0x80

    BUS_SPEED = 1000000
    WRT_FLAG = 0x00
    RD_FLAG = 0x01

    def __init__(self, pn, initial_val, spi_address, spi_speed):
        """Initialize a new instance of the raspy.io.pi_face_gpio_digital.PiFaceGpioDigital class.

        :param raspy.io.pi_face_pins.PiFacePin pn: The PiFace pin to control.
        :param int initial_val: The initial value (state) to set the pin to.
        Default is PinState.LOW.
        :param int spi_address: The SPI address to use. (Should be ADDRESS_0,
        ADDRESS_1, ADDRESS_2, or ADDRESS_3).
        :param int spi_speed: The clock speed to set the bus to. Can be powers
        of 2 (500KHz minimum up to 32MHz maximum). If not specified, the
        default of SPI_SPEED (1MHz) will be used.
        :raises: raspy.io.io_exception.IOException if unable to read or write
        to the SPI bus.
        """
        PiFaceGPIO.__init__(self, pn, initial_val, pn.name)

        if spi_speed is None or not isinstance(spi_speed, (int, long)):
            spi_speed = self.BUS_SPEED

        self.__speed = spi_speed
        self.__spi = SpiDev()
        try:
            self.__spi.open(0, 0)
        except Exception:
            raise IOException("Unable to open SPI device 0 on bus 0.")

        self.__spi.max_speed_hz = self.__speed
        self.__address = self.DEF_ADDR
        if spi_address is not None:
            self.__address = spi_address

        self.__currentStatesA = 0x00000000
        self.__currentStatesB = 0x11111111
        self.__currentDirectionA = 0x00000000
        self.__currentDirectionB = 0x11111111
        self.__currentPullupA = 0x00000000
        self.__currentPullupB = 0x11111111
        self.__oldState = pin_state.LOW
        self.__pullResistance = pin_pull_resistance.Off
        self.__pollThread = None
        self.__pollRunning = False
        self.__stopEvent = threading.Event()
        self.__stopEvent.set()

        # IOCON - I/O EXPANDER CONFIGURATION REGISTER
        #
        # bit 7 BANK: Controls how the registers are addressed
        #     1 = The registers associated with each port are separated into
        # different banks
        # 0 = The registers are in the same bank (addresses are sequential)
        # bit 6 MIRROR: INT Pins Mirror bit
        # 1 = The INT pins are internally connected
        # 0 = The INT pins are not connected. INTA is associated with PortA and
        # INTB is associated with PortB
        # bit 5 SEQOP: Sequential Operation mode bit.
        # 1 = Sequential operation disabled, address pointer does not
        # increment.
        # 0 = Sequential operation enabled, address pointer increments.
        # bit 4 DISSLW: Slew Rate control bit for SDA output.
        # 1 = Slew rate disabled.
        # 0 = Slew rate enabled.
        # bit 3 HAEN: Hardware Address Enable bit (MCP23S17 only).
        # Address pins are always enabled on MCP23017.
        # 1 = Enables the MCP23S17 address pins.
        # 0 = Disables the MCP23S17 address pins.
        # bit 2 ODR: This bit configures the INT pin as an open-drain output.
        # 1 = Open-drain output (overrides the INTPOL bit).
        # 0 = Active driver output (INTPOL bit sets the polarity).
        # bit 1 INTPOL: This bit sets the polarity of the INT output pin.
        # 1 = Active-high.
        # 0 = Active-low.
        # bit 0 Unimplemented: Read as '0'.
        #

        # write io configuration. enable hardware address.
        self.__write(self.REGISTER_IOCON_A, self.IOCON_SEQOP | self.IOCON_HAEN)
        self.__write(self.REGISTER_IOCON_B, self.IOCON_SEQOP | self.IOCON_HAEN)

        # read initial GPIO pin states
        self.__currentStatesA = self.__read(self.REGISTER_GPIO_A)
        self.__currentStatesB = self.__read(self.REGISTER_GPIO_B)

        # set all default pin pull up resistors
        # (1 = Pull-up enabled.)
        # (0 = Pull-up disabled.)
        self.__write(self.REGISTER_IODIR_A, self.__currentDirectionA)
        self.__write(self.REGISTER_IODIR_B, self.__currentDirectionB)

        # set all default pin states
        self.__write(self.REGISTER_GPIO_A, self.__currentStatesA)
        self.__write(self.REGISTER_GPIO_B, self.__currentStatesB)

        # set all default pin pull up resistors
        # (1 = Pull-up enabled.)
        # (0 = Pull-up disabled.)
        self.__write(self.REGISTER_GPPU_A, self.__currentPullupA)
        self.__write(self.REGISTER_GPPU_B, self.__currentPullupB)

        # set all default pin interrupts
        # (if pin direction is input (1), then enable interrupt for pin)
        # (1 = Enable GPIO input pin for interrupt-on-change event.)
        # (0 = Disable GPIO input pin for interrupt-on-change event.)
        self.__write(self.REGISTER_GPINTEN_A, self.__currentDirectionA)
        self.__write(self.REGISTER_GPINTEN_B, self.__currentDirectionB)

        # set all default pin interrupt default values
        # (comparison value registers are not used in this implementation)
        self.__write(self.REGISTER_DEFVAL_A, 0x00)
        self.__write(self.REGISTER_DEFVAL_B, 0x00)

        # set all default pin interrupt comparison behaviors
        # (1 = Controls how the associated pin value is compared for
        # interrupt-on-change.)
        # (0 = Pin value is compared against the previous pin value.)
        self.__write(self.REGISTER_INTCON_A, 0x00)
        self.__write(self.REGISTER_INTCON_B, 0x00)

        # reset/clear interrupt flags
        if self.__currentDirectionA > 0:
            self.__read(self.REGISTER_INTCAP_A)

        if self.__currentDirectionB > 0:
            self.__read(self.REGISTER_INTCAP_B)

    def __write(self, register, data):
        """Write the specified byte to the specified register.

        :param int register: The register to write to. This should be one of
        the register constants.
        :param int data: A single byte to write to the register.
        :raises: raspy.io.io_exception.IOException if unable to write to the
        SPI bus.
        """
        # create packet in data buffer.
        packet = [
            self.__address | self.WRT_FLAG,  # address byte
            register,                        # register byte
            data                             # data byte
        ]

        try:
            self.__spi.writebytes(packet)
        except(IOError, SystemError, RuntimeError) as ex:
            err_msg = "Failed to write to SPI bus device at address "
            err_msg += str(self.__address) + " on channel /dev/spidev0.0"
            err_msg += str(ex)
            raise IOException(err_msg)

    def __read(self, register):
        """Read a single byte from the specified register.

        :param int register: The register to write to. This should be one of
        the register constants.
        :returns: The byte read.
        :rtype: int
        :raises: raspy.io.io_exception.IOException if unable to read from
        the SPI bus.
        """
        # create packet in data buffer.
        packet = [
            self.__address | self.RD_FLAG,  # address byte
            register,                       # register byte
            0x00000000                      # data byte
        ]

        result = 0
        try:
            temp = self.__spi.xfer(packet, self.__speed)
            if temp is not None:
                result = temp[2] & 0xFF
        except(IOError, SystemError, RuntimeError) as ex:
            err_msg = "Failed to write to SPI bus device at address "
            err_msg += str(self.__address) + " on channel /dev/spidev0.0"
            err_msg += str(ex)
            raise IOException(err_msg)

        return result

    def __set_state_a(self, state):
        """Set the state of this pin if on Port A (outputs).

        :param int state: The state to set.
        :raises: raspy.io.io_exception.IOException if unable to write to
        the SPI port.
        """
        # determine pin address.
        pin_address = self.inner_pin.value - self.GPIO_A_OFFSET

        # determine state value for pin bit
        if state == pin_state.HIGH:
            self.__currentStatesA |= pin_address
        else:
            self.__currentStatesA &= ~pin_address

        # update state value.
        self.__write(self.REGISTER_GPIO_A, self.__currentStatesA)

    def __set_state_b(self, state):
        """Set the state of this pin if on Port B (inputs).

        :param int state: The state to set.
        :raises: raspy.io.io_exception.IOException if unable to write to the
        SPI port.
        """
        # determine pin address
        pin_address = self.inner_pin.value - self.GPIO_B_OFFSET

        # determine state value for pin bit
        if state == pin_state.HIGH:
            self.__currentStatesB |= pin_address
        else:
            self.__currentStatesB &= ~pin_address

        # update state value.
        self.__write(self.REGISTER_GPIO_B, self.__currentStatesB)

    def __set_state(self, state):
        """Set the state of this pin.

        :param int state: The state to set.
        :raises: raspy.io.io_exception.IOException if unable to write to the
        SPI port.
        """
        if self.state == state:
            return

        self.__oldState = self.state
        PiFaceGPIO.write(self, state)

        # determine A or B port based on pin address.
        if self.inner_pin.value == self.GPIO_B_OFFSET:
            self.__set_state_a(state)
        else:
            self.__set_state_b(state)

    def write(self, state):
        """Write a value to the pin.

        :param int state: The pin state value to write to the pin.
        :raises: raspy.ObjectDisposedException if this instance has been
        disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("PiFaceGpioDigital")

        PiFaceGPIO.write(self, state)
        self.__set_state(state)

    def __evaluate_pin_for_change_a(self, state):
        """Evaluate Port A for pin change.

        If the state is different compared to the specified state, then emits
        a raspy.io.gpio.EVENT_GPIO_STATE_CHANGED event.

        :param int state: The state to check against.
        """
        # determine pin address.
        pin_address = self.inner_pin.value - self.GPIO_A_OFFSET

        # determine if state changed.
        if (state & pin_address) != (self.__currentStatesA & pin_address):
            # Determine new state value for pin bit.
            new_state = pin_state.LOW
            if (state & pin_address) == pin_address:
                new_state = pin_state.HIGH

            if new_state == pin_state.HIGH:
                self.__currentStatesA |= pin_address
            else:
                self.__currentStatesA &= ~pin_address

            # change detected for pin.
            evt = PinStateChangeEvent(self.__oldState, new_state, pin_address)
            self.on_pin_state_change(evt)

    def __evaluate_pin_for_change_b(self, state):
        """Evaluate Port B for pin change.

        If the state is different compared to the specified state, then emits
        a raspy.io.Gpio.EVENT_GPIO_STATE_CHANGED event.

        :param int state: The state to check against.
        """
        # determine pin address.
        pin_address = self.inner_pin.value - self.GPIO_B_OFFSET

        # determine if state changed.
        if (state & pin_address) != (self.__currentStatesB & pin_address):
            # Determine new state value for pin bit.
            new_state = pin_state.LOW
            if (state & pin_address) == pin_address:
                new_state = pin_state.HIGH

            if new_state == pin_state.HIGH:
                self.__currentStatesB |= pin_address
            else:
                self.__currentStatesB &= ~pin_address

            # change detected for pin.
            evt = PinStateChangeEvent(self.__oldState, new_state, pin_address)
            self.on_pin_state_change(evt)

    def __set_mode_a(self, mode):
        """Set the mode of this pin on Port A.

        :param int mode: The pin mode to set.
        :raises: raspy.io.io_exception.IOException if unable to write to the
        SPI bus.
        """
        pin_address = self.inner_pin.value - self.GPIO_A_OFFSET

        if mode == pin_mode.IN:
            self.__currentDirectionA |= pin_address
        elif mode == pin_mode.OUT:
            self.__currentDirectionA &= ~pin_address

        self.__write(self.REGISTER_IODIR_A, self.__currentDirectionA)
        self.__write(self.REGISTER_GPINTEN_A, self.__currentDirectionA)

    def __set_mode_b(self, mode):
        """Set the mode of this pin on Port B.

        :param int mode: The pin mode to set.
        :raises: raspy.io.io_exception.IOException if unable to write to the
        SPI bus.
        """
        pin_address = self.inner_pin.value - self.GPIO_B_OFFSET

        if mode == pin_mode.IN:
            self.__currentDirectionB |= pin_address
        elif mode == pin_mode.OUT:
            self.__currentDirectionB &= ~pin_address

        self.__write(self.REGISTER_IODIR_B, self.__currentDirectionB)
        self.__write(self.REGISTER_GPINTEN_B, self.__currentDirectionB)

    def __background_poll(self):
        """The background (asynchronous) poll cycle routine.

        This is the callback executed by the poll thread.

        :raises: raspy.io.IOException if unable to write to the SPI bus.
        """
        while not self.__stopEvent.is_set():
            # only process for interrupts if a pin on port A is configured as
            # an input pin.
            pin_interrupt_state = -1
            if self.__currentDirectionA > 0:
                # process interrupts for port A.
                pin_interrupt_a = self.__read(self.REGISTER_INTF_A)

                # validate that there is at least one interrupt active on port
                # A.
                if pin_interrupt_a > 0:
                    # read the current pin states on port A.
                    pin_interrupt_state = self.__read(self.REGISTER_GPIO_A)

                    # is there an interrupt flag on this pin?
                    self.__evaluate_pin_for_change_a(pin_interrupt_state)

            # only process for interrupts if a pin on port B is configured as
            # an input pin.
            if self.__currentDirectionB > 0:
                # process interrupts for port B.
                pin_interrupt_b = self.__read(self.REGISTER_INTF_B)

                # validate that there is at least one interrupt active on port
                # B.
                if pin_interrupt_b > 0:
                    # read the current pin states on port B.
                    pin_interrupt_state = self.__read(self.REGISTER_GPIO_B)

                    # is there an interrupt flag on this pin?
                    self.__evaluate_pin_for_change_b(pin_interrupt_state)

    def cancel_poll(self):
        """Cancel an input poll cycle (if running) started by poll()."""
        if self.is_disposed:
            return

        if self.__stopEvent.is_set() or self.__pollThread is None:
            return

        self.__stopEvent.set()
        self.__pollRunning = False

    def poll(self):
        """Start a pin poll cycle.

        This will monitor the pin and check for state changes. If a state
        change is detected, the raspy.io.Gpio.EVENT_GPIO_STATE_CHANGED event
        will be emitted. The poll cycle runs asynchronously until stopped by
        the cancel_poll() method or when this object instance is disposed.

        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        :raises: raspy.invalid_operation_exception.InvalidOperationException
        if the poll thread is already running.
        """
        if self.is_disposed:
            raise ObjectDisposedException("PiFaceGpioDigital")

        if self.__pollRunning:
            raise InvalidOperationException("Poll thread already running.")

        self.__stopEvent.clear()
        self.__pollThread = threading.Thread(target=self.__background_poll)
        self.__pollThread.name = "PiFaceGpioPoller"
        self.__pollThread.daemon = True
        self.__pollThread.start()
        self.__pollRunning = True

    @property
    def mode(self):
        """Get the pin mode.

        :returns: The pin mode.
        :rtype: int
        """
        return super(PiFaceGPIO, self).mode

    @mode.setter
    def mode(self, p_mode):
        """Set the pin mode.

        :param int p_mode: The pin mode to set.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("PiFaceGpioDigital")

        if p_mode is None:
            p_mode = p_mode.TRI

        super(PiFaceGPIO, self).mode = p_mode

        # determine A or B port based on pin address
        if self.inner_pin.value < self.GPIO_B_OFFSET:
            self.__set_mode_a(p_mode)
        else:
            self.__set_mode_b(p_mode)

        # if any pins are configured as input pins, then we need to start the
        # interrupt monitoring poll timer.
        if self.__currentDirectionA > 0 or self.__currentDirectionB > 0:
            self.poll()
        else:
            self.cancel_poll()

    def provision(self):
        """Provision this pin.

        :raises: raspy.ObjectDisposedException if this instance has been
        disposed.
        """
        self.write(self.__get_initial_pin_value())

    def __set_pull_resistance_a(self, resistance):
        """Set the pin pull-up/down resistance for port A.

        :param raspy.io.pin_pull_resistance.PinPullResistance resistance: The
        pin pull resistance flag to set. Can enable the internal pull-up or
        pull-down resistor, or disable it.
        :raises: raspy.io.io_exception.IOException if unable to write to the
        SPI port.
        """
        pin_address = self.inner_pin.value - self.GPIO_A_OFFSET

        if resistance.value == pin_pull_resistance.PullUp.value:
            self.__currentPullupA |= pin_address
        else:
            self.__currentPullupA &= ~pin_address

        self.__write(self.REGISTER_GPPU_A, self.__currentPullupA)

    def __set_pull_resistance_b(self, resistance):
        """Set the pin pull-up/down resistance for port B.

        :param raspy.io.pin_pull_resistance.PinPullResistance resistance: The
        pin pull resistance flag to set. Can enable the internal pull-up or
        pull-down resistor, or disable it.
        :raises: raspy.io.io_exception.IOException if unable to write to the
        SPI port.
        """
        pin_address = self.inner_pin.value - self.GPIO_B_OFFSET

        if resistance.value == pin_pull_resistance.PullUp.value:
            self.__currentPullupB |= pin_address
        else:
            self.__currentPullupB &= ~pin_address

        self.__write(self.REGISTER_GPPU_B, self.__currentPullupB)

    @property
    def pull_resistance(self):
        """Get the pin pull-up/down resistance.

        :returns: The pin pull resistance.
        :rtype: raspy.io.pin_pull_resistance.PinPullResistance
        """
        return self.__pullResistance

    @pull_resistance.setter
    def pull_resistance(self, resistance):
        """Set the pin pull-up/down resistance.

        :param raspy.io.pin_pull_resistance.PinPullResistance resistance: The
        pin pull resistance.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        :raises: raspy.io.io_exception.IOException if unable to write to the
        SPI port.
        """
        if self.__pullResistance.value == resistance.value:
            return

        if self.is_disposed:
            raise ObjectDisposedException("PiFaceGpioDigital")

        self.__pullResistance = resistance
        if self.inner_pin.value > self.GPIO_B_OFFSET:
            self.__set_pull_resistance_a(resistance)
        else:
            self.__set_pull_resistance_b(resistance)

    def read(self):
        """Read a value from the pin.

        :returns: The state (value) of the pin.
        :rtype: int
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        :raises: raspy.io.io_exception.IOException if unable to read from the
        SPI port.
        """
        if self.is_disposed:
            raise ObjectDisposedException("PiFaceGpioDigital")

        if self.inner_pin.value < self.GPIO_B_OFFSET:
            return self.__read(self.REGISTER_GPIO_A)

        return self.__read(self.REGISTER_GPIO_B)

    def __get_state_a(self):
        """Get the state of the pin if on Port A.

        :returns: The state of the pin.
        :rtype: int
        :raises: raspy.io.io_exception.IOException if unable to write to the
        SPI port.
        """
        pin_address = self.inner_pin.value - self.GPIO_A_OFFSET
        temp_state = (self.__currentStatesA & pin_address)
        my_state = pin_state.LOW
        if temp_state == pin_address:
            my_state = pin_state.HIGH

        super(PiFaceGPIO, self).write(my_state)
        return my_state

    def __get_state_b(self):
        """Get the state of the pin if on Port B.

        :returns: The state of the pin.
        :rtype: int
        :raises: raspy.io.io_exception.IOException if unable to write to the
        SPI port.
        """
        pin_address = self.inner_pin.value - self.GPIO_B_OFFSET
        temp_state = (self.__currentStatesB & pin_address)
        my_state = pin_state.LOW
        if temp_state == pin_address:
            my_state = pin_state.HIGH

        super(PiFaceGPIO, self).write(my_state)
        return my_state

    @property
    def state(self):
        """Get the state of the pin.

        :returns: The pin state.
        :rtype: int
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        :raises: raspy.io.io_exception.IOException if unable to read from the
        SPI port.
        """
        if self.is_disposed:
            raise ObjectDisposedException("PiFaceGpioDigital")

        if self.inner_pin.value < self.GPIO_B_OFFSET:
            result = self.__get_state_a()
        else:
            result = self.__get_state_b()

        return result

    def dispose(self):
        """Dispose managed resources.

        Performs application-defined tasks associated with freeing, releasing,
        or resetting resources.
        """
        if self.is_disposed:
            return

        self.cancel_poll()
        self.__spi = None
        super(PiFaceGPIO, self).dispose()
