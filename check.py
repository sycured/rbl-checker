#!/usr/bin/env python3
# coding: utf-8
"""Entire checker module."""
from rbls.run import do_job


def check(ip):
    """Check and print listed rbl only.

    :type ip: str
    """
    crate_server = 'localhost'
    crate_port = '4200'
    rip = '.'.join(reversed(ip.split('.')))
    do_job(crate_server, crate_port, rip)

def dispatch(entry):
    """Send each IP in a range to the check otherwise send only one IP."""
    from ipaddress import ip_network
    if '/32' in entry:
        check(entry.split('/')[0])
    else:
        for ip in ip_network(entry).hosts():
            check(ip)
