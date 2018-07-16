"""This module contains the PiCameraDevice type."""


import sys
import threading
from Queue import Queue, Empty
from pyee import EventEmitter
from subprocess import Popen, PIPE
from raspy.object_disposed_exception import ObjectDisposedException
from raspy.devices.device import Device
from raspy.devices.picamera.events import CaptureDoneEvent
from raspy.devices.picamera.events import CaptureOutputEvent
from raspy.devices.picamera.events import CaptureStartEvent
from raspy.devices.picamera.still_capture_settings import StillCaptureSettings
from raspy.pi_system import core_utils


EVENT_CAPTURE_START = "captureStartEvent"
"""The name of the capture start event."""

EVENT_CAPTURE_DONE = "captureDoneEvent"
"""The name of the capture done event."""

EVENT_CAPTURE_OUTPUT = "captureOutputEvent"
"""The name of the capture output event."""


class PiCameraDevice(Device):
    """An abstraction of the RaspiCam device.

    RaspiCam is a peripheral camera device designed specifically for use with
    the Raspberry Pi. This class provides a threaded wrapper around the
    raspistill utility and thus a means for still capture control. See
    http://www.raspberrypi.org/wp-content/uploads/2013/07/RaspiCam-Documentation.pdf
    for instructions on how to install and configure RaspiCam support.
    """

    def __init__(self, settings=None):
        """Initialize a new instance of PiCameraDevice.

        :param StillCaptureSettings settings: The image capture settings.
        """
        Device.__init__(self)
        self.__settings = settings
        self.__emitter = EventEmitter()
        self.__isRunning = False
        self.__processID = -1
        self.__exitCode = -1
        self.__captureProc = None
        self.__syncLock = threading.RLock()
        self.__captureThread = None

    def on(self, evt, callback):
        """Register an event with a callback to handle it.

        :param str evt: The name of the event to register a handler for.
        :param function callback: The callback to execute when the event
        fires.
        :raises: ObjectDisposedException if this instance is disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("PiCameraDevice")

        self.__emitter.on(evt, callback)

    def emit(self, evt, args):
        """Emit the specified event to all registered listeners.

        :param str evt: The name of the event to emit.
        :param object args: The arguments to pass to the event handlers
        (listeners).
        :raises: ObjectDisposedException if this instance is disposed.
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

    @property
    def capture_settings(self):
        """Get the still capture settings.

        :returns: The still capture settings.
        :rtype: StillCaptureSettings
        """
        return self.__settings

    @capture_settings.setter
    def capture_settings(self, settings):
        """Set the still capture settings.

        :param StillCaptureSettings settings: The capture settings.
        """
        self.__settings = settings

    @property
    def process_id(self):
        """Get the process ID.

        :returns: The ID of the capture process if started;
        Otherwise, -1.
        :rtype: int
        """
        return self.__processID

    @property
    def is_running(self):
        """Get whether or not the capture process is running.

        :returns: True if running.
        :rtype: bool
        """
        return self.__isRunning

    @property
    def exit_code(self):
        """Get the exit code of the capture process.

        :returns: The process exit code if terminated normally;
        Otherwise, -1.
        """
        return self.__exitCode

    def on_capture_started(self, start_evt):
        """Fire the capture started event.

        :param CaptureStartEvent start_evt: The event object.
        :raises: ObjectDisposedException if this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("PiCameraDevice")

        _t = threading.Thread(target=self.emit,
                              name=EVENT_CAPTURE_START,
                              args=(EVENT_CAPTURE_START, start_evt))
        _t.daemon = True
        _t.start()

    def on_capture_output_received(self, out_evt):
        """Fire the capture output event.

        :param CaptureOutputEvent out_evt: The event object.
        :raises: ObjectDisposedException if this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("PiCameraDevice")

        _t = threading.Thread(target=self.emit,
                              name=EVENT_CAPTURE_OUTPUT,
                              args=(EVENT_CAPTURE_OUTPUT, out_evt))
        _t.daemon = True
        _t.start()

    def on_capture_done(self, done_evt):
        """Fire the capture done event.

        :param CaptureDoneEvent done_evt: The event object.
        :raises: ObjectDisposedException if this instance has been disposed.
        """
        if self.is_disposed:
            raise ObjectDisposedException("PiCameraDevice")

        _t = threading.Thread(target=self.emit,
                              name=EVENT_CAPTURE_DONE,
                              args=(EVENT_CAPTURE_DONE, done_evt))
        _t.daemon = True
        _t.start()

    def cancel(self):
        """Cancel the still capture process, if running.

        Should emit EVENT_CAPTURE_DONE and include the termination signal.
        """
        if not self.__isRunning:
            return

        self.__syncLock.acquire()
        self.__isRunning = False
        self.__syncLock.release()
        core_utils.sleep(500)
        if self.__captureProc is not None:
            if self.__captureProc.poll() is not None:
                try:
                    self.__captureProc.kill()
                except OSError:
                    # Process probably already died.
                    pass

    @staticmethod
    def _enqueue_output(out, queue):
        """Enqueue output from the process.

        :param File out: The standard output stream from the process.
        :param Queue queue: The queue to store the output lines in.
        """
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()

    def _monitor_capture(self):
        """Monitor the capture process."""
        if self.__settings is None:
            self.__settings = StillCaptureSettings()

        args = self.__settings.to_argument_string()
        cmd = ['raspistill'] + args.split(" ")

        # start the process and get the PID.
        on_posix = 'posix' in sys.builtin_module_names
        self.__captureProc = Popen(cmd, stdout=PIPE, stderr=PIPE, bufsize=1, close_fds=on_posix)
        read_queue = Queue()
        enqueue_args = (self.__captureProc.stdout, read_queue)
        queue_thread = threading.Thread(target=PiCameraDevice._enqueue_output, args=enqueue_args)
        queue_thread.daemon = True
        queue_thread.start()
        self.__syncLock.acquire()
        self.__processID = self.__captureProc.pid
        self.__syncLock.release()

        # Notify listeners that the process started and start signaling output.
        self.on_capture_started(CaptureStartEvent(self.__processID))
        while self.__captureProc.poll() is None:
            try:
                line = read_queue.get_nowait()
            except Empty:
                pass
            else:
                self.on_capture_output_received(CaptureOutputEvent(line))

        # The process finished. Get the exit code.
        self.__syncLock.acquire()
        self.__exitCode = self.__captureProc.returncode
        self.__isRunning = False
        self.__syncLock.release()

        # Notify listeners that the process finished.
        self.on_capture_done(CaptureDoneEvent(self.__exitCode))

    def start(self):
        """Start the capture process on a separate thread.

        This method immediately returns and the process continues in the
        background firing events as they occur.
        """
        if self.is_running:
            return

        self.__processID = -1
        self.__exitCode = 0
        self.__captureThread = threading.Thread(target=self._monitor_capture)
        self.__captureThread.name = "raspistillMonitor"
        self.__captureThread.daemon = True
        self.__captureThread.start()
        self.__isRunning = True

    def dispose(self):
        """Release managed resources used by this component."""
        if self.is_disposed:
            return

        self.cancel()
        self.__captureThread = None
        self.__exitCode = 0
        self.__processID = -1
        self.__syncLock = None
        self.__captureProc = None
        self.__settings = None
        self.__emitter.remove_all_listeners()
        self.__emitter = None
        Device.dispose(self)
