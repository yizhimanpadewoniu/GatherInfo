#!/usr/bin/python
# -*-coding:utf-8-*-

import struct
import paramiko
import os
import re
from stat import *


# 定义文件类型列表
def type_list():
    return {
        "EFD8FF": "JPEG",
        "89504E47": "PNG",
        "3C3F786D6C": "XML",
        "68746D6C3E": "HTML"
    }


# 字节码转16进制字符串
def bytes2hex(bytes):
    num = len(bytes)
    hexstr = u""
    for i in range(num):
        t = u"%x" % bytes[i]
        if len(t) % 2:
            hexstr += u"0"
        hexstr += t
    return hexstr.upper()


# 获取xml结果文件
# 获取文件类型
def file_type(filename):
    binfile = open(filename, 'rb')  # 必需二制字读取
    tl = type_list()
    ftype = 'unknown'
    for hcode in tl.keys():
        numOfBytes = len(hcode) / 2  # 需要读多少字节
        binfile.seek(0)  # 每次读取都要回到文件头，不然会一直往后读取
        hbytes = struct.unpack_from("B" * numOfBytes, binfile.read(numOfBytes))  # 一个 "B"表示一个字节
        f_hcode = bytes2hex(hbytes)
        if f_hcode == hcode:
            ftype = tl[hcode]
            break
    binfile.close()
    return ftype


# 从远程将扫描结果传送到本地
def __get_all_files_in_remote_dir(sftp, remote_dir):
    # 保存所有文件列表
    all_files = list()
    # 去掉路径字符串中的字符‘/’
    if remote_dir[-1] == '/':
        remote_dir = remote_dir[0:-1]
    # 获取当前指定目录下的所有目录及文件，包含属性值
    files = sftp.listdir_attr(remote_dir)
    for x in files:
        # remote_dir目录中每一个文件或目录的完整路径
        filename = remote_dir + '/' + x.filename
        # 如果是目录，则递归处理该目录，这里用到了stat库中的S_ISDIR方法，与linux中的宏的名字完全一致
        if S_ISDIR(x.st_mode):
            all_files.extend(__get_all_files_in_remote_dir(sftp, filename))
        else:
            all_files.append(filename)
    return all_files


def output(host, port, usrname, passwd, domain):
    # client_ssh = ConnectSSH(self.host, self.port, self.usrname, self.passwd)
    transport = paramiko.Transport(host, port)
    transport.connect(username=usrname, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    remote_dir = '/root/harvest_result'
    local_dir = 'results'
    # 获取远端linux主机上制定目录及其子目录下的所有文件
    all_files = __get_all_files_in_remote_dir(sftp, remote_dir)
    # print all_files

    for x in all_files:
        # remote_dir目录中每一个文件或目录的完整路径
        filename = x.split('/')[-1]
        local_filename = os.path.join(local_dir, filename)
        print u'Get文件%s传输中...' % filename
        sftp.get(x, local_filename)
    transport.close()

    lists = os.listdir('results/')
    for li in lists:
        xml_path = open('results/%s' % li)
        file_name = 'results/%s' % li
        filetype = file_type(file_name)
        if filetype is 'XML':
            # xml_path = open('/result/%s' % list)
            nmap_target_path = 'nmap/%s' % domain
            subdomian_path = 'hosturl/%s' % domain
            host_nmap = open(nmap_target_path, 'w')
            host_url = open(subdomian_path, 'w')
            lines = xml_path.readlines()

            for line in lines:
                # ips = re.compile(r'(?<=<host><ip>)(.*?)(?<=(</ip>))')
                # hosts = re.compile(r'(?<=<hostname>)(.*?)(?<=(</hostname>))')
                ips = re.compile(r'<ip>(.*?)</ip>')
                hosts = re.compile(r'<hostname>(.*?)</hostname>')
                ip_address = list(set(re.findall(ips, line)))
                host = list(set(re.findall(hosts, line)))

                for i in ip_address:
                    host_nmap.write('%s\n' % i)

                for h in host:
                    host_url.write('%s\n' % h)
            xml_path.close()
            host_nmap.close()
            host_url.close()