#!/usr/bin/python
# -*-coding:utf-8-*-

import sys
import argparse
import re


def parse_args():
    parser = argparse.ArgumentParser(prog="GatherInfo", formatter_class=argparse.RawTextHelpFormatter,
                                     description="A Tiny Toy For Gather Info.\nBy Am4zing(www.*********)",
                                     usage="Python GatherInfo.py [options]")
    parser.add_argument('-d', '--domain', help='The Target Url. eg: google.com', type=str, )
    parser.add_argument('-host', '--host', help='The Remote SSH Host IP.', type=str, )
    parser.add_argument('-p', '--password', help='The Remote SSH Host Password.', type=str, )
    parser.add_argument('-u', '--username', help='The Remote SSH Host Username.', type=str, )
    parser.add_argument('-a', '--auto', help='Running Auto Mode.', action='store_true')
    parser.add_argument('-in', '--intercative', help='Running Interactive Mode.', action='store_true')
    parser.add_argument('-port', '--port', help='The Remote SSH Host Port.', type=int, )
    parser.add_argument('-l', '--local-mode', help='Run this script at local machine.', type=str)
    parser.add_argument('-r', '--remote-mode', help='Use the Remote SSH Host.',
                        usage='Python GatherInfo.py -r -host 1.1.1.1 -u user -p password -port 22 -d xxx.com', type=str)
    # parser.add_argument('-p', help='The Remote SSH Host Password.', type=str)

    if len(sys.argv) == 1:
        sys.argv.append('-h')

    args = parser.parse_args()
    # check_args(args)
    # check_ipaddr(args.host)
    return args


def check_args(args):
    if not args.l or not args.r:
        msg1 = '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ \n' \
              'Args Missing! One of the following args should be specified \n' \
              '-i 192.168.1.1 \n' \
              '-u root \n' \
              '-p password'
        raise Exception(msg1)
    if type(args.port) != int:
        msg2 = '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ \n' \
              'The type of port is int.'
        raise Exception(msg2)


def check_ipaddr(ipaddr):
    ip_pattern = '^((?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.){3}(?:(2[0-4]\d)|(255[0-5])|([01]?\d\d?))$'
    msg = 'SSH Host IP is Not Correct.'
    if not ipaddr:
        return False

    ipcheck = re.compile(ip_pattern, re.I)
    return True if ipcheck.match(ipaddr) else Exception(msg)

