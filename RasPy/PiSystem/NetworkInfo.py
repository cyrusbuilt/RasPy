"""Provides network-related utility methods.

NetworkInfo.py

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


import socket
import psutil
from RasPy import ExecUtils


def get_hostname():
    """Get the name of the localhost.

    :returns: The host name.
    :rtype: string
    """
    return socket.gethostname()


def get_fqdn():
    """Get the fully-qualified domain name of the local host.

    :returns: The fully-qualified domain name (FQDN).
    :rtype: string
    """
    result = ExecUtils.execute_command("hostname -f")
    if result is not None:
        return result[0]

    return get_hostname()


def get_ip_addresses():
    """Get an array of all the IP addresses to all network interfaces.

    :returns: An array of IPv4/IPv6 addresses assigned to the local host.
    :rtype: array
    """
    addrs = []
    ifaces = psutil.net_if_addrs()
    for eth, net in ifaces.iteritems():
        for n in net:
            if n.family == socket.AF_INET or n.family == psutil.AF_LINK:
                if eth != "loopback" and n.address:
                    addrs.append(n.address)
    return addrs


def get_ip_address():
    """Get the IP address of the local system's hostname.

    This only works if the hostname can be resolved.

    :returns: The IP address.
    :rtype: string
    """
    return ExecUtils.execute_command("hostname --ip-address")[0]


def get_all_fqdns():
    """Get all FQDNs of the machine.

    This enumerates all the configured network addresses on all configured
    network interfaces, and translates them to DNS domain names. Addresses
    that cannot be translated (ie. because they do not have an appropriate
    reverse DNS entry) are skipped. Note that different addresses may resolve
    to the same name, therefore the return value may contain duplicate entries.
    Do not make any assumptions about the order of the items in the array.

    :returns: The FQDNs.
    :rtype: array
    """
    names = ExecUtils.execute_command("hostname --all-fqdns")[0]
    return names.split()


def get_name_servers():
    """Get an array of all available name servers.

    :returns: The name servers.
    :rtype: array
    """
    result = []
    lines = ExecUtils.execute_command("cat /etc/resolv.conf | grep nameserver")
    for namestr in lines:
        result.append(namestr[len("nameserver") + 1:])

    return result
