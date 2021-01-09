from rbls import rbls
from datetime import datetime
from requests import post
from dns.resolver import resolve


def do_job(crate_server, crate_port, rip):
    """Run verification and if positive insert data to the database."""
    ip = '.'.join(reversed(rip.split('.')))
    for rblname in rbls.rbls:
        try:
            dns_query = rip + '.' + rblname
            dns_result = resolve(dns_query, 'A')
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
        except Exception as e:
            print(f'error {e}')
