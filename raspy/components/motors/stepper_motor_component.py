"""This module contains the StepperMotorComponent type."""


import threading
from raspy.argument_null_exception import ArgumentNullException
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.motors import motor_state
from raspy.components.motors.motor_rotate_event import MotorRotateEvent
from raspy.components.motors.motor_state_change_event import MotorStateChangeEvent
from raspy.components.motors.stepper_motor import StepperMotor
from raspy.io import pin_state
from raspy.pi_system import core_utils


class StepperMotorComponent(StepperMotor):
    """A component that is an abstraction of a stepper motor."""

    def __init__(self, pins):
        """Initialze a new instance of StepperMotorComponent.

        :param list pins: The output pins for each controller in the stepper
        motor. This should be a list of `rapsy.io.gpio.Gpio` (or derivative)
        objects.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        'pins' is None or zero-length.
        """
        StepperMotor.__init__(self)
        if pins is None or len(pins) == 0:
            msg = "'pin' param cannot be None or zero-length."
            raise ArgumentNullException(msg)

        self.__sequenceIndex = 0
        self.__controlThread = None
        self.__stopEvent = threading.Event()
        self.__lock = threading.Lock()
        self.__stopEvent.set()
        self.__pins = pins
        for _p in self.__pins:
            _p.provision()

    def _kill_control_thread(self):
        """Stop the continuous movement thread."""
        if self.is_disposed:
            return
        if self.__stopEvent.is_set() or self.__controlThread is None:
            return
        self.__stopEvent.set()

    def _do_step(self, forward=True):
        """Step the motor forward or backward.

        :param bool forward: Set True if moving forward.
        """
        if forward:
            self.__sequenceIndex += 1
        else:
            self.__sequenceIndex -= 1

        # Check sequence bounds; rollover if needed.
        seq = self.step_sequence
        if self.__sequenceIndex >= len(seq):
            self.__sequenceIndex = 0
        elif self.__sequenceIndex < 0:
            self.__sequenceIndex = len(seq) - 1

        # Start cycling through GPIO pins to move the motor forward or reverse.
        for i in range(0, len(self.__pins) - 1):
            nib = pow(2, i)
            if (seq[self.__sequenceIndex] & int(nib)) > 0:
                self.__pins[i].write(pin_state.HIGH)
            else:
                self.__pins[i].write(pin_state.LOW)

        millis = self.step_interval_millis
        nanos = self.step_interval_nanos
        micros = (millis + (nanos * 1000000)) * 1000
        core_utils.sleep_microseconds(micros)

    def _async_exec_movement(self):
        """Helper method for executing or ending movement."""
        # Continuous loop until stopped.
        while self.state != motor_state.STOP:
            self._do_step(self.state == motor_state.FORWARD)

        # Turn all GPIO pins off.
        for _p in self.__pins:
            _p.write(pin_state.LOW)

    def _execute_movement(self):
        """Asynchronously executes or ends movement based on motor state."""
        with self.__lock:
            if self.state == motor_state.STOP:
                for _p in self.__pins:
                    _p.write(pin_state.LOW)
                return

        self.__stopEvent.clear()
        self.__controlThread = threading.Thread(target=self._async_exec_movement)
        self.__controlThread.name = "motorMovementExec"
        self.__controlThread.daemon = True
        self.__controlThread.start()

    @property
    def state(self):
        """Get the motor state.

        :returns: The motor state.
        :rtype: int
        """
        return StepperMotor.state.fget()

    @state.setter
    def state(self, mot_state):
        """Set the motor state.

        :param int mot_state: The motor state.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("StepperMotorComponent")

        old_state = self.state
        if self.state != mot_state:
            self.state = mot_state
            evt = MotorStateChangeEvent(old_state, mot_state)
            self.on_motor_state_change(evt)
            self._execute_movement()

    def stop(self):
        """Stop the motor's movement."""
        for _p in self.__pins:
            _p.write(pin_state.LOW)
        StepperMotor.stop(self)

    def step(self, steps):
        """Step the motor the specified number of steps.

        :param int steps: The number or steps to rotate.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("StepperMotorComponent")

        if steps == 0:
            self.state = motor_state.STOP
            return

        # Perform step in positive or negative direction from current position.
        StepperMotor.step(self, steps)
        evt = MotorRotateEvent(steps)
        self.on_rotation_started(evt)
        if steps > 0:
            for _i in range(0, steps):
                self._do_step(True)
        else:
            for _j in range(steps, 0):
                self._do_step(False)

        # Stop movement.
        self.stop()
        self.on_rotation_stopped()

    def dispose(self):
        """Dispose managed resources."""
        if self.is_disposed:
            return

        self.state = motor_state.STOP
        self._kill_control_thread()
        self.__sequenceIndex = 0
        self.__controlThread = None
        self.__stopEvent = None
        self.__controlThread = None
        if self.__lock.locked():
            self.__lock.release()
        self.__lock = None
        if self.__pins is not None and len(self.__pins) > 0:
            for _p in self.__pins:
                _p.write(pin_state.LOW)
                _p.dispose()
        self.__pins = None
        StepperMotor.dispose(self)
