"""Test all ExecUtils methods."""

import platform
from RasPy import StringUtils
from RasPy import ExecUtils


def test_execute_command():
    """Test execute_command method."""
    cmd = "ping -c 1 127.0.0.1"
    text = "bytes from"
    if platform.system() == "Windows":
        cmd = "ping -n 1 127.0.0.1"
        text = "Reply from 127.0.0.1"

    newline = '\n'
    result = ExecUtils.execute_command(cmd)
    outputstr = newline.join(result)
    assert StringUtils.contains(outputstr, text)
