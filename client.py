#!/usr/bin/python
#coding:utf-8
#For FTP client
import  socket
import os
import hashlib
from hashlib import md5
host='192.168.1.103'
port=8887
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))
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
    m = md5()
    a_file = open(filename, 'rb')
    m.update(a_file.read())
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
            string=raw_input('input your command:').strip()
            if len(string) == 0:
               print '请输入命令内容！！'
               continue
            user_cmd=string.split()
            ###################上传模块开始###########################
            if user_cmd[0] =='put':
                if len(user_cmd) == 2:
                  try:
                    f=file(user_cmd[1],'rb')
                    f_size=os.stat(user_cmd[1]).st_size
                    f_md5=md5_file(user_cmd[1])
                    s.sendall("%s %s %s %s %s"%(username,user_cmd[0],user_cmd[1],f_size,f_md5))
                    while True:
                      md5_check_result=len(s.recv(1024))
                      print md5_check_result
                      if md5_check_result == 2: #当数据库中没有该文件的md5值，所以查询返回结果为空列表，2表示前后括号长度，如果为2则上传
                          print '---------------------------------------'
                          print md5_check_result
                          print '正在发送。。。'
                          s.sendall(f.read())
                          print '++++++++++++++++++++++++++'
                          if len(s.recv(1024)) == 6:   #如果上传完成,server端会发送'finish'字符串，可以判断长度继而判断上传与否
                             print '上传完成'
                             break
                          else:
                              print '上传失败'
                              break
                      else:
                          print md5_check_result
                          print '------------------------------'
                          print '文件已存在'
                          break
                  except IOError,e:
                        print '输入的文件名错误,请检查'
                        continue
            else:
                print '命令不存在，请重新输入！！'
                continue
         ###################上传模块结束##########################
    else:
      print '验证失败'
      continue
    
s.close()
#print data
