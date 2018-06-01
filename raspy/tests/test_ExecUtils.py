"""Test all ExecUtils methods."""

import platform
from raspy import string_utils
from raspy import exec_utils


def test_execute_command():
    """Test execute_command method."""
    cmd = 'echo "Hello World!"'
    text = "Hello"
    if platform.system() == "Windows":
        cmd = "echo Hello World!"

    newline = '\n'
    result = exec_utils.execute_command(cmd)
    # noinspection PyTypeChecker
    output_str = newline.join(result)
    print("DEBUG: " + output_str)
    assert string_utils.contains(output_str, text)
