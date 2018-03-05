#!/usr/bin/python
# -*-coding:utf-8-*-

import paramiko
import interactive


class Linux(object):

    def __init__(self, host, port, usrname, passwd):
        self.host = host
        self.port = port
        self.usrname = usrname
        self.passwd = passwd
        self.cmd = ''
        # self.client = None
        # self.channel = channel
        # self.interactive()

    def interactive(self):
        interactive_ssh = paramiko.SSHClient()
        interactive_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        interactive_ssh.connect(hostname=self.host, port=self.port, username=self.usrname, password=self.passwd)
        channel = interactive_ssh.invoke_shell()
        interactive.interactive_shell(channel)
        channel.close()
        # interactive_ssh.close()

    def connect_ssh(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.host, username=self.usrname, password=self.passwd, timeout=300)
        return ssh








