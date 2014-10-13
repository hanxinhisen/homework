#!/usr/bin/env python
#coding:utf-8
import SocketServer
import time
import commands
import MySQLdb
import hashlib
import getpass
from prettytable import PrettyTable
#from hashlib import md5
from multiprocessing import Process, Pool
import paramiko
import os
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
      cur.execute("select s.host_name,s.host_ip,s.`user`,s.`password`,s.`port`,g.group_name from user_info u, server_info s,server_group g where u.server_group = s.group_id and  s.group_id = g.group_id and u.name  = '%s';"%username)
      result= cur.fetchall()
      cur.close()
      conn.close()
      return result
    except MySQLdb.Error,e:
      print 'mysql error mes:',e
#def net_test(ip):
#
def ssh_run(host_info,cmd):

    ip,username,password,port = host_info
    s.connect(ip,int(port),username,password,timeout=5)   #连接远程主机
    stdin,stdout,stderr = s.exec_command(cmd)		#执行命令

    cmd_result = stdout.read(),stderr.read()		#读取命令结果

    print '\033[32;1m-------------%s执行结果-----------\033[0m' % ip
    for line in cmd_result:
        print line,
    #print stdout.read(),stderr.read()
    s.close()
#############
while True:
    notice='''
      欢迎使用运维审计系统
      请选择功能:
      1.登陆单台服务器
      2.执行批量命令
      3.发送文件
      4.回收文件
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
        while True:
          choose=raw_input('请选择-->').strip()
          if not choose.isdigit():
              print '请输入数字'
              continue
          else:
              break
        tmp=host_list(username)
        server_list={} #for log in
        ip_list=[]
        print_list={} #for print to user
        server_group=''
        for row in tmp:
            server_list[row[0]]=row[1:]
            server_group=row[5]
            ip_list.append(row[1:5])
            print_list[row[0]]=row[1]

        if choose == '1':
            print '您可登陆的服务器组是\033[32;1m%s\033[0m组'%(server_group)
            print '正在获取您可登陆的服务器和服务器的当前连接状态...'
            a = PrettyTable(['服务器名','服务器ip','当前状态','组名称'])
            offline_list=[]   #获取不能ping通的服务器，为下面做铺垫
            for n,ip in print_list.items():
                  status=commands.getstatusoutput('ping -c 1 -w 1 %s'%ip)
                  if status[0] is 0:
                    a.add_row([n,ip,'online',server_group])
                  else:
                    a.add_row([n,ip,'offline',server_group])
                    offline_list.append(n)
            print '您可登陆的服务器列表如下:'
            print a
            try:
                host = raw_input('请选择您要登陆的服务器名:').strip()
                if host == 'quit':
                    print "Goodbye!"
                    break
            except KeyboardInterrupt:continue
            except EOFError:continue
            if len(host) ==0 or not server_list.has_key(host):
                print '你输入的服务器名称为\033[031;1m%s\033[0m,此服务器名不存在，或者您无权登陆！'%host
                continue
            if host in offline_list:
                choose2=raw_input('您选择的服务器状态为offline,可能无法连接,是否继续(y)?').strip()
                if choose2.upper() == 'Y':
                    #status=commands.getstatusoutput('ping -c 1 -w 1 %s'%host)
                    #if status == '0':
                        print '\033[32;1mGoing to connect \033[0m', server_list[host][0]
                        os.system("python demo.py %s %s  %s  %s %s" % (server_list[host][0],server_list[host][1],server_list[host][2],server_list[host][3],username))
                    #else:
                    #    print '无法连接'
                else:
                    print '放弃登陆！'
            else:
               print '\033[32;1mGoing to connect \033[0m', server_list[host][0]
               os.system("python demo.py %s %s  %s  %s %s" % (server_list[host][0],server_list[host][1],server_list[host][2],server_list[host][3],username))
               os.system('clear')
        elif choose  == '2':

            s = paramiko.SSHClient()	#绑定实例
            s.load_system_host_keys()	#加载本机HOST主机文件
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            while True:
                cmd=raw_input('command:--->').strip()
                host_info=ip_list
                p = Pool(processes=5)

                result_list = []

                for h in  host_info:
                  status=commands.getstatusoutput('ping -c 1 -w 1 %s'%h[0])
                  if status[0] is 0:
                     result_list.append(p.apply_async(ssh_run, [h,'%s'%cmd])  )
                  else:
                      print "%s 无法连接,跳过该服务器"%h[0]
                      continue
                if os.path.exists('/tmp/audit/logs'): #判断用户目录是否存在
                         pass
                else:
                   os.makedirs('/tmp/audit/logs')
                day_time=time.strftime('%Y_%m_%d')
                date =time.strftime('%Y_%m_%d %H:%M:%S')
                f = open('/tmp/audit/logs/audit_%s_%s_batch.log' % (day_time,username),'a')
                log = "%s | %s | %s | %s\n" % (server_group,date,username,cmd)
                f.write(log)
                f.flush()
                f.close()
                for res in result_list:
                   res.get()
        else:
            print '功能不存在'
    else:
        print '对不起，用户名或密码错误！！'