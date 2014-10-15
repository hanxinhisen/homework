#!/usr/bin/env python
#coding:utf-8
import SocketServer
import sys
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
    try:
       s.connect(ip,int(port),username,password,timeout=5)   #连接远程主机
       stdin,stdout,stderr = s.exec_command(cmd)		#执行命令
       cmd_result = stdout.read(),stderr.read()		#读取命令结果

       print '\033[32;1m-------------%s执行结果-----------\033[0m' % ip
       for line in cmd_result:
           print line,
    except Exception,e:
       print '连接%s:\033[31;1;5m%s\033[0m,已经跳过执行命令！！'%(ip,e)
    finally:
        s.close()
def put_file(host_info,localfile):
    ip,username,password,port = host_info

    try:
        t = paramiko.Transport((ip,int(port)))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        #sftp.get('/tmp/sunlogin_linux_v1.0.0.25020_beta.tar.gz', '/tmp/file_from_hanxin.gz')
        time1=time.time()
        sftp.put('%s'%localfile, '/tmp/from_audit_system_%s'%localfile.split('/')[-1])
        time2=time.time()
        print '成功将\033[32;1m%s\033[0m发送至\033[32;1m%s,\033[0m本次上传消耗\033[32;1m%s\033[0m秒'%(localfile.split('/')[-1],ip,time2-time1)
        t.close()
    except Exception:
        print '%s连接失败!'%ip
def get_file(host_info,remotefile):
    ip,username,password,port = host_info
    t = paramiko.Transport((ip,int(port)))
    t.connect(username=username, password=password)

    sftp = paramiko.SFTPClient.from_transport(t)

    try:
       time1=time.time()
       sftp.get('%s'%remotefile, '/tmp/%s_from_%s'%(remotefile.split('/')[-1],ip))
       time2=time.time()
       print '成功将\033[32;1m%s\033[0m从\033[32;1m%s\033[0m下载至本机\033[32;1m/tmp/\033[0m下,本次上传消耗\033[32;1m%s\033[0m秒'%(remotefile.split('/')[-1],ip,time2-time1)
    except IOError,e:
       print e
       print '%s上没有%s，已跳过。'%(ip,remotefile.split('/')[-1])
    finally:
       t.close()
def get_sys_info():#for get server information
        tmp=host_list(username)
        global server_list
        global ip_list
        global print_list
        global server_group
        server_list={} #for log in
        ip_list=[]
        print_list={} #for print to user
        server_group=''
        for row in tmp:
            server_list[row[0]]=row[1:]
            server_group=row[5]
            ip_list.append(row[1:5])
            print_list[row[0]]=row[1]
def print_sys_info():#for print server information
    a = PrettyTable(['序号','服务器名','服务器ip','当前状态','组名称'])
    global offline_list#获取不能ping通的服务器
    offline_list=[]
    count=0
    for n,ip in print_list.items():
          status=commands.getstatusoutput('ping -c 1 -w 1 %s'%ip)
          if status[0] is 0:
            count+=1
            a.add_row([count,n,ip,'normal',server_group])
          else:
            count+=1
            a.add_row([count,n,ip,'can not reach',server_group])
            offline_list.append(n)
    print '您可文件操作的服务器列表如下:'
    print a

#############
while True:
    notice='''
      欢迎使用运维审计系统
      请选择功能:
      1.\033[32;1m 登陆单台服务器\033[0m
      2.\033[36;1m 批量执行命令\033[0m
      3.\033[32;1m 单台发送文件\033[0m
      4.\033[36;1m 批量发送文件\033[0m
      5.\033[32;1m 单台下载文件\033[0m
      6.\033[36;1m 批量下载文件\033[0m
      7. 切换用户
      8. 退出系统
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
          choose=raw_input('请选择数字-->').strip()
          if not choose.isdigit():
              print '请输入数字'
              continue
          else:
              break


        if choose == '1':
           while True:
            get_sys_info()
            print '您可登陆的服务器组是\033[32;1m%s\033[0m组'%(server_group)
            print '正在获取您可登陆的服务器和服务器的当前连接状态...'
            print_sys_info()

            try:
                host = raw_input('请选择您要登陆的服务器名:').strip()
                if host == 'quit':
                    print "Goodbye!"
                    break
            except KeyboardInterrupt:continue
            except EOFError:continue
            if len(host) ==0 or not server_list.has_key(host):
                os.system('clear')
                print '你输入的服务器名称为\033[031;1m%s\033[0m,此服务器名不存在，或者您无权登陆！'%host

                continue
            if host in offline_list:
                choose2=raw_input('您选择的服务器状态为:can not reach,可能无法连接,是否继续(y)?').strip()
                if choose2.upper() == 'Y':
                    #status=commands.getstatusoutput('ping -c 1 -w 1 %s'%host)
                    #if status == '0':
                        print '\033[32;1mGoing to connect \033[0m', server_list[host][0]
                        os.system("python virtual_login.py %s %s  %s  %s %s" % (server_list[host][0],server_list[host][1],server_list[host][2],server_list[host][3],username))
                    #else:
                    #    print '无法连接'
                else:
                    print '放弃登陆！'
            else:
               print '\033[32;1mGoing to connect \033[0m', server_list[host][0]
               os.system("python virtual_login.py %s %s  %s  %s %s" % (server_list[host][0],server_list[host][1],server_list[host][2],server_list[host][3],username))
               os.system('clear')
        elif choose  == '2':
            get_sys_info()
            time1=time.time()
            s = paramiko.SSHClient()	#绑定实例
            s.load_system_host_keys()	#加载本机HOST主机文件
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print '批量命令将发往以下服务器:'
            print_sys_info()
            while True:
                cmd=raw_input('command:--->').strip()
                if cmd =='quit':break
                host_info=ip_list
                p = Pool(processes=5)

                result_list = []

                for h in  host_info:
                     result_list.append(p.apply_async(ssh_run, [h,'%s'%cmd])  )
                p.close()
                p.join()
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
        elif choose  == '3':
          while True:
            get_sys_info()
            print '您可文件操作的服务器组是\033[32;1m%s\033[0m组'%(server_group)
            print '正在获取您可文件操作的服务器和服务器的当前连接状态...'
            print_sys_info()

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

            h=server_list[host][0],server_list[host][1],server_list[host][2],server_list[host][3]
            if host in offline_list:
                choose2=raw_input('您选择的服务器状态为offline,可能无法连接,是否继续(y)?').strip()
                if choose2.upper() == 'Y':
                   while True:
                      local_file=raw_input('请输入本地服务器文件名(如:/tmp/test.file,退出请输入"quit"):').strip()
                      if len(local_file) == 0:continue
                      if not os.path.exists(local_file):
                          print '\033[31;1m%s\033[0m不存在'%local_file;continue
                      put_file(h,local_file)
                else:
                   print '放弃传输！'

            else:
               while True:
                      local_file=raw_input('请输入本地服务器文件名(如:/tmp/test.file,退出请输入"quit"):').strip()
                      if local_file == 'quit':break
                      if len(local_file) == 0:continue
                      if not os.path.exists(local_file):
                          print '\033[31;1m%s\033[0m不存在'%local_file;continue
                      put_file(h,local_file)
        elif choose == '4':
            get_sys_info()
            host_info=ip_list
            print '批量上传命令将发往以下服务器:'
            print_sys_info()
            while True:

                local_file=raw_input('请输入远程服务器文件名(如:/tmp/test.file):').strip()
                #if os.path.exists('%s'%local_file): #判断用户目录是否存在
                #    break
                #else:
                #    print '%s不存在'%local_file
                #    continue
                if local_file == 'quit':break
                if not os.path.exists(local_file):
                          print '\033[31;1m%s\033[0m不存在'%local_file;continue
                result_list = []
                p = Pool(processes=5)
                for h in  host_info:
                      print '%s上传任务已经创建'%h[0]
                      result_list.append(p.apply_async(put_file, [h,local_file]))

                print '全部上传任务创建完成，等待传输结果'
                #for res in result_list:
                #    print res.get()
                p.close()
                p.join()
        elif choose  == '5':
          while True:
            get_sys_info()
            print '您可文件操作的服务器组是\033[32;1m%s\033[0m组'%(server_group)
            print '正在获取您可文件操作的服务器和服务器的当前连接状态...'
            print_sys_info()
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
            h=server_list[host][0],server_list[host][1],server_list[host][2],server_list[host][3]
            if host in offline_list:
                choose2=raw_input('您选择的服务器状态为offline,可能无法连接,是否继续(y)?').strip()

                if choose2.upper() == 'Y':
                   while True:
                      remote_file=raw_input('请输入远程服务器文件名(如:/tmp/test.file):').strip()
                      if remote_file == 'quit':break
                      put_file(h,remote_file)
                else:
                   print '放弃传输！'
            else:
               while True:
                      remote_file=raw_input('请输入远程服务器文件名(如:/tmp/test.file):').strip()
                      if remote_file == 'quit':break
                      get_file(h,remote_file)
        elif choose  == '6':
            get_sys_info()
            host_info=ip_list
            print '批量下载命令将发往以下服务器:'
            print_sys_info()
            while True:

                remote_file=raw_input('请输入远程服务器文件名(如:/tmp/test.file):').strip()
                if remote_file == 'quit':break
                p = Pool(processes=5)
                for h in  host_info:
                      print '已经在%s创建下载任务'%h[0]
                      p.apply_async(get_file, [h,remote_file])
                p.close()
                p.join()
        elif choose  == '7':
            break
        elif choose  == '8':
            sys.exit()
        else:
            print '功能不存在'
    else:
        print '对不起，用户名或密码错误！！'