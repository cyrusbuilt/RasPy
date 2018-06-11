"""This module contains the StepperMotor type."""


import threading
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.components.motors import motor_state
from raspy.components.motors.motor import Motor
from raspy.components.motors.motor_rotate_event import MotorRotateEvent


EVENT_ROTATION_STARTED = "stepperMotorRotationStarted"
"""The event the fires when motor rotation starts."""

EVENT_ROTATION_STOPPED = "stepperMotorRotationStopped"
"""The event that fires when motor rotation stops."""


class StepperMotor(Motor):
    """A stepper motor abstraction base type."""

    def __init__(self):
        """Initialize a new instance of StepperMotor."""
        Motor.__init__(self)
        self.__stepIntervalMillis = 0
        self.__stepIntervalNanos = 0
        self.__stepSequence = list()
        self.__stepsPerRevolution = 0

    def dispose(self):
        """Dispose managed resources."""
        if self.is_disposed:
            return

        self.__stepSequence = None
        self.__stepsPerRevolution = 0
        self.__stepIntervalMillis = 0
        self.__stepIntervalNanos = 0
        Motor.dispose(self)

    def on_rotation_started(self, rotate_evt):
        """Fire the rotation start event.

        :param raspy.components.motors.motor_rotate_event.MotorRotateEvent rotate_evt:
        The motor rotation event info object.
        :raises: raspy.object_diposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("StepperMotor")

        _t = threading.Thread(target=self.emit,
                              name="stepperMotorRotation",
                              args=(EVENT_ROTATION_STARTED, rotate_evt))
        _t.daemon = True
        _t.start()

    def on_rotation_stopped(self):
        """Fire the rotation stopped event.

        :raises: raspy.object_diposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("StepperMotor")

        _t = threading.Thread(target=self.emit,
                              name="stepperMotorStop",
                              args=(EVENT_ROTATION_STOPPED, None))
        _t.daemon = True
        _t.start()

    @property
    def steps_per_revolution(self):
        """Get the number of steps per revolution.

        :returns: The steps per revolution.
        :rtype: int
        """
        return self.__stepsPerRevolution

    @steps_per_revolution.setter
    def steps_per_revolution(self, steps=0):
        """Set the number of steps per revolution.

        :param int steps: The steps per revolution.
        """
        self.__stepsPerRevolution = steps

    @property
    def step_sequence(self):
        """Get a list of bytes representing the step sequence.

        :returns: The step sequence.
        :rtype: list
        """
        return self.__stepSequence

    @step_sequence.setter
    def step_sequence(self, seq=[]):
        """Set the list of bytes representing the step sequence.

        :param list seq: The step sequence.
        """
        self.__stepSequence = seq

    def set_step_interval(self, millis, nanos):
        """Set the step interval.

        :param int millis: The milliseconds between steps.
        :param int nanos: The nanoseconds between steps.
        """
        self.__stepIntervalMillis = millis
        self.__stepIntervalNanos = nanos

    def rotate(self, revolutions):
        """Rotate for the specified number of revolutions.

        :param int revolutions: The number or revolutions to rotate.
        """
        steps = round(self.__stepsPerRevolution * revolutions)
        steps_actual = int(steps)
        evt = MotorRotateEvent(steps_actual)
        self.on_rotation_started(evt)
        self.step(steps_actual)
        self.on_rotation_stopped()

    def step(self, steps):
        """Step the motor the specified number of steps.

        :param int steps: The number or steps to rotate.
        :raises: raspy.object_disposed_exception.ObjectDisposedException if
        this instance has been disposed.
        """
        if steps == 0:
            self.state = motor_state.STOP
            return

        if steps < 0:
            self.state = motor_state.REVERSE
        elif steps > 0:
            self.state = motor_state.FORWARD

    @property
    def step_interval_millis(self):
        """Get the step interval in milliseconds.

        :returns: The step interval.
        :rtype: int
        """
        return self.__stepIntervalMillis

    @property
    def step_interval_nanos(self):
        """Get the step interval in nanoseconds.

        :returns: The step interval.
        :rtype: int
        """
        return self.__stepIntervalNanos
