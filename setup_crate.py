#!/usr/bin/env python3
"""Create table in Crate.io database engine."""
from os import _exit

from requests import post

crate_server = 'localhost'
crate_port = '4200'
url = 'http://' + crate_server + ':' + crate_port + '/_sql'
value = """CREATE TABLE rbl(date timestamp, ip_srv ip, rblname string)"""
payload = {'stmt': value}
r = post(url, json=payload)
if r.status_code == 200:
    print('SUCCESS')
else:
    print('Error :\n' + r.text)
    _exit(1)
