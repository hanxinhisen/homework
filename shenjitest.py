#!/usr/bin/env python
#coding:utf-8
import SocketServer
import os
import time
import commands
import MySQLdb
import hashlib
import getpass
from prettytable import PrettyTable
from hashlib import md5
from multiprocessing import Process, Pool
import paramiko
import sys,os
import paramiko
host='192.168.1.107'
port=22
user='root'
password='123456'

s = paramiko.SSHClient()	#绑定实例
s.load_system_host_keys()	#加载本机HOST主机文件
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
s.connect(host,port,user,password,timeout=5)   #连接远程主机
stdin,stdout,stderr = s.exec_command('hostname')		#执行
cmd_result = stdout.read(),stderr.read()		#读取命令
print '\033[32;1m-------------%s-----------\033[0m' % host, user
for line in cmd_result:
    print line,