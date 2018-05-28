"""Implemented by classes that represent GPIO pins on the Raspberry Pi.

Gpio.py

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

import time
from pyee import EventEmitter
from RasPy import BoardRevision
from RasPy.ObjectDisposedException import ObjectDisposedException
from RasPy.IO import GpioPins
from RasPy.IO import PinState
from RasPy.IO import PinMode
from RasPy.IO.Pin import Pin


EVENT_GPIO_STATE_CHANGED = "gpioStateChanged"
"""The name of the GPIO state changed event."""


class Gpio(Pin):
    """Implemented by classes that represent GPIO pins on the Raspberry Pi."""

    __pin = None
    __mode = None
    __initValue = None
    __revision = None
    __state = None
    __emitter = None

    def __init__(self, pn, mode, value):
        """Initialize a new instance of RasPy.IO.Gpio.

        :param pn: The GPIO pin.
        :param mode: The I/O pin mode.
        :param value: The initial pin value.
        :type pn: RasPy.IO.GpioPins
        :type mode: int
        :type value: int
        """
        super(Gpio, self).__init__()
        self.__emitter = EventEmitter()

        self.__pin = pn
        if self.__pin is None:
            self.__pin = GpioPins.GPIO_NONE

        self.__mode = mode
        if not isinstance(self.__mode, (int, long)):
            self.__mode = PinMode.OUT

        self.__initValue = value
        if not isinstance(self.__initValue, (int, long)):
            self.__initValue = PinState.LOW

        self.__revision = BoardRevision.REV2
        self.__state = PinState.LOW

    def on(self, evt, callback):
        """Register an event with a callback to handle it.

        :param evt: The name of the event to register a handler for.
        :param callback: The callback to execute when the event fires.
        :type evt: string
        :type callback: function
        """
        if self.is_disposed:
            raise ObjectDisposedException("Gpio")

        self.__emitter.on(evt, callback)

    def emit(self, evt, args):
        """Emit the specified event to all registered listeners.

        :param evt: The name of the event to emit.
        :param args: The arguments to pass to the event handlers (listeners).
        :type evt: string
        :type args: object
        """
        if self.is_disposed:
            raise ObjectDisposedException("Gpio")

        self.__emitter.emit(evt, args)

    def remove_all_listeners(self):
        """Remove all registered event listeners."""
        if self.is_disposed:
            return

        if self.__emitter is not None:
            self.__emitter.remove_all_listeners()

    def write(self, ps):
        """Write a value to the pin.

        :param ps: The pin state value to write to the pin.
        :type ps: int
        :raises: RasPy.ObjectDisposedException if this instance has been
        disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Gpio")

        self.__state = ps

    def pulse(self, millis):
        """Pulse the pin output for the specified number of milliseconds.

        :param millis: The number of milliseconds to wait between states.
        :type millis: int, long
        :raises: RasPy.ObjectDisposedException if this instance has been
        disposed.
        """
        if not isinstance(millis, (int, long)):
            millis = 0

        if self.is_disposed:
            raise ObjectDisposedException("Gpio")

        seconds = 0
        if millis > 0:
            seconds = millis / 1000

        self.write(PinState.HIGH)
        time.sleep(seconds)
        self.write(PinState.LOW)

    def read(self):
        """Read a value from the pin.

        :returns: The state (value) of the pin.
        :rtype: int
        :raises: RasPy.ObjectDisposedException if this instance has been
        disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Gpio")

        return PinState.LOW

    def on_pin_state_change(self, psce):
        """Fire the pin state change event.

        :param psce: The event object.
        :type psce: RasPy.IO.PinStateChangeEvent
        :raises: RasPy.ObjectDisposedException if this instance is disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Gpio")

        # Emit on a seperate thread here? Or maybe just do that from within
        # emit() itself.
        self.emit(EVENT_GPIO_STATE_CHANGED, psce)

    @property
    def revision(self):
        """Get the board revision.

        :returns: The board revision.
        :rtype: int
        """
        return self.__revision

    @property
    def state(self):
        """Get the state of the pin.

        :returns: The pin state.
        :rtype: int
        :raises: RasPy.ObjectDisposedException if this instance has been
        disposed.
        """
        self.__state = self.read()
        return self.__state

    @property
    def inner_pin(self):
        """Get the physical pin being represented by this instance.

        :returns: The underlying physical pin.
        :rtype: RasPy.IO.GpioPins
        """
        return self.__pin

    def provision(self):
        """Provision this pin.

        :raises: RasPy.ObjectDisposedException if this instance has been
        disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Gpio")

        self.write(self.__initValue)

    @property
    def mode(self):
        """Get the pin mode.

        :returns: The pin mode.
        :rtype: int
        """
        return self.__mode

    @mode.setter
    def mode(self, m):
        """Set the pin mode.

        :param m: The pin mode to set.
        :type m: int
        :raises: RasPy.ObjectDisposedException if this instance has been
        disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("Gpio")

        if m is None:
            m = PinMode.TRI

        if self.__mode != m:
            self.__mode = m
            self.provision()

    @property
    def address(self):
        """Get the pin address.

        :returns: The pin address.
        :rtype: int
        """
        return self.__pin.value

    def change_board_revision(self, revision):
        """Change the board revision.

        :param revision: The board revision.
        :type revision: int
        """
        if revision is None or not isinstance(revision, (int, long)):
            revision = BoardRevision.REV2

        self.__revision = revision

    def __get_initial_pin_value(self):
        """Get the initial pin value.

        :returns: The initial pin value.
        :rtype: int
        """
        return self.__initValue

    @property
    def pwm(self):
        """Get the PWM (pulse-width modulation) value.

        :returns: The PWM value.
        :rtype: int
        """
        return 0

    @pwm.setter
    def pwm(self, val):
        """Set the PWM (pulse-width modulation) value.

        :param val: The PWM value.
        :type val: int
        """
        pass

    @property
    def pwm_range(self):
        """Get the PWM (pulse-width modulation) range.

        :returns: The PWM range.
        :rtype: int
        """
        return 0

    @pwm_range.setter
    def pwm_range(self, rng):
        """Set the PWM (pulse-width modulation) range.

        :param range: The PWM range.
        :type range: int
        """
        pass

    def dispose(self):
        """Dispose managed resources.

        In a subclass, performs application-defined tasks associated with
        freeing, releasing, or resetting resources.
        """
        if self.is_disposed:
            return

        self.__emitter.remove_all_listeners()
        self.__emitter = None
        self.__state = None
        self.__mode = None
        self.__pin = None
        self.__initValue = None
        super(Gpio, self).dispose()
