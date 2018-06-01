"""This module provides a File object."""


import os
from raspy import string_utils
from raspy.argument_null_exception import ArgumentNullException
from raspy.io.io_exception import IOException


class FileInfo(object):
    """A file object.

    This represents a file specifically, and not a directory or other
    container.
    """

    def __init__(self, file_path):
        """Initialize a new instance of raspy.io.file_info.FileInfo.

        Initializes a new instance of the FileInfo class with the
        fully-qualified or relative name of the file.

        :param str file_path: The fully-qualified name of the of the file,
        or the relative file name.
        :raises: raspy.argument_null_exception.ArgumentNullException if
        file_path is null or an empty string.
        """
        if string_utils.is_null_or_empty(file_path):
            raise ArgumentNullException("'file_path' param cannot be null or " +
                                        "undefined.")

        self.__name = os.path.basename(file_path)
        self.__originalPath = file_path
        self.__fullPath = os.path.normpath(self.__originalPath)

    def __str__(self):
        """Return the path as a string.

        :returns: A string representing the path.
        :rtype: str
        """
        return self.__originalPath

    def exists(self):
        """Check to see if this file exists.

        :returns: True if exists; Otherwise, false.
        :rtype: bool
        """
        return os.path.exists(self.__fullPath)

    def get_directory_name(self):
        """Get the directory name (path) the file is in.

        :returns: The directory component of the full file path.
        :rtype: str
        """
        head, tail = os.path.split(self.__fullPath)
        return head

    def get_file_name(self):
        """Get the file name.

        :returns: The file name component of the full file path.
        :rtype: str
        """
        head, tail = os.path.split(self.__fullPath)
        return tail

    def get_file_extension(self):
        """Get the file extension name.

        :returns: The file extension (ie. "txt" or "pdf")
        :rtype: str
        """
        root, ext = os.path.splitext(self.__name)
        return ext

    def delete(self):
        """Delete this file.

        :raises: raspy.io.io_exception.IOException if an error occurred while
        trying to delete the file (such as if the file does not exist).
        """
        try:
            if self.exists():
                os.remove(self.__fullPath)
        except OSError as ex:
            raise IOException(ex.strerror)

    def get_length(self):
        """Get the file size in bytes.

        :returns: The file size in bytes if it exists; Otherwise, zero. May
        also return zero if this is a zero byte file.
        :rtype: int
        """
        if not self.exists():
            return 0

        return os.path.getsize(self.__fullPath)

    def get_filename_without_extension(self):
        """Get the file name, without the file extension.

        :returns: The file name without file extension.
        :rtype: str
        """
        ext_len = len(self.get_file_extension())
        return self.__name[0:len(self.__name) - ext_len]

    def get_fullname(self):
        """Get the full file name path (dir + name + extension).

        :returns: The full file path.
        :rtype: str
        """
        return self.__fullPath
