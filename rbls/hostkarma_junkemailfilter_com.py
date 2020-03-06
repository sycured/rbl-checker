"""Verify hostkarma.junkemailfilter.com."""
from datetime import datetime

from requests import post


def run(crate_server, crate_port, rip):
    """Run verification and if positive insert data to the database."""
    from dns.resolver import Resolver
    dns_resolver = Resolver()
    try:
        ip = '.'.join(reversed(rip.split('.')))
        rblname = 'hostkarma.junkemailfilter.com'
        dns_query = rip + '.' + rblname
        dns_result = dns_resolver.query(dns_query, 'A')
        date = datetime.now().isoformat()
        switcher = {
            '127.0.0.1': '0',
            '127.0.0.2': '1',
            '127.0.0.3': '1',
            '127.0.0.4': '0',
            '127.0.0.5': '0',
        }
        if (switcher.get(str(dns_result[0]))) == '1':
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
