"""Provides utility methods for executing child processes and getting output."""

from subprocess import Popen, PIPE
from raspy import string_utils


def execute_command(command):
    """Execute the specified command.

    Executes the specified command and returns the output.

    :param command: The command to execute.
    :type command: str
    :returns: A string array containing each line of the output.
    :rtype: list
    """
    if string_utils.is_null_or_empty(command):
        return []

    args = string_utils.EMPTY
    cmd_line = command.split(" ")
    if len(cmd_line) > 1:
        command = cmd_line[0]
        for i in range(1, len(cmd_line)):
            args += cmd_line[i] + " "

        if string_utils.ends_with(args, " "):
            args = args[0:len(args) - 1]

    result = []
    cmd = [command] + args.split(" ")
    cmd_spawn = Popen(cmd, stdout=PIPE, stderr=PIPE)
    output, err = cmd_spawn.communicate()
    if cmd_spawn.returncode == 0:
        for line in output.strip().split("\n"):
            result.append(line)

    if err:
        # TODO should we do anything with this? # pylint: disable=fixme
        pass

    return result
