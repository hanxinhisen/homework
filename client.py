#!/usr/bin/python
#coding:utf-8
#For FTP client
#0928 finally 
#0929 finally add get file
#0930 finally add xiazai jindutiao
#1002 finally add delete 
#1003 finall add rename 
from __future__ import division
import  socket
import  os
import  sys
import  hashlib
import  time
from hashlib import md5
import getpass
host='192.168.1.103'
port=8889
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))
buffersize=4096
def recv_all(obj,msg_length ):
    raw_result = ''
    while msg_length != 0:
        if msg_length <= 4096:
            data= obj.recv(msg_length)
            msg_length =0
        else:
            data= obj.recv(4096)
            msg_length -= 4096
        raw_result += data
    return raw_result
def ftp_down(username,filename,msg_length):
            f=file('/home/ftp/%s/%s'%(username,filename),'wb+')
            print msg_length
            filesize=msg_length
            while True:
                if msg_length > 4096:
                   filedata = s.recv(4096)
                else:
                   filedata = s.recv(msg_length)
                if not filedata:break
                f.write(filedata)
                msg_length=int(msg_length)-len(filedata)
                msg_finish=int(filesize)-int(msg_length)
                a= (format(int(msg_finish) / int(filesize),'.2%'))
                b=str(int(msg_finish) / int(filesize)*100).split('.')[0]
                print '='*int(b)+'>'+a+'\r',
                if msg_length ==0:
                  break
            f.close()                  
            return 'finish'
def md5_file(filename):   #校验文件md5值
    print '正在计算 %s MD5值。。。'%filename
    m = hashlib.md5()
    a_file = open(filename, 'rb')
    while True:
        blk=a_file.read(4096)
        if not blk:break
        m.update(blk)
    a_file.close()
    return m.hexdigest()
while True:
    while True:
      username=raw_input('input your username:').strip()
      #password=raw_input('input your password:').strip()
      password=getpass.getpass('input your password:').strip()
      if len(username) >= 6 and len(password) >=6:
         break
      else:
         print '用户名或密码长度至少为6位！'
    ###验证用户名密码
    password=hashlib.md5(password).hexdigest()
    print '+++++++++++++++++++++++++++++++++++++'
    s.sendall("%s %s"%(username,password))
    print '-------------------------------------'
    if repr(s.recv(1024)).strip("'") == 'success':
        print '验证成功'
        print '欢迎\033[32;1m%s\033[0m登录该系统！'%username
        while True:
            notice='''
               欢迎使用FTP客户端系统
                           --基于socket
              使用方法介绍
              1.上传功能:put filename
              2.下载功能:get filename
              3.列出所有文件:list
              4.删除文件:delete filename
              5.重命名文件:rename old_filename new_filename
              6.修改密码:repasswd newpasswd newpasswd_again
              7.用户管理(仅限管理员使用):user
              8.退出系统:quit
              '''
            print notice
            string=raw_input('input your command:').strip()
            if len(string) == 0:
               print '请输入命令内容！！'
               continue
            user_cmd=string.split()
            ###################上传模块###########################
            if user_cmd[0] =='put':
                if len(user_cmd) == 2:
                  try:
                    f_size=os.stat(user_cmd[1]).st_size
                    f_md5=md5_file(user_cmd[1])
                    s.sendall("%s %s %s %s %s"%(username,user_cmd[0],user_cmd[1],f_size,f_md5))
                    while True:
                      md5_check_result=s.recv(1024)
                      print md5_check_result
                      #tmp=repr(md5_check_result)
                      #md5_check_result=len(md5_check_result)
                      #print md5_check_result
                      print '++++++++++++++++++++++++++++++++'
                      #print tmp.split(',')[4].strip().strip("'")
                      print '++++++++++++++++++++++++++++++++'
                      print md5_check_result
                      print '++++++++++++++++++++++++++++++++++'
                      if md5_check_result=='null': #当数据库中没有该文件的md5值，所以查询返回结果为空列表，如果不为空返回来存在的记录，判断用户名即可
                          s.sendall('duandian_request')#发送请求是否可以断点续传
                          duandian_check_result=repr(s.recv(1024)).strip("'")
                          print '----------------duandian_check_result----------------'
                          print duandian_check_result
                          print '----------------duandian_check_result----------------'
                          if duandian_check_result == 'keduandian':
                            status='run'
                            while status is 'run':
                              choice=raw_input('当前任务可断点上传,请选择1(重新上传)或者2(断点续传)：').strip()
                              if choice == '1':
                                  print '选择了重新上传'
                                  s.sendall('redo')
                                  print '正在重新发送。。。'
                                  if repr(s.recv(1024)).strip("'") == 'start':
                                    f=file(user_cmd[1],'rb')
                                    f_size_shishi = f_size
                                    time1=time.time()
                                    while True:
                                      data=f.read(buffersize)
                                      if not data:break
                                      s.send(data)
                                      f_size_shishi = f_size_shishi - len(data)
                                      f_finish=f_size-f_size_shishi
                                      a= (format((f_finish / f_size),'.2%'))
                                      b=str(f_finish / f_size*100).split('.')[0]
                                      print '='*int(b)+'>'+a+'\r',
                                    f.close()
                                    status='stop'
                                    print '\n' 
                                    break                                  
                              elif choice == '2':
                                  print '选择了续传'
                                  s.sendall('xuchuan')
                                  print '已发送续传请求'
                                  if repr(s.recv(1024)).strip("'") == 'start':
                                    file_already_upload=repr(s.recv(1024)).strip("'")
                                    print '正在断点发送。。。'
                                    print file_already_upload
                                    f=file(user_cmd[1],'rb')
                                    f_size_weishangchuan = f_size - int(file_already_upload)
                                    time1=time.time()
                                    f.seek(int(file_already_upload))#跳至文件断点位置
                                    while True:
                                      data=f.read(buffersize)
                                      if not data:
                                        break
                                      s.send(data)
                                      f_size_weishangchuan = f_size_weishangchuan - len(data)
                                      f_finish=f_size-f_size_weishangchuan
                                      a= (format((f_finish / f_size),'.2%'))
                                      b=str(f_finish / f_size*100).split('.')[0]
                                      print '='*int(b)+'>'+a+'\r',
                                    f.close()
                                    status='stop'
                                    print '\n'
                              else:
                                print '请选择1或者2！！！'
                                continue
                          elif duandian_check_result == 'bukeduandian':
                                  print '正在正常上传。。。'
                                  f=file(user_cmd[1],'rb')
                                  f_size_shishi = f_size
                                  time1=time.time()
                                  while True:
                                    data=f.read(buffersize)
                                    if not data:break
                                    s.send(data)
                                    f_size_shishi = f_size_shishi - len(data)
                                    f_finish=f_size-f_size_shishi
                                    a= (format((f_finish / f_size),'.2%'))
                                    b=str(f_finish / f_size*100).split('.')[0]
                                    print '='*int(b)+'>'+a+'\r',   
                                  f.close()
                                  print '\n' 
                          if len(s.recv(1024)) == 6:   #如果上传完成,server端会发送'finish'字符串，可以判断长度继而判断上传与否
                             time2=time.time()
                             print '上传成功，本次上传消耗\033[31;1m%s\033[0m秒'%(time2 - time1)
                             break
                          else:
                              print '上传失败'
                              break
                      else:
                          print '\033[31;1;5m 文件已存在,为了避免重复上传,已经取消本次上传任务 \033[0m'
                          print " 已存在的文件,服务器端文件名为:\033[32;1m%s\033[0m"%md5_check_result.strip().strip("'")#文件名前 "'"前有个空格，先strip掉
                          print '------------------------------'
                          break
                  except (IOError,OSError),e:
                        print '输入的文件名错误,请检查',e
                        continue
            ###################列表模块##########################
            elif user_cmd[0] =='list':
                    s.sendall("%s %s %s %s %s"%(username,user_cmd[0],0,0,0))
                    result=s.recv(4096)
                    os.system('clear')
                    print '文件列表:'
                    print result
            ###################下载模块##########################
            elif user_cmd[0] =='get':
                if len(user_cmd) == 2:
                  s.sendall("%s %s %s %s %s"%(username,user_cmd[0],user_cmd[1],0,0))
                  file_check_result=repr(s.recv(1024)).strip("'")
                  if file_check_result != 'null':
                     s.send('start')#让服务器端发送文件
                     if os.path.exists('/home/ftp/%s'%username): #判断用户目录是否存在
                          pass
                     else:
                          os.makedirs('/home/ftp/%s'%username)
                     result = ftp_down(username,user_cmd[1],file_check_result.strip().strip("'").strip('L'))
                     del file_check_result
                     if result == 'finish':
                        print '\n'
                        print '下载完成'
                        print '%s已经下载至/home/ftp/%s'%(user_cmd[1],username)
                     else:
                        print '下载失败'
                  else:
                      print '文件不存在'
    ###################删除模块########################## 
            elif user_cmd[0] =='delete':
                if len(user_cmd) == 2:
                  s.sendall("%s %s %s %s %s"%(username,user_cmd[0],user_cmd[1],0,0))                 
                  file_check_result=repr(s.recv(1024)).strip("'")
                  print '----------------------------'
                  print file_check_result
                  print type(file_check_result)
                  print '----------------------------'
                  if file_check_result == 'exist':
                     choose=raw_input("确定删除请输入'Y',输入其他取消删除：").strip()
                     if choose.strip().upper() == 'Y':
                        s.send('yes')
                        if repr(s.recv(1024)).strip("'")== 'success':
                           print '删除成功！！'
                        else:
                           print '删除失败！！'
                     else:
                        s.send('cancel')
                  elif file_check_result == 'null':
                      print '将要删除的文件不存在!!!'
            elif user_cmd[0] =='rename':
                if len(user_cmd) == 3:
                  s.sendall("%s %s %s %s %s"%(username,user_cmd[0],user_cmd[1],user_cmd[2],0))
                  rename_check_result=repr(s.recv(1024)).strip("'")
                  if rename_check_result == 'exist':
                    print '确定要把\033[32;1m%s\033[0m的文件名，改为\033[31;1m%s\033[0m吗'%(user_cmd[1],user_cmd[2])
                    choose=raw_input("确定重命名请输入'Y',输入其他取消重命名：").strip()
                    if choose.strip().upper() == 'Y':
                          s.send('yes')
                          if repr(s.recv(1024)).strip("'")== 'success':
                            print '重命名成功！！'
                          else:
                            print '重命名失败！！'
                    else: 
                          print '取消重命名！'
                          s.send('cancel')
                  elif rename_check_result == 'null':
                      print '旧文件名不存在或者新文件名已存在!!!'
            elif user_cmd[0] == 'repasswd':
                if len(user_cmd) == 3:            
                  if user_cmd[1] == user_cmd[2] and len(user_cmd[1]) >=6:
                        user_cmd[2]=hashlib.md5(user_cmd[2]).hexdigest()
                        s.sendall("%s %s %s %s %s"%(username,user_cmd[0],user_cmd[2],user_cmd[2],0))
                        if repr(s.recv(1024)).strip("'")== 'success':
                            print '密码修改成功，请重新登录！'
                            sys.exit()
                        else:
                            print '密码修改失败！'
                  else:
                    print '两次输入的新密码不一致或者密码长度不够6位！！'
            elif user_cmd[0] == 'user':
                notice ='''
                             欢迎使用用户管理系统:
                             1.增加用户: useradd username passwd passwd_again
                             2.删除用户: deluser username
                             3.列出所有账号：userlist
                             4.返回上一层: back
                             5.退出系统: quit
                '''
                if username.strip() == 'administrator':#检测是否为管理员
                   #s.sendall("%s %s %s %s %s"%(username,0,0,0,0))
                   #admin_test=repr(s.recv(1024)).strip("'")== 'yes'
                   print '欢迎管理员'
                   os.system('clear')
                   while True:
                      print notice
                      string2=raw_input('input your command:').strip()
                      if len(string) == 0:
                        print '请输入命令内容！！'
                        continue
                      user_cmd2=string2.split()
                      if user_cmd2[0] == 'useradd':
                        if len(user_cmd2) == 4:            
                          if user_cmd2[2] == user_cmd2[3] and len(user_cmd2[2]) >=6 and len(user_cmd2[3]) >=6:
                             user_cmd2[2]=hashlib.md5(user_cmd2[2]).hexdigest()
                             s.sendall("%s %s %s %s %s"%(username,user_cmd2[0],user_cmd2[1],user_cmd2[2],user_cmd2[2]))
                             username_check=repr(s.recv(1024)).strip("'")
                             if username_check == 'bucunzai':
                                add_result=repr(s.recv(1024)).strip("'")
                                if add_result == 'success':
                                   print '添加用户名%s成功'%user_cmd2[1]
                                else:
                                   print '添加用户名%s失败'%user_cmd2[1]
                             else:
                                print '用户名已存在'
                          else:
                             print '两次输入的新密码不一致或者用户名、密码长度不够6位！！' 
                      elif user_cmd2[0] == 'deluser':
                         if len(user_cmd2) == 2:
                            s.sendall("%s %s %s %s %s"%(username,user_cmd2[0],user_cmd2[1],0,0))
                            username_check=repr(s.recv(1024)).strip("'")
                            if username_check == 'cunzai':
                               choose=raw_input("确定删除请输入'Y',输入其他取消删除：").strip()
                               if choose.strip().upper() == 'Y':
                                  s.send('yes')
                                  if repr(s.recv(1024)).strip("'")== 'success':
                                      print '删除成功！！'
                                  else:
                                      print '删除失败！！'
                               else:
                                 s.send('cancel')
                            else:
                                print '用户%s不存在'%user_cmd2[1]
                      elif user_cmd2[0]=='userlist':
                        s.sendall("%s %s %s %s %s"%(username,user_cmd2[0],0,0,0))
                        result=s.recv(4096)
                        os.system('clear')
                        print '账户列表:'
                        print result
                      elif user_cmd2[0] == 'back':
                          os.system('clear')
                          break
                      elif user_cmd2[0] == 'quit':
                          sys.exit()
                      else:
                          print '命令不存在，请重新输入'
                else:
                   print '对不起,您不是管理员'
                
            elif user_cmd[0] =='quit':
                sys.exit()
            else:
                print '命令不存在，请重新输入！！'
                continue
         
    else:
      print '验证失败'
      continue
    
s.close()
#print data
