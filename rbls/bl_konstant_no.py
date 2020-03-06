"""Verify bl.konstant.no."""
from datetime import datetime

from requests import post


def run(crate_server, crate_port, rip):
    """Run verification and if positive insert data to the database."""
    from dns.resolver import Resolver
    dns_resolver = Resolver()
    try:
        ip = '.'.join(reversed(rip.split('.')))
        rblname = 'bl.konstant.no'
        dns_query = rip + '.' + rblname
        dns_result = dns_resolver.query(dns_query, 'A')
        date = datetime.now().isoformat()
        if dns_result[0]:
            url = 'http://' + crate_server + ':' + crate_port + '/_sql'
            k = ['date', 'ip_srv', 'rblname']
            v = ["'{}', '{}', '{}'".format(date, ip, rblname)]
            value = """INSERT INTO {} ({}) VALUES ({})""".format(
                'rbl',
                ', '.join(k),
                ', '.join(v)
            )
            payload = {'stmt': value}
            post(url, json=payload)
    except:
        pass
