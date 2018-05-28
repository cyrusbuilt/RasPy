"""Tests for RasPy.IO.FileInfo class."""

import os
from RasPy.IO.FileInfo import FileInfo


filePath = os.tempnam() + ".txt"


def make_file():
    if not os.path.exists(filePath):
        fd = os.open(filePath, os.O_WRONLY | os.O_CREAT)
        os.close(fd)
        print "Created " + filePath


def del_file():
    if os.path.exists(filePath):
        try:
            os.remove(filePath)
            print "Removed " + filePath
        except OSError:
            pass


class TestFileInfo(object):
    """Test FileInfo class methods."""

    def test__str__(self):
        """Test __str__ method."""
        f = FileInfo(filePath)
        expected = filePath
        actual = f.__str__()
        assert expected == actual

    def test_exists(self):
        """Test exists method."""
        make_file()
        f = FileInfo(filePath)
        assert f.exists()
        del_file()

    def test_get_directory_name(self):
        """Test get_directory_name method."""
        f = FileInfo(filePath)
        head, tail = os.path.split(filePath)
        expected = head
        actual = f.get_directory_name()
        assert actual == expected

    def test_get_file_name(self):
        """Test get_file_name method."""
        f = FileInfo(filePath)
        head, tail = os.path.split(filePath)
        expected = tail
        actual = f.get_file_name()
        assert actual == expected

    def test_get_file_extension(self):
        """Test get_file_extension method."""
        f = FileInfo(filePath)
        root, ext = os.path.splitext(filePath)
        expected = ext
        actual = f.get_file_extension()
        assert actual == expected

    def test_delete(self):
        """Test delete method."""
        make_file()
        f = FileInfo(filePath)
        f.delete()

        assert not f.exists()

    def test_get_length(self):
        """Test get_length method."""
        f = FileInfo(filePath)
        assert f.get_length() == 0

    def test_get_filename_without_extension(self):
        """Test get_filename_without_extension method."""
        f = FileInfo(filePath)
        head, tail = os.path.split(filePath)  # Get just the file name.
        root, ext = os.path.splitext(tail)    # Now get name without ext.
        expected = root
        actual = f.get_filename_without_extension()
        assert actual == expected

    def test_get_fullname(self):
        """Test get_fullname method."""
        f = FileInfo(filePath)
        expected = filePath
        actual = f.get_fullname()
        assert actual == expected
