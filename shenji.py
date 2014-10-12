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
def user_check(username,passwd):#将客户端输入的用户名和密码进行验证
    try:
      conn=MySQLdb.connect(host='192.168.1.107',user='root',passwd='123456',port=3306)
      cur=conn.cursor()
      conn.select_db('audit_server_hx')
      cur.execute("SELECT * FROM `user_info` where `name` ='%s' and  `password` = '%s'"%(username,passwd))
      result= cur.fetchall()
      tmp=[]
      for row in result:
        tmp.append(row)
      cur.close()
      conn.close()
      if len(tmp) >= 1:
       return 'success'
      else:
       return 'error'
    except MySQLdb.Error,e:
      print 'mysql error mes:',e
def host_list(username):
    try:
      conn=MySQLdb.connect(host='192.168.1.107',user='root',passwd='123456',port=3306)
      cur=conn.cursor()
      conn.select_db('audit_server_hx')
      cur.execute("select s.host_name,s.host_ip,s.`user`,s.`password`,s.`port` from user_info u, server_info s where u.server_group = s.server_group and u.name = '%s';"%username)
      result= cur.fetchall()
      #tmp=[]
      #for row in result:
      #  tmp.append(row)
      cur.close()
      conn.close()
      return result
    except MySQLdb.Error,e:
      print 'mysql error mes:',e
def ssh_run(host_info,cmd):
    ip,username,password,port = host_info
    print '-----------------'
    print ip
    print username
    print password
    print port
    print '-----------------'
    s.connect('%s'%ip,'%s'%port,'%s'%username,'%s'%password,timeout=1)   #连接远程主机
    stdin,stdout,stderr = s.exec_command(cmd)		#执行命令

    cmd_result = stdout.read(),stderr.read()		#读取命令结果

    print '\033[32;1m-------------%s-----------\033[0m' % ip, username
    for line in cmd_result:
        print line,
#############
while True:
    notice='''
      欢迎使用运维审计系统
      请选择功能:
      1.登陆服务器
      2.发送文件
      3.回收文件
          '''
    while True:
      username=raw_input('input your username:').strip()
      password=getpass.getpass('input your password:').strip()
      #password=raw_input('input your password:').strip()
      if len(username) >= 6 and len(password) >=6:
         break
      else:
         print '用户名或密码长度至少为6位！'
    password=hashlib.md5(password).hexdigest()
    result=user_check(username,password)
    if result == 'success': #如果用户验证成功
     while True:
        print notice
        choose=int(raw_input('请选择-->').strip())
        if choose is 1:
            tmp=host_list(username)
            server_list={} #for log in
            #ip_list=[]
            print_list={} #for print to user
            for row in tmp:
                server_list[row[0]]=row[1:]
                #ip_list.append(row[1:5])
                print_list[row[0]]=row[1]
            print print_list
            print '登陆方式'
            #print ip_list
            print '您可登陆的服务器有:'
            a = PrettyTable(['服务器名','服务器ip'])
            for n,ip in print_list.items():
                a.add_row([n,ip])
            print '您可登陆的服务器列表如下:'
            print a
            try:
                host = raw_input('Please choose one server to login:').strip()
                if host == 'quit':
                    print "Goodbye!"
                    break
            except KeyboardInterrupt:continue
            except EOFError:continue
            if len(host) ==0:continue
            if not server_list.has_key(host) :
                print 'No host matched, try again.'
                continue
            print '\033[32;1mGoing to connect \033[0m', server_list[host][0]
            os.system("python demo.py %s %s  %s  %s %s" % (server_list[host][0],server_list[host][1],server_list[host][2],server_list[host][3],username))


    else:
        print '对不起，用户名或密码错误！！'