"""Tests for PinUtils module."""


import os
from raspy.io import pin_mode
from raspy.io import pin_utils
from raspy.io.io_exception import IOException


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


def test_get_pin_mode_name():
    """Test the get_pin_mode_name method."""
    expected = "OUT"
    actual = pin_utils.get_pin_mode_name(pin_mode.OUT)
    assert actual == expected


def test_write_fs_pin():
    """Test the write_fs_pin method."""
    make_file()
    success = True
    try:
        pin_utils.write_fs_pin(filePath, "test")
    except IOException:
        success = False

    assert success
    del_file()


def test_read_fs_pin():
    """Test the read_fs_pin method."""
    target = open(filePath, 'w')
    target.write(str(0))
    target.close()

    make_file()
    expected = 0
    actual = pin_utils.read_fs_pin(filePath)
    assert actual == expected
    del_file()
