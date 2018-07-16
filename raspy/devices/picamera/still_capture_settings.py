"""This module contains the StillCaptureSettings type."""


import os
from raspy import size
from raspy.illegal_argument_exception import IllegalArgumentException
from raspy.devices.picamera import capture_utils
from raspy.devices.picamera import image_encoding
from raspy.io.file_info import FileInfo


DEFAULT_IMG_SIZE_W = 640
"""The default image width (640px)."""

DEFAULT_IMG_SIZE_H = 480
"""The default image height (480)."""

QUALITY_MIN = 0
"""The minimum quality value (0)."""

QUALITY_MAX = 100
"""The maximum quality value (100)."""

QUALITY_DEFAULT = 75
"""The default quality value (75)."""

TIMEOUT_DEFAULT = 5000
"""The default timeout value (5 seconds)."""


class StillCaptureSettings(object):
    """Still capture image settings."""

    def __init__(self):
        """Initialize a new instance of StillCaptureSettings."""
        self.__quality = QUALITY_DEFAULT
        self.__size = size.Size(DEFAULT_IMG_SIZE_W, DEFAULT_IMG_SIZE_H)
        self.__timeout = TIMEOUT_DEFAULT
        self.__timeLapseInterval = 0
        self.__verbose = False
        self.__raw = False
        self.__fullPreview = False
        self.__encoding = image_encoding.JPEG
        self.__outputFile = None

    @property
    def image_size(self):
        """Get the size of the image. Default is 640x480.

        :returns: The image size.
        :rtype: raspy.size.Size
        """
        return self.__size

    @image_size.setter
    def image_size(self, img_size):
        """Set the size of the image.

        :param raspy.size.Size img_size: The image size.
        :raises: IllegalArgumentException if img_size is not of type
        `raspy.size.Size`.
        """
        if type(img_size) != size.Size:
            msg = "img_size property must be of type raspy.size.Size"
            raise IllegalArgumentException(msg)

        self.__size = img_size

    @property
    def timeout(self):
        """Get the timeout in milliseconds.

        This is the time to elapse before capture and shutdown. Default is
        TIMEOUT_DEFAULT.

        :returns: The capture timeout.
        :rtype: int
        """
        return self.__timeout

    @timeout.setter
    def timeout(self, millis):
        """Set the timeout in milliseconds.

        :param int millis: The capture timeout.
        :rtype: int
        """
        self.__timeout = millis

    @property
    def time_lapse_interval(self):
        """Get the time lapse interval. Default is zero (disabled).

        :returns: The time lapse interval.
        :rtype: int
        """
        return self.__timeLapseInterval

    @time_lapse_interval.setter
    def time_lapse_interval(self, interval):
        """Set the time lapse interval.

        :param int interval: The time lapse interval in milliseconds.
        """
        self.__timeLapseInterval = interval

    @property
    def verbose(self):
        """Get a value indicating whether or not the process will be verbose.

        Default is False.

        :returns: True if verbose.
        :rtype: bool
        """
        return self.__verbose

    @verbose.setter
    def verbose(self, be_verbose=False):
        """Set a value indicating whether or not the process will be verbose.

        :param bool be_verbose: Set True to enable verbosity.
        """
        self.__verbose = be_verbose

    @property
    def raw(self):
        """Get whether or not to add raw Bayer data to the JPEG metadata.

        This option inserts the raw Bayer data into the JPEG metadata if the
        encoding property is set ti image_encoding.JPEG. Default is False.

        :returns: When set True, will add raw Bayer data.
        :rtype: bool
        """
        return self.__raw

    @raw.setter
    def raw(self, flag=False):
        """Set a flag indicating whether or not to add raw Bayer data to meta.

        :param bool flag: Set True to add raw Bayer data.
        """
        self.__raw = flag

    @property
    def full_preview(self):
        """Get a flag indicating whether or not to enable full preview mode.

        This runs the preview windows using the full resolution capture mode.
        Maximum frames-per-second in this mode is 15fps and the preview will
        have the same field of view as the capture. Captures should happen
        more quickly as no mode change should be required.

        :returns: True if full preview mode is enabled.
        :rtype: bool
        """
        return self.__fullPreview

    @full_preview.setter
    def full_preview(self, flag=False):
        """Set a flag indicating whether or not to enable full preview mode.

        This runs the preview windows using the full resolution capture mode.
        Maximum frames-per-second in this mode is 15fps and the preview will
        have the same field of view as the capture. Captures should happen
        more quickly as no mode change should be required.

        :param bool flag: Set True to enable.
        """
        self.__fullPreview = flag

    @property
    def encoding(self):
        """Get the still image capture encoding format.

        :returns: The image encoding.
        :rtype: int
        """
        return self.__encoding

    @encoding.setter
    def encoding(self, enc):
        """Set the still image capture encoding format.

        :param int enc: The image encoding.
        """
        self.__encoding = enc

    @property
    def output_file(self):
        """Get the output file the image will be captured to.

        :returns: The output file to capture to.
        :rtype: FileInfo
        """
        return self.__outputFile

    @output_file.setter
    def output_file(self, out_file):
        """Set the output file the image will be captured to.

        :param FileInfo out_file: The output file.
        :raises: IllegalArgumentException if out_file is not of type FileInfo.
        """
        if type(out_file) != FileInfo:
            msg = "out_file must be of type raspy.io.file_info.FileInfo"
            raise IllegalArgumentException(msg)

        self.__outputFile = out_file

    @property
    def image_quality(self):
        """Get the image quality.

        :returns: The image quality level.
        :rtype: int
        """
        return self.__quality

    @image_quality.setter
    def image_quality(self, quality):
        """Set the image quality.

        :param int quality: The image quality level.
        :raises: IllegalArgumentException if the quality level is not a value
        between QUALITY_MIN and QUALITY_MAX.
        """
        if quality < QUALITY_MIN or quality > QUALITY_MAX:
            msg = "Quality value out of range."
            raise IllegalArgumentException(msg)

        self.__quality = quality

    def to_argument_string(self):
        """Convert this instance to a string of arguments that can be passed.

        :returns: The argument string.
        :rtype: str
        """
        fname = ""
        if self.output_file is not None:
            fname = self.output_file.get_filename_without_extension()

        args = ""
        if self.image_size != size.EMPTY:
            args += " --width " + str(self.image_size.width)
            args += " --height " + str(self.image_size.height)

        args += " --quality " + str(self.image_quality)
        if self.timeout > 0:
            args += " --timeout " + str(self.timeout)

        if self.time_lapse_interval > 0:
            args += " --timelapse " + str(self.time_lapse_interval)
            fname += "_%04d"

        fname += "." + capture_utils.get_encoding_file_extension(self.encoding)
        fname = os.path.join(self.output_file.get_directory_name(), fname)
        self.output_file = FileInfo(fname)
        args += ' --output "' + self.output_file.get_fullname() + '"'

        if self.verbose:
            args += " --verbose"

        args += " --encoding " + self.output_file.get_file_extension()
        if self.full_preview:
            args += " --fullpreview"

        return args
