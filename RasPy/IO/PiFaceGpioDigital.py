"""PiFace GPIO pin implementing SPI.

The PiFace is an expansion board for the Raspberry Pi.

PiFaceGpioDigital.py

Author:
      Chris Brunner <cyrusbuilt at gmail dot com>

  Copyright (c) 2017 CyrusBuilt

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
"""

import spidev
import threading
from RasPy.InvalidOperationException import InvalidOperationException
from RasPy.ObjectDisposedException import ObjectDisposedException
from RasPy.IO import PinState
from RasPy.IO import PinMode
from RasPy.IO import PinPullResistance
from RasPy.IO.IOException import IOException
from RasPy.IO.PiFaceGPIO import PiFaceGPIO
from RasPy.IO.PinStateChangeEvent import PinStateChangeEvent


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

    def __init__(self, pn, initialVal, spiAddress, spiSpeed):
        """Initialize a new instance of the RasPy.IO.PiFaceGpioDigital class.

        :param pn: The PiFace pin to control.
        :param initialVal: The initial value (state) to set the pin to.
        Default is PinState.LOW.
        :param spiAddress: The SPI address to use. (Should be ADDRESS_0,
        ADDRESS_1, ADDRESS_2, or ADDRESS_3).
        :param spiSpeed: The clock speed to set the bus to. Can be powers
        of 2 (500KHz minimum up to 32MHz maximum). If not specified, the
        default of SPI_SPEED (1MHz) will be used.
        :type pn: object
        :type initialVal: int
        :type spiAddress: int
        :type spiSpeed: int
        :raises: RasPy.IO.IOException if unable to read or write to the SPI
        bus.
        """
        super(PiFaceGpioDigital, self).__init(pn, initialVal, None)

        if spiSpeed is None or not isinstance(spiSpeed, (int, long)):
            spiSpeed = self.BUS_SPEED

        self.__speed = spiSpeed
        self.__spi = spidev.SpiDev()
        try:
            self.__spi.open(0, 0)
        except:
            raise IOException("Unable to open SPI device 0 on bus 0.")

        self.__spi.max_speed_hz = self.__speed
        self.__address = self.DEF_ADDR
        if spiAddress is not None:
            self.__address = spiAddress

        self.__currentStatesA = 0x00000000
        self.__currentStatesB = 0x11111111
        self.__currentDirectionA = 0x00000000
        self.__currentDirectionB = 0x11111111
        self.__currentPullupA = 0x00000000
        self.__currentPullupB = 0x11111111
        self.__oldState = PinState.LOW
        self.__pullResistance = PinPullResistance.OFF
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

        # write IO configuration. enable hardware address.
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

        :param register: The register to write to. This should be one of
        the register constants.
        :param data: A single byte to write to the register.
        :type register: int
        :type data: int
        :raises: RasPy.IO.IOException if unable to write to the SPI bus.
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
            errMsg = "Failed to write to SPI bus device at address "
            errMsg += str(self.__address) + " on channel /dev/spidev0.0"
            errMsg += str(ex)
            raise IOException(errMsg)

    def __read(self, register):
        """Read a single byte from the specified register.

        :param register: The register to write to. This should be one of the
        register constants.
        :type register: int
        :returns: The byte read.
        :rtype: int
        :raises: RasPy.IO.IOException if unable to read from the SPI bus.
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
            errMsg = "Failed to write to SPI bus device at address "
            errMsg += str(self.__address) + " on channel /dev/spidev0.0"
            errMsg += str(ex)
            raise IOException(errMsg)

        return result

    def __set_state_A(self, state):
        """Set the state of this pin if on Port A (outputs).

        :param state: The state to set.
        :type state: int
        :raises: RasPy.IO.IOException if unable to write to the SPI port.
        """
        # determine pin address.
        pinAddress = self.inner_pin.value - self.GPIO_A_OFFSET

        # determine state value for pin bit
        if state == PinState.HIGH:
            self.__currentStatesA |= pinAddress
        else:
            self.__currentStatesA &= ~pinAddress

        # update state value.
        self.__write(self.REGISTER_GPIO_A, self.__currentStatesA)

    def __set_state_B(self, st):
        """Set the state of this pin if on Port B (inputs).

        :param st: The state to set.
        :type st: int
        :raises: RasPy.IO.IOException if unable to write to the SPI port.
        """
        # determine pin address
        pinAddress = self.inner_pin.value - self.GPIO_B_OFFSET

        # determine state value for pin bit
        if st == PinState.HIGH:
            self.__currentStatesB |= pinAddress
        else:
            self.__currentStatesB &= ~pinAddress

        # update state value.
        self.__write(self.REGISTER_GPIO_B, self.__currentStatesB)

    def __set_state(self, st):
        """Set the state of this pin.

        :param st: The state to set.
        :type st: int
        :raises: RasPy.IO.IOException if unable to write to the SPI port.
        """
        if self.state == st:
            return

        self.__oldState = self.state
        super(PiFaceGpioDigital, self).write(st)

        # determine A or B port based on pin address.
        if self.inner_pin.value == self.GPIO_B_OFFSET:
            self.__set_state_A(st)
        else:
            self.__set_state_B(st)

    def write(self, ps):
        """Write a value to the pin.

        :param ps: The pin state value to write to the pin.
        :type ps: int
        :raises: RasPy.ObjectDisposedException if this instance has been
        disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("PiFaceGpioDigital")

        super(PiFaceGpioDigital, self).write(ps)
        self.__set_state(ps)

    def __evaluate_pin_for_change_A(self, ps):
        """Evaluate Port A for pin change.

        If the state is different compared to the specified state, then emits
        a RasPy.IO.Gpio.EVENT_GPIO_STATE_CHANGED event.

        :param ps: The state to check against.
        :type ps: int
        """
        # determine pin address.
        pinAddress = self.inner_pin.value - self.GPIO_A_OFFSET

        # determine if state changed.
        if (ps & pinAddress) != (self.__currentStatesA & pinAddress):
            # Determine new state value for pin bit.
            newState = PinState.LOW
            if (ps & pinAddress) == pinAddress:
                newState = PinState.HIGH

            if newState == PinState.HIGH:
                self.__currentStatesA |= pinAddress
            else:
                self.__currentStatesA &= ~pinAddress

            # change detected for pin.
            evt = PinStateChangeEvent(self.__oldState, newState, pinAddress)
            self.on_pin_state_change(evt)

    def __evaluate_pin_for_change_B(self, ps):
        """Evaluate Port B for pin change.

        If the state is different compared to the specified state, then emits
        a RasPy.IO.Gpio.EVENT_GPIO_STATE_CHANGED event.

        :param ps: The state to check against.
        :type ps: int
        """
        # determine pin address.
        pinAddress = self.inner_pin.value - self.GPIO_B_OFFSET

        # determine if state changed.
        if (ps & pinAddress) != (self.__currentStatesB & pinAddress):
            # Determine new state value for pin bit.
            newState = PinState.LOW
            if (ps & pinAddress) == pinAddress:
                newState = PinState.HIGH

            if newState == PinState.HIGH:
                self.__currentStatesB |= pinAddress
            else:
                self.__currentStatesB &= ~pinAddress

            # change detected for pin.
            evt = PinStateChangeEvent(self.__oldState, newState, pinAddress)
            self.on_pin_state_change(evt)

    def __set_mode_A(self, md):
        """Set the mode of this pin on Port A.

        :param md: The pin mode to set.
        :type md: int
        :raises: RasPy.IO.IOException if unable to write to the SPI bus.
        """
        pinAddress = self.inner_pin.value - self.GPIO_A_OFFSET

        if md == PinMode.IN:
            self.__currentDirectionA |= pinAddress
        elif md == PinMode.OUT:
            self.__currentDirectionA &= ~pinAddress

        self.__write(self.REGISTER_IODIR_A, self.__currentDirectionA)
        self.__write(self.REGISTER_GPINTEN_A, self.__currentDirectionA)

    def __set_mode_B(self, md):
        """Set the mode of this pin on Port B.

        :param md: The pin mode to set.
        :type md: int
        :raises: RasPy.IO.IOException if unable to write to the SPI bus.
        """
        pinAddress = self.inner_pin.value - self.GPIO_B_OFFSET

        if md == PinMode.IN:
            self.__currentDirectionB |= pinAddress
        elif md == PinMode.OUT:
            self.__currentDirectionB &= ~pinAddress

        self.__write(self.REGISTER_IODIR_B, self.__currentDirectionB)
        self.__write(self.REGISTER_GPINTEN_B, self.__currentDirectionB)

    def __background_poll(self):
        """The background (asynchronous) poll cycle routine.

        This is the callback executed by the poll thread.

        :raises: RasPy.IO.IOException if unable to write to the SPI bus.
        """
        while not self.__stopEvent.is_set():
            # only process for interrupts if a pin on port A is configured as
            # an input pin.
            pinInterruptState = -1
            if self.__currentDirectionA > 0:
                # process interrupts for port A.
                pinInterruptA = self.__read(self.REGISTER_INTF_A)

                # validate that there is at least one interrupt active on port
                # A.
                if pinInterruptA > 0:
                    # read the current pin states on port A.
                    pinInterruptState = self.__read(self.REGISTER_GPIO_A)

                    # is there an interrupt flag on this pin?
                    self.__evaluate_pin_for_change_A(pinInterruptState)

            # only process for interrupts if a pin on port B is configured as
            # an input pin.
            if self.__currentDirectionB > 0:
                # process interrupts for port B.
                pinInterruptB = self.__read(self.REGISTER_INTF_B)

                # validate that there is at least one interrupt active on port
                # B.
                if pinInterruptB > 0:
                    # read the current pin states on port B.
                    pinInterruptState = self.__read(self.REGISTER_GPIO_B)

                    # is there an interrupt flag on this pin?
                    self.__evaluate_pin_for_change_B(pinInterruptState)

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
        change is detected, the RasPy.IO.Gpio.EVENT_GPIO_STATE_CHANGED event
        will be emitted. The poll cycle runs asynchronously until stopped by
        the cancel_poll() method or when this object instance is disposed.

        :raises: RasPy.ObjectDisposedException if this instance has been
        disposed.
        :raises: RasPy.InvalidOperationException if the poll thread is already
        running.
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
        return super(PiFaceGpioDigital, self).mode

    @mode.setter
    def mode(self, m):
        """Set the pin mode.

        :param m: The pin mode to set.
        :type m: int
        :raises: RasPy.ObjectDisposedException if this instance has been
        disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("PiFaceGpioDigital")

        if m is None:
            m = PinMode.TRI

        super(PiFaceGpioDigital, self).mode = m

        # determine A or B port based on pin address
        if self.inner_pin.value < self.GPIO_B_OFFSET:
            self.__set_mode_A(m)
        else:
            self.__set_mode_B(m)

        # if any pins are configured as input pins, then we need to start the
        # interrupt monitoring poll timer.
        if self.__currentDirectionA > 0 or self.__currentDirectionB > 0:
            self.poll()
        else:
            self.cancel_poll()

    def provision(self):
        """Provision this pin.

        :raises: RasPy.ObjectDisposedException if this instance has been
        disposed.
        """
        self.write(self.__get_initial_pin_value())

    def __set_pull_resistanceA(self, resistance):
        """Set the pin pull-up/down resistance for port A.

        :param resistance: The pin pull resistance flag to set. Can enable the
        internal pull-up or pull-down resistor, or disable it.
        :type resistance: object
        :raises: RasPy.IO.IOException if unable to write to the SPI port.
        """
        pinAddress = self.inner_pin.value - self.GPIO_A_OFFSET

        if resistance.value == PinPullResistance.PULL_UP.value:
            self.__currentPullupA |= pinAddress
        else:
            self.__currentPullupA &= ~pinAddress

        self.__write(self.REGISTER_GPPU_A, self.__currentPullupA)

    def __set_pull_resistanceB(self, resistance):
        """Set the pin pull-up/down resistance for port A.

        :param resistance: The pin pull resistance flag to set. Can enable the
        internal pull-up or pull-down resistor, or disable it.
        :type resistance: object
        :raises: RasPy.IO.IOException if unable to write to the SPI port.
        """
        pinAddress = self.inner_pin.value - self.GPIO_B_OFFSET

        if resistance.value == PinPullResistance.PULL_UP.value:
            self.__currentPullupB |= pinAddress
        else:
            self.__currentPullupB &= ~pinAddress

        self.__write(self.REGISTER_GPPU_B, self.__currentPullupB)

    @property
    def pull_resistance(self):
        """Get the pin pull-up/down resistance.

        :returns: The pin pull resistance.
        :rtype: object
        """
        return self.__pullResistance

    @pull_resistance.setter
    def pull_resistance(self, resistance):
        """Set the pin pull-up/down resistance.

        :param resistance: The pin pull resistance.
        :type resistance: object
        :raises: RasPy.ObjectDisposedException if this instance has been
        disposed.
        :raises: RasPy.IO.IOException if unable to write to the SPI port.
        """
        if self.__pullResistance.value == resistance.value:
            return

        if self.is_disposed:
            raise ObjectDisposedException("PiFaceGpioDigital")

        self.__pullResistance = resistance
        if self.inner_pin.value > self.GPIO_B_OFFSET:
            self.__set_pull_resistanceA(resistance)
        else:
            self.__set_pull_resistanceB(resistance)

    def read(self):
        """Read a value from the pin.

        :returns: The state (value) of the pin.
        :rtype: int
        :raises: RasPy.ObjectDisposedException if this instance has been
        disposed.
        :raises: RasPy.IO.IOException if unable to read from the SPI port.
        """
        if self.is_disposed:
            raise ObjectDisposedException("PiFaceGpioDigital")

        if self.inner_pin.value < self.GPIO_B_OFFSET:
            return self.__read(self.REGISTER_GPIO_A)

        return self.__read(self.REGISTER_GPIO_B)

    def __get_stateA(self):
        """Get the state of the pin if on Port A.

        :returns: The state of the pin.
        :rtype: int
        :raises: RasPy.IO.IOException if unable to write to the SPI port.
        """
        pinAddress = self.inner_pin.value - self.GPIO_A_OFFSET
        tempState = (self.__currentStatesA & pinAddress)
        myState = PinState.LOW
        if tempState == pinAddress:
            myState = PinState.HIGH

        super(PiFaceGpioDigital, self).write(myState)
        return myState

    def __get_stateB(self):
        """Get the state of the pin if on Port B.

        :returns: The state of the pin.
        :rtype: int
        :raises: RasPy.IO.IOException if unable to write to the SPI port.
        """
        pinAddress = self.inner_pin.value - self.GPIO_B_OFFSET
        tempState = (self.__currentStatesB & pinAddress)
        myState = PinState.LOW
        if tempState == pinAddress:
            myState = PinState.HIGH

        super(PiFaceGpioDigital, self).write(myState)
        return myState

    @property
    def state(self):
        """Get the state of the pin.

        :returns: The pin state.
        :rtype: int
        :raises: RasPy.ObjectDisposedException if this instance has been
        disposed.
        :raises: RasPy.IO.IOException if unable to read from the SPI port.
        """
        if self.is_disposed:
            raise ObjectDisposedException("PiFaceGpioDigital")

        result = super(PiFaceGpioDigital, self).state
        if self.inner_pin.value < self.GPIO_B_OFFSET:
            result = self.__get_stateA()
        else:
            result = self.__get_stateB()

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
        super(PiFaceGpioDigital, self).dispose()
