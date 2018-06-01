"""Test all ExecUtils methods."""

import platform
from raspy import string_utils
from raspy import exec_utils


def test_execute_command():
    """Test execute_command method."""
    cmd = "ping -c 1 127.0.0.1"
    text = "bytes from"
    if platform.system() == "Windows":
        cmd = "ping -n 1 127.0.0.1"
        text = "Reply from 127.0.0.1"

    newline = '\n'
    result = exec_utils.execute_command(cmd)
    # noinspection PyTypeChecker
    output_str = newline.join(result)
    assert string_utils.contains(output_str, text)
