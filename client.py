#!/usr/bin/python
#coding:utf-8
#For FTP client
from __future__ import division
import  socket
import  os
import  hashlib
import  time
from hashlib import md5
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
      password=raw_input('input your password:').strip()
      if len(username) >= 6 and len(password) >=6:
         break
      else:
         print '用户名或密码长度至少为6位！'
    ###验证用户名密码
    password=hashlib.md5(password).hexdigest()
    print '+++++++++++++++++++++++++++++++++++++'
    s.sendall("%s %s"%(username,password))
    print '-------------------------------------'
    user_check_result=len(s.recv(1024))
    if user_check_result > 2:
        print '验证成功'
        while True:
            notice='''
               欢迎使用FTP客户端系统
                           --基于socket
              使用方法介绍
              1.上传功能:put filename
              2.下载功能:get filename
              3.列出所有文件:list
              4.删除文件:delete filename
              '''
            print notice
            string=raw_input('input your command:').strip()
            if len(string) == 0:
               print '请输入命令内容！！'
               continue
            user_cmd=string.split()
            ###################上传模块开始###########################
            if user_cmd[0] =='put':
                if len(user_cmd) == 2:
                  try:
                    f_size=os.stat(user_cmd[1]).st_size
                    f_md5=md5_file(user_cmd[1])
                    s.sendall("%s %s %s %s %s"%(username,user_cmd[0],user_cmd[1],f_size,f_md5))
                    while True:
                      md5_check_result=s.recv(1024)
                      tmp=repr(md5_check_result)
                      md5_check_result=len(md5_check_result)
                      print md5_check_result
                      print '++++++++++++++++++++++++++++++++'
                      print tmp.split(',')[4].strip().strip("'")
                      print '++++++++++++++++++++++++++++++++'
                      if tmp.split(',')[4].strip().strip("'") != f_md5: #当数据库中没有该文件的md5值，所以查询返回结果为空列表，如果不为空返回来存在的记录，判断用户名即可
                          print '---------------------------------------'
                          print md5_check_result
                          print '正在发送。。。'
                          f=file(user_cmd[1],'rb')
                          f_size_shishi = f_size
                          time1=time.time()
                          while True:
                             data=f.read(buffersize)
                             if not data:break
                             s.send(data)
                             f_size_shishi = f_size_shishi - buffersize
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
                          print " 已存在的文件,服务器端文件名为:\033[32;1m%s\033[0m"%tmp.split(',')[2].strip().strip("'")
                          print '------------------------------'
                          break
                  except (IOError,OSError),e:
                        print '输入的文件名错误,请检查',e
                        continue
            elif user_cmd[0] =='list':
                    s.sendall("%s %s %s %s %s"%(username,user_cmd[0],0,0,0))
                    result=s.recv(4096)
                    print '文件列表:'
                    print result
            else:
                print '命令不存在，请重新输入！！'
                continue
         ###################上传模块结束##########################
    else:
      print '验证失败'
      continue
    
s.close()
#print data
