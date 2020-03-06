#!/usr/bin/env python3
# coding: utf-8
"""Help you to check if any IP in your IP range is blacklisted : SECURE."""


def main():
    """Main function with launch multiprocessing."""
    import check
    from os.path import dirname, realpath
    from sys import argv
    from multiprocessing import Pool
    print('rbl-checker : SECURE\n'
          'Author : sycured\n'
          'LICENSE : GNU GENERAL PUBLIC LICENSE Version 3\n')
    dnipr = dirname(realpath(argv[0])) + '/../ip_range.list'
    with open(dnipr, 'r') as ip_range_file:
        entries = ip_range_file.read().splitlines()
        with Pool(processes=None) as pool:
            pool.map(check.dispatch, entries)


if __name__ == '__main__':
    main()
