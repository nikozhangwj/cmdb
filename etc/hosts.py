#!/usr/bin/env python
# encoding: utf-8

import argparse
import sys
import json


def list():
    d_host = {}
    host1 = {}
    host2 = {}
    h1 = ['139.199.172.142', '111.230.219.214']
    h2 = ['23.106.152.90']
    host1['hosts'] = h1
    host2['hosts'] = h2
    d_host['tencent_server'] = host1
    d_host['ss_server'] = host2
    return json.dumps(d_host, indent=4)


def hosts(name):
    d_hosts = {'23.106.152.90':{'ansible_ssh_port': 29959,'ansible_sudo_pass': 'Nikoray0910'}, '111.230.219.214':{'ansible_ssh_port': 2235, 'ansible_python_interpreter':'/usr/bin/python2', 'ansible_sudo_pass': 'Nikoray0910'}, '139.199.172.142':{'ansible_ssh_port': 2235, 'ansible_python_interpreter':'/usr/bin/python2', 'ansible_sudo_pass': 'Nikoray0910'}}
    return json.dumps(d_hosts[name])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l','--list',help='hosts list',action='store_true')
    parser.add_argument('-H', '--host', help='hosts vars')
    args = vars(parser.parse_args())

    if args['list']:
        print(list())
    elif args['host']:
        print(hosts(args['host']))
    else:
        parser.print_help()
