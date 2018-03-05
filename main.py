#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from lib.ssh import *
from lib.cmdline import parse_args
from lib.output import *
paramiko.util.log_to_file('lib/logs/log')


def auto(client_ssh, host_domain):
    # 判断域名命名文件夹是否已存在
    cmd = 'ls /root/harvest_result'
    stdin, stdout, stderr = client_ssh.exec_command(cmd)
    err_msg = stderr.read()
    out_data = stdout.read()
    # 判断域名名命的文件夹是否存在，用来存储域名枚举结果
    if len(err_msg) >= 0:
        client_ssh.exec_command('rm -rf /root/harvest_result')
        client_ssh.exec_command('mkdir /root/harvest_result')
    cmd = 'python /root/theHarvester/theHarvester.py -d %s -b all -e 8.8.8.8 -f /root/harvest_result/domain' % host_domain
    # cmd = 'theharvester -d %s -b linkedin -e 8.8.8.8 -f /root/%s.xml' % (self.domain, self.domain)  # 虚拟机测试使用
    stdin, stdout, stderr = client_ssh.exec_command(cmd)
    data = stdout.read()
    err = stderr.read()
    print data
    client_ssh.close()

if __name__ == "__main__":
    args = parse_args()
    # host = sys.argv[1]
    # port = sys.argv[2]
    # usrname = sys.argv[3]
    # passwd = sys.argv[4]
    # domain = sys.argv[5]
    host = args.i
    port = args.port
    usrname = args.u
    passwd = args.p
    domain = args.d
    print host
    # client_ssh = Linux(host, port, usrname, passwd).connect_ssh()
    # auto(client_ssh, domain)


