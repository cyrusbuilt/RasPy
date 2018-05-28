"""A file object.

FileInfo.py

Author:
      Chris Brunner <cyrusbuilt at gmail dot com>

  Copyright (c) 2015 CyrusBuilt

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


import os
from RasPy import StringUtils
from RasPy.ArgumentNullException import ArgumentNullException
from RasPy.IO.IOException import IOException


class FileInfo(object):
    """A file object.

    This represents a file specifically, and not a directory or other
    container.
    """

    def __init__(self, filePath):
        """Initialize a new instance of RasPy.IO.FileInfo.

        Initializes a new instance of the FileInfo class with the
        fully-qualified or relative name of the file.

        :param filePath: The fully-qualified name of the of the file, or the
        relative file name.
        :type filePath: string
        :raises: RaPy.ArgumentNullException if filePath is null or an empty
        string.
        """
        if StringUtils.is_null_or_empty(filePath):
            raise ArgumentNullException("'filePath' param cannot be null or " +
                                        "undefined.")

        self.__name = os.path.basename(filePath)
        self.__originalPath = filePath
        self.__fullPath = os.path.normpath(self.__originalPath)

    def __str__(self):
        """Return the path as a string.

        :returns: A string representing the path.
        :rtype: string
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
        :rtype: string
        """
        head, tail = os.path.split(self.__fullPath)
        return head

    def get_file_name(self):
        """Get the file name.

        :returns: The file name component of the full file path.
        :rtype: bool
        """
        head, tail = os.path.split(self.__fullPath)
        return tail

    def get_file_extension(self):
        """Get the file extension name.

        :returns: The file extension (ie. "txt" or "pdf")
        :rtype: string
        """
        root, ext = os.path.splitext(self.__name)
        return ext

    def delete(self):
        """Delete this file.

        :raises: RasPy.IO.IOException if an error occurred while trying to
        delete the file (such as if the file does not exist).
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
        :retype: string
        """
        extLen = len(self.get_file_extension())
        return self.__name[0:len(self.__name) - extLen]

    def get_fullname(self):
        """Get the full file name path (dir + name + extension).

        :returns: The full file path.
        :rtype: string
        """
        return self.__fullPath
