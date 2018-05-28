"""Provides utility methods for executing child processes and getting output.

ExecUtils.py

Author:
      Chris Brunner <cyrusbuilt at gmail dot com>

  Copyright (c) 2017 CyrusBuilt

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

from subprocess import Popen, PIPE
from RasPy import StringUtils


def execute_command(command):
    """Execute the specified command.

    Executes the specified command and returns the output.

    :param command: The command to execute.
    :type command: string
    :returns: A string array containing each line of the output.
    :rtype: array
    """
    if StringUtils.is_null_or_empty(command):
        return []

    args = StringUtils.EMPTY
    cmdLine = command.split(" ")
    if len(cmdLine) > 1:
        command = cmdLine[0]
        for i in range(1, len(cmdLine)):
            args += cmdLine[i] + " "

        if StringUtils.ends_with(args, " "):
            args = args[0:len(args) - 1]

    result = []
    cmd = [command] + args.split(" ")
    cmdSpawn = Popen(cmd, stdout=PIPE, stderr=PIPE)
    output, err = cmdSpawn.communicate()
    if cmdSpawn.returncode == 0:
        for line in output.strip().split("\n"):
            result.append(line)

    return result
