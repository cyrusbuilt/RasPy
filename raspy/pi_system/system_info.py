"""
This module Provides methods for getting system-specific info.

This includes info about the host OS and the board it is running on.
"""


import platform
import re
import time
from raspy import exec_utils
from raspy import string_utils
from raspy.pi_system import board_type
from raspy.invalid_operation_exception import InvalidOperationException


__cpuInfo = None
"""Internal CPU info cache."""


def get_cpu_info(target):
    """Get information about the CPU.

    Returns the value from the specified target field.

    :param string target: The target attribute to the value of.
    :returns: The value of the specified CPU attribute.
    :rtype: string
    :raises: raspy.invalid_operation_exception.InvalidOperationException if
    the specified target is invalid (unknown).
    """
    global __cpuInfo
    if __cpuInfo is None:
        __cpuInfo = []
        result = exec_utils.execute_command("cat /proc/cpuinfo")
        if result is not None:
            # noinspection PyTypeChecker
            for key, val in enumerate(result):
                line = val
                parts = line.split(":")
                if len(parts) >= 2:
                    tpart0 = string_utils.trim(parts[0])
                    tpart1 = string_utils.trim(parts[1])
                    if (not string_utils.is_null_or_empty(tpart0) and
                            not string_utils.is_null_or_empty(tpart1)):
                        # noinspection PyTypeChecker
                        __cpuInfo[tpart0] = tpart1

    if target in __cpuInfo:
        # noinspection PyTypeChecker
        return __cpuInfo[target]

    raise InvalidOperationException("Invalid target: " + target)


def get_processor():
    """Get the processor.

    :returns: The processor.
    :rtype: string
    """
    return get_cpu_info("Processor")


def get_bogomips():
    """Get the Bogo MIPS.

    :returns: The Bogo MIPS.
    :rtype: string
    """
    return get_cpu_info("BogoMIPS")


def get_cpu_features():
    """Get the CPU features.

    :returns: The CPU features.
    :rtype: array
    """
    return get_cpu_info("Features").split()


def get_cpu_implementer():
    """Get the CPU implementer.

    :returns: The CPU implementer.
    :rtype: string
    """
    return get_cpu_info("CPU implementer")


def get_cpu_architecture():
    """Get the CPU architecture.

    :returns: The CPU architecture.
    :rtype: string
    """
    return get_cpu_info("CPU architecture")


def get_cpu_variant():
    """Get the CPU variant.

    :returns: The CPU variant.
    :rtype: string
    """
    return get_cpu_info("CPU variant")


def get_cpu_part():
    """Get the CPU part.

    :returns: The CPU part.
    :rtype: string
    """
    return get_cpu_info("CPU part")


def get_cpu_revision():
    """Get the CPU revision.

    :returns: The CPU revision.
    :rtype: string
    """
    return get_cpu_info("CPU revision")


def get_hardware():
    """Get the hardware the system is implemented on.

    :returns: The hardware.
    :rtype: string
    """
    return get_cpu_info("Hardware")


def get_system_revision():
    """Get the system revision.

    :returns: The system revision.
    :rtype: string
    """
    return get_cpu_info("Revision")


def get_serial():
    """Get the serial number.

    :returns: The serial number.
    :rtype: string
    """
    return get_cpu_info("Serial")


def get_os_name():
    """Get the name of the OS.

    :returns: The name of the OS.
    :rtype: string
    """
    return platform.system()


def get_os_version():
    """Get the OS version.

    :returns: The OS version.
    :rtype: string
    """
    return platform.release()


def get_os_arch():
    """Get the OS architecture.

    :returns: The OS architecture.
    :rtype: string
    """
    return platform.machine()


def get_os_firmware_build():
    """Get the OS firmware build.

    :returns: the OS firmware build.
    :rtype: string
    :raises: raspy.invalid_operation_exception.InvalidOperationException if
    an unexpected response is received.
    """
    results = exec_utils.execute_command("/opt/vc/bin/vcgencmd version")
    val = string_utils.EMPTY
    if results is not None:
        # noinspection PyTypeChecker
        for key, val in enumerate(results):
            line = val
            if string_utils.starts_with(line, "version "):
                val = line
                break

    if not string_utils.is_null_or_empty(val):
        return val[8:]

    raise InvalidOperationException("Invalid command or response")


def get_os_firmware_date():
    """Get the OS firmware date.

    :returns: The OS firmware date.
    :rtype: string
    :raises: raspy.invalid_operation_exception.InvalidOperationException if
    an unexpected response is received.
    """
    results = exec_utils.execute_command("/opt/vc/bin/vcgencmd version")
    val = string_utils.EMPTY
    if results is not None:
        # noinspection PyTypeChecker
        for key, value in enumerate(results):
            # We are intentionally only getting the first line.
            val = value
            break

    if not string_utils.is_null_or_empty(val):
        return val

    raise InvalidOperationException("Invalid command or response.")


def get_memory():
    """Get the system memory info.

    :returns: The memory info.
    :rtype: array
    """
    values = []
    result = exec_utils.execute_command("free -b")
    if result is not None:
        val = 0
        # noinspection PyTypeChecker
        for i, line in enumerate(result):
            if string_utils.starts_with(line, "Mem:"):
                parts = line.split()
                for j, part in enumerate(parts):
                    line_part = string_utils.trim(part)
                    if (not string_utils.is_null_or_empty(line_part)
                            and line.upper() == "Mem:".upper()):
                        values.append(float(val))

    return values


def get_memory_total():
    """Get the total amount of system memory.

    :returns: If successful, the total system memory; Otherwise, -1.
    :rtype: int, long
    """
    values = get_memory()
    # noinspection PyTypeChecker
    if values is not None and len(values) > 0:
        return values[0]  # Total memory value is the first position.

    return -1


def get_memory_used():
    """Get the amount of memory consumed.

    :returns: If successful, the amount of memory that is in use.
    :rtype: int, long
    """
    values = get_memory()
    # noinspection PyTypeChecker
    if values is not None and len(values) > 1:
        return values[1]  # Used memory value is the second position.

    return -1


def get_memory_free():
    """Get the free memory available.

    :returns: If successful, the amount of memory available; Otherwise, -1.
    :rtype: int, long
    """
    values = get_memory()
    # noinspection PyTypeChecker
    if values is not None and len(values) > 2:
        return values[2]  # Free memory value is the third position.

    return -1


def get_memory_shared():
    """Get the amount of shared memory.

    :returns: If successful, the shared memory; Otherwise, -1.
    :rtype: int, long
    """
    values = get_memory()
    # noinspection PyTypeChecker
    if values is not None and len(values) > 3:
        return values[3]  # Shared memory value is the fourth position.

    return -1


def get_memory_buffers():
    """Get the buffer memory.

    :returns: If successful, the buffer memory; Otherwise, -1
    :rtype: int, long
    """
    values = get_memory()
    # noinspection PyTypeChecker
    if values is not None and len(values) > 4:
        return values[4]  # Buffer memory value is the fifth position.

    return -1


def get_memory_cached():
    """Get the amount of cache memory.

    :returns: If successful, the cache memory; Otherwise, -1.
    :rtype: int, long
    """
    values = get_memory()
    # noinspection PyTypeChecker
    if values is not None and len(values) > 5:
        return values[5]  # Cache memory is the sixth position.

    return -1


def get_board_type():
    """Get the type of board the executing script is running on.

    :returns: The board type.
    :rtype: int
    """
    # The following info obtained from:
    # http://www.raspberrypi.org/archives/1929
    # http://raspberryalphaomega.org.uk/?p=428
    # http://www.raspberrypi.org/phpBB3/viewtopic.php?p=281039#281039

    bt = board_type.UNKNOWN
    rev = get_system_revision()
    if rev == "0002" or rev == "0003":
        # 0002 = Model B Rev 1
        # 0003 = Model B Rev 1 + Fuses mod and D14 removed.
        bt = board_type.MODELB_REV1
    elif (rev == "0004" or rev == "0005" or rev == "0006" or
            rev == "000d" or rev == "000e" or rev == "000f"):
        # 0004 = Model B Rev 2 256MB (Sony)
        # 0005 = Model B Rev 2 256MB (Qisda)
        # 0006 = Model B Rev 2 256MB (Egoman)
        # 000d = Model B Rev 2 512MB (Egoman)
        # 000e = Model B Rev 2 512MB (Sony)
        # 000f = Model B Rev 2 512MB (Qisda)
        bt = board_type.MODELB_REV2

    return bt


def get_cpu_temperature():
    """Get the CPU temperature.

    :returns: The CPU temperature.
    :rtype: int, long
    :raises: raspy.invalid_operation_exception.InvalidOperationException if
    invalid command ("measure_temp") or response.
    """
    # CPU temperature is in the form:
    # pi@mypi$ /opt/vc/bin/vcgencmd measure_temp
    # temp=42.3'C
    # Support for this was added around firmware version 3357xx per info
    # at http://www.raspberrypi.org/phpBB3/viewtopic.php?p=169909#p169909
    result = exec_utils.execute_command("/opt/vc/bin/vcgencmd measure_temp")
    if result is not None:
        val = -1
        separators = ["\\\[", "\\\=", "\\\]", "\\\'"]
        # noinspection PyTypeChecker
        for i, line in enumerate(result):
            parts = re.split('|'.join(map(re.escape, separators)), line)
            try:
                val = float(parts[1])
            except ValueError:
                val = -1

        return val

    raise InvalidOperationException("Invalid command or response.")


def get_voltage(id):
    """Get the voltage.

    :param string id: The ID of the voltage type to get (core, sdram_c, etc).
    :returns: The voltage.
    :rtype: int, long
    :raises: raspy.invalid_operation_exception.InvalidOperationException if
    invalid command ("measure_volts") or response.
    """
    cmd = "/opt/vc/bin/vcgencmd measure_volts " + id
    result = exec_utils.execute_command(cmd)
    if result is not None:
        val = -1
        separators = ["\\\[", "\\\=", "\\\V", "\\\]"]
        # noinspection PyTypeChecker
        for i, line in enumerate(result):
            parts = re.split('|'.join(map(re.escape, separators)), line)
            try:
                val = float(parts[1])
            except ValueError:
                val = -1

        return val

    raise InvalidOperationException("Invalid command or response.")


def get_cpu_voltage():
    """Get the CPU voltage.

    :returns: The CPU voltage.
    :rtype: int, long
    :raises: raspy.invalid_operation_exception.InvalidOperationException if
    invalid command ("measure_volts") or response.
    """
    return get_voltage("core")


def get_memory_voltage_sdram_c():
    """Get the memory voltage of SDRAM C.

    :returns: The memory voltage of SDRAM C.
    :rtype: int, long
    :raises: raspy.invalid_operation_exception.InvalidOperationException if
    invalid command ("measure_volts") or response.
    """
    return get_voltage("sdram_c")


def get_memory_voltage_sdram_i():
    """Get the memory voltage of SDRAM I.

    :returns: The memory voltage of SDRAM I.
    :rtype: int, long
    :raises: raspy.invalid_operation_exception.InvalidOperationException if
    invalid command ("measure_volts") or response.
    """
    return get_voltage("sdram_i")


def get_memory_votage_sdram_p():
    """Get the memory voltage of SDRAM P.

    :returns: The memory voltage of SDRAM P.
    :rtype: int, long
    :raises: raspy.invalid_operation_exception.InvalidOperationException if
    invalid command ("measure_volts") or response.
    """
    return get_voltage("sdram_p")


def get_codec_enabled(codec):
    """Get whether or not the specified codec is enabled.

    :param codec: The codec to get.
    :type codec: string
    :returns: true if the specified codec is enabled; Otherwise, false.
    :rtype: boolean
    :raises: raspy.InvalidOperationException if invalid command
    ("codec_enabled") or response.
    """
    enabled = False
    cmd = "/opt/vc/bin/vcgencmd codec_enabled " + codec
    result = exec_utils.execute_command(cmd)
    if result is not None:
        # noinspection PyTypeChecker
        for i, line in enumerate(result):
            parts = line.split("=", 2)
            if string_utils.trim(parts[1]).upper() == "ENABLED":
                enabled = True
                break
    return enabled


def is_codec_h264_enabled():
    """Determine if the H264 codec is enabled.

    :returns: True if enabled; Otherwise, False.
    :rtype: bool
    """
    return get_codec_enabled("H264")


def is_codec_mpg2_enabled():
    """Determine if the MPG2 code is enabled.

    :returns: True if enabled; Otherwise, False.
    :rtype: bool
    """
    return get_codec_enabled("MPG2")


def is_codec_wvc1_enabled():
    """Determine if the WVC1 codec is enabled.

    :returns: True if enabled; Otherwise, False.
    :rtype: bool
    """
    return get_codec_enabled("WVC1")


def get_clock_frequency(target):
    """Get the clock frequency for the specified target.

    :param string target: The target clock to get the frequency of.
    :returns: The clock frequency, if successful; Otherwise, -1.
    :rtype: int, long
    """
    if string_utils.is_null_or_empty(target):
        return -1

    target = string_utils.trim(target)
    val = -1
    cmd = "/opt/vc/bin/vcgencmd measure_clock " + target
    result = exec_utils.execute_command(cmd)
    if result is not None:
        # noinspection PyTypeChecker
        for i, line in enumerate(result):
            parts = line.split("=", 2)
            try:
                temp = float(string_utils.trim(parts[1]))
            except ValueError:
                temp = -1

            if temp != -1:
                val = temp
                break
    return val


def get_bash_version_info():
    """Get the BaSH version info.

    This method is used to help determine the HARD_FLOAT / SOFT_FLOAT ABI of
    the system.

    :returns: The BaSH version info.
    :rtype: string
    """
    ver = string_utils.EMPTY
    try:
        result = exec_utils.execute_command("bash --version")
        # noinspection PyTypeChecker
        for i, line in enumerate(result):
            if not string_utils.is_null_or_empty(line):
                ver = line  # Return only the first line.
                break
    except Exception:
        pass

    return ver


def get_read_elf_tag(tag):
    """Obtain a specific tag value from the ELF.

    This method will obtain a specified tag value from the ELF info in the
    '/proc/self/exe' program (this method is used to help determine the
    HARD-FLOAT / SOFT-FLOAT ABI of the system).

    :param string tag: The tag to get the value of.
    :returns: The ABI tag value.
    :rtype: string
    """
    tag_val = string_utils.EMPTY
    try:
        cmd = "/usr/bin/readelf -A /proc/self/exe"
        result = exec_utils.execute_command(cmd)
        if result is not None:
            # noinspection PyTypeChecker
            for i, line in enumerate(result):
                part = string_utils.trim(line)
                if (string_utils.starts_with(part, tag) and
                        string_utils.contains(part, ":")):
                    line_parts = part.split(":", 2)
                    if len(line_parts) > 1:
                        tag_val = string_utils.trim(line_parts[1])

                    break
    except Exception:
        pass

    return tag_val


def has_read_elf_tag(tag):
    """Determine if a specified tag exists from the ELF.

    This method will determine if a specified tag exists from the ELF info in
    the '/proc/self/exe' program (this method is used to help determine the
    HARD-FLOAT / SOFT-FLOAT ABI of the system).

    :param string tag: The tag to check for.
    :returns: True if contains the specified ELF tag.
    :rtype: boolean
    """
    tag_val = get_read_elf_tag(tag)
    return not string_utils.is_null_or_empty(tag_val)


def is_hard_float_abi():
    """Determine if is hard float ABI.

    :returns: True if is hard float ABI; Otherwise, False.
    :rtype: bool
    """
    return (string_utils.contains(get_bash_version_info(), "gnueabihf") or
            has_read_elf_tag("Tag_ABI_HardFP_use"))


def get_current_time_millis():
    """Get the current system time in milliseconds.

    :returns: The current time in milliseconds.
    :rtype: int
    """
    return int(round(time.time() * 1000))
