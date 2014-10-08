#!/usr/bin/env python
#coding:utf-8
#0928 finally
#0929 finally add get file
#0930 finally add xiazai jindutiao
#1002 finally add delete
#1003 finall add rename
import SocketServer
import os
import time
import commands
import MySQLdb
import hashlib
from prettytable import PrettyTable
from hashlib import md5
class MySockServer(SocketServer.BaseRequestHandler):
    def md5_file(self,filename):   #校验文件md5值
          print '正在计算 %s MD5值。。。'%filename
          m = hashlib.md5()
          a_file = open(filename, 'rb')
          while True:
            blk=a_file.read(4096)
            if not blk:break
            m.update(blk)
          a_file.close()
          return m.hexdigest()
    def ftp_down(self,username,filename,msg_length,status,finish_size):
            self.username=username
            self.filename=filename
            self.msg_length=msg_length    #待接收文件大小
            if os.path.exists('/home/ftp/%s'%username): #判断用户目录是否存在
                pass
            else:
                os.makedirs('/home/ftp/%s'%username)
            if status == 'normal':
                f=file('/home/ftp/%s/%s.tmp'%(self.username,self.filename),'wb+')
                while True:
                    if self.msg_length > 4096:
                       filedata = self.request.recv(4096)
                    else:
                       filedata = self.request.recv(self.msg_length)
                    if not filedata:break
                    f.write(filedata)
                    f.flush()
                    self.msg_length=self.msg_length-len(filedata)
                    if self.msg_length ==0:
                      break
                f.close()
                if os.stat('/home/ftp/%s/%s.tmp'%(username,filename)).st_size == msg_length:
                 return 'finish'
            elif status == 'duandian':
                daichuan_length=self.msg_length-finish_size #待传的文件大小
                f=file('/home/ftp/%s/%s.tmp'%(self.username,self.filename),'ab+')
                f.seek(finish_size)
                while True:
                  if daichuan_length > 4096:
                     filedata = self.request.recv(4096)
                  else:
                     filedata = self.request.recv(daichuan_length)
                  if not filedata:break
                  f.write(filedata)
                  f.flush()
                  daichuan_length=daichuan_length-len(filedata)
                  if daichuan_length ==0:
                      break
                f.close()
                if os.stat('/home/ftp/%s/%s.tmp'%(username,filename)).st_size == msg_length:
                 return 'finish'
    def db_qurey_md5_check(self,username,md5): #for upload
      try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
        cur=conn.cursor()
        conn.select_db('ftp_server')
        cur.execute("SELECT * FROM `ftp_info` where `name` ='%s' and  `filemd5` = '%s'"%(username,md5))
        result= cur.fetchall()
        tmp=[]
        for row in result:
            tmp.append(row)
        cur.close()
        conn.close()
        return tmp
      except MySQLdb.Error,e:
         print 'mysql error mes:',e
    def db_qurey_filename_check(self,username,filename): #for getdown
      try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
        cur=conn.cursor()
        conn.select_db('ftp_server')
        cur.execute("SELECT * FROM `ftp_info` where `name` ='%s' and  `filename` = '%s'"%(username,filename))
        result= cur.fetchall()
        tmp=[]
        for row in result:
            tmp.append(row)
        cur.close()
        conn.close()
        return tmp
      except MySQLdb.Error,e:
         print 'mysql error mes:',e
    def db_insert_fileinfo(self,username,filename,filesize,filemd5,ip):
        try:
            conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
            cur=conn.cursor()
            conn.select_db('ftp_server')
            date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) #get  time
            tmp=('%s'%username,'%s'%filename,'%s'%filesize,'%s'%filemd5,'%s'%ip,'%s'%date)
            cur.execute('insert into ftp_info value(null,%s,%s,%s,%s,%s,%s)',tmp)
            conn.commit()
            cur.close()
            conn.close()
            return 'success'
        except MySQLdb.Error,e:
            print 'mysql error mes:',e
    def db_delete_fileinfo(self,username,filename):
        try:
            conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
            cur=conn.cursor()
            conn.select_db('ftp_server')
            tmp=('%s'%username,'%s'%filename)
            cur.execute('delete from ftp_info where name=%s and filename=%s',tmp)
            conn.commit()
            cur.close()
            conn.close()
            return 'success'
        except MySQLdb.Error,e:
            print 'mysql error mes:',e
    def db_update_fileinfo(self,username,filename,newfilename):  #文件信息更改
        try:
            conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
            cur=conn.cursor()
            conn.select_db('ftp_server')
            tmp=('%s'%newfilename,'%s'%username,'%s'%filename)
            cur.execute('update ftp_info set filename=%s where name=%s and filename=%s',tmp)
            conn.commit()
            cur.close()
            conn.close()
            return 'success'
        except MySQLdb.Error,e:
            print 'mysql error mes:',e
    def file_list(self,username):
        try:
            conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
            cur=conn.cursor()
            conn.select_db('ftp_server')
            tmp=('%s'%username)
            cur.execute('select * from  ftp_info where name=%s',tmp)
            conn.commit()
            result=cur.fetchall()
            cur.close()
            conn.close()
            return result
        except MySQLdb.Error,e:
            print 'mysql error mes:',e
    def user_check(self,username,passwd):#将客户端输入的用户名和密码进行验证
        try:
          conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
          cur=conn.cursor()
          conn.select_db('ftp_server')
          cur.execute("SELECT * FROM `user_info` where `name` ='%s' and  `passwd` = '%s'"%(username,passwd))
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
    def user_passwd_change(self,username,passwd):#将客户端输入的用户名和密码进行验证
        try:
          conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
          cur=conn.cursor()
          conn.select_db('ftp_server')
          tmp=('%s'%passwd,'%s'%username,)
          cur.execute('update user_info set passwd=%s where name=%s',tmp)
          conn.commit()
          cur.close()
          conn.close()
          return 'success'
        except MySQLdb.Error,e:
          print 'mysql error mes:',e
    def user_exist_check(self,username): #for admin add or delete user
      try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
        cur=conn.cursor()
        conn.select_db('ftp_server')
        print username
        cur.execute("SELECT * FROM `user_info` where `name` ='%s'"%(username))
        result= cur.fetchall()
        tmp=[]
        for row in result:
            tmp.append(row)
        cur.close()
        conn.close()
        if len(tmp) >= 1:
           return 'cunzai'
        else:
           return 'bucunzai'
      except MySQLdb.Error,e:
         print 'mysql error mes:',e
    def user_add(self,username,passwd): #for admin add or delete user
        try:
            conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
            cur=conn.cursor()
            conn.select_db('ftp_server')
            date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) #get  time
            tmp=('%s'%username,'%s'%passwd,'0')
            cur.execute('insert into user_info value(null,%s,%s,%s)',tmp)
            conn.commit()
            cur.close()
            conn.close()
            return 'success'
        except MySQLdb.Error,e:
          print 'mysql error mes:',e
    def user_delete(self,username): #for admin add or delete user
        try:
            conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
            cur=conn.cursor()
            conn.select_db('ftp_server')
            cur.execute("DELETE from user_info where name='%s'"%username)
            conn.commit()
            cur.close()
            conn.close()
            return 'success'
        except MySQLdb.Error,e:
          print 'mysql error mes:',e
    def user_list(self):
        try:
            conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
            cur=conn.cursor()
            conn.select_db('ftp_server')
            cur.execute('select name from  user_info')
            conn.commit()
            result=cur.fetchall()
            cur.close()
            conn.close()
            return result
        except MySQLdb.Error,e:
            print 'mysql error mes:',e
    def handle(self):
        print 'i have got a connection from ',self.client_address
        while True:
            print 'wait for check username'
            user_info_recived=self.request.recv(4096).strip()
            print 'check username start...'
            if len(user_info_recived) == 0:
               print '验证过程失去连接:',self.client_address
               result1='error'
               break
            else:
                username,passwd=user_info_recived.split()[:2] #防止用户名输入空格，产生影响，自动截取前两个元素
                result1=self.user_check(username,passwd)
                self.request.send(str(result1))
                print 'check username finish...'
            if result1 is 'success':
                while True: #循环接收命令
                  print '------------------wait for commands--------------'
                  cmd_recived=self.request.recv(4096).strip()
                  print cmd_recived
                  if len(cmd_recived) == 0:
                      print '命令过程失去连接：',self.client_address
                      break
                  else:
                      username,cmd,filename,filesize,filemd5=cmd_recived.split()
                      if cmd == 'put':
                        result2=self.db_qurey_md5_check(username,filemd5)#如果不存在记录，则返回null，如果存在直接返回文件名
                        if int(len(result2))==0: #文件不存在
                           self.request.send('null')
                           ###result2为列表 如果数据库中没有将要上传文件的md5则返回空列表
                           if self.request.recv(4096).strip() == 'duandian_request': #可断点交互:客户端发送文件时,服务端经查询没有该文件,首先发送null告知客户端可以上传，然后客户端再请求是否可以断点续传
                            print '进入断点检测'
                            #print os.popen('ls -lh /home/ftp/hanxin').read()
                            if os.path.exists('/home/ftp/%s/%s.tmp'%(username,filename)):
                                self.request.send('keduandian')
                                upload_choice=self.request.recv(4096).strip()
                                if upload_choice == 'redo':
                                    self.request.send('start') #收到redo命令后，让客户端开始发送文件
                                    print '断点续传---重新上传'
                                    status='normal'
                                    finish_size=0
                                    write_to_file=self.ftp_down(username,filename,int(filesize),status,finish_size)
                                    if write_to_file == 'finish':
                                      os.rename('/home/ftp/%s/%s.tmp'%(username,filename),'/home/ftp/%s/%s'%(username,filename))
                                      if self.md5_file('/home/ftp/%s/%s'%(username,filename)) == filemd5: ###判断接收到的文件md5是否与源文件相同
                                          insert_result=self.db_insert_fileinfo(username,filename,filesize,filemd5,self.client_address[0])
                                          if insert_result == 'success': #判断信息是否插入成功
                                              self.request.send('finish')
                                          else:
                                              print '插入数据库错误'
                                              self.request.send('error')
                                          continue   #数据库插入成功与否都要重新接收command
                                      else:
                                          print '接收到的文件和源文件md5不一致'
                                          self.request.send('error')
                                elif upload_choice == 'xuchuan':
                                    print '断点续传--续传'
                                    self.request.send('start')
                                    f_size_finish=os.stat('/home/ftp/%s/%s.tmp'%(username,filename)).st_size
                                    self.request.send(str(f_size_finish))
                                    status='duandian'
                                    finish_size=f_size_finish
                                    write_to_file=self.ftp_down(username,filename,int(filesize),status,finish_size)
                                    if write_to_file == 'finish':
                                      os.rename('/home/ftp/%s/%s.tmp'%(username,filename),'/home/ftp/%s/%s'%(username,filename))
                                      if self.md5_file('/home/ftp/%s/%s'%(username,filename)) == filemd5: ###判断接收到的文件md5是否与源文件相同
                                          insert_result=self.db_insert_fileinfo(username,filename,filesize,filemd5,self.client_address[0])
                                          if insert_result == 'success': #判断信息是否插入成功
                                              self.request.send('finish')
                                          else:
                                              print '插入数据库错误'
                                              self.request.send('error')
                                          continue   #数据库插入成功与否都要重新接收command
                                      else:
                                          print '接收到的文件和源文件md5不一致'
                                          self.request.send('error')
                                          continue
                            else:
                                self.request.send('bukeduandian')
                                print '正常接收。。。'
                                status='normal'
                                finish_size=0
                                write_to_file=self.ftp_down(username,filename,int(filesize),status,finish_size)
                                if write_to_file == 'finish':
                                  os.rename('/home/ftp/%s/%s.tmp'%(username,filename),'/home/ftp/%s/%s'%(username,filename))
                                  print 'tmp rename'
                                  if self.md5_file('/home/ftp/%s/%s'%(username,filename)) == filemd5: ###判断接收到的文件md5是否与源文件相同
                                      insert_result=self.db_insert_fileinfo(username,filename,filesize,filemd5,self.client_address[0])
                                      if insert_result == 'success': #判断信息是否插入成功
                                          self.request.send('finish')
                                      else:
                                          print '插入数据库错误'
                                          self.request.send('error')
                                      continue   #数据库插入成功与否都要重新接收command
                                  else:
                                      print '接收到的文件和源文件md5不一致'
                                      self.request.send('error')
                        else:  #文件存在
                            a=str(result2).split(',')
                            self.request.send(str(a[2]))
                      elif cmd=='list':
                          #result=os.popen('ls -lh /home/ftp/%s'%username).read()
                          #result=os.popen("ls -lh /home/ftp/%s | grep -v '.tmp'"%username).read()
                          result=self.file_list(username)
                          print result
                          a = PrettyTable(['序号','账户', '文件名称', '文件大小(bit)', '文件MD5值', '上传端IP','上传时间'])
                          result_len=len(result)
                          if result_len > 0:
                            for i in range(result_len):
                              r=[]
                              for t in result[i]:
                                  r.append(t)
                              a.add_row([i+1,r[1],r[2],r[3],r[4],r[5],r[6]])
                          else:
                             a.add_row(['None','None','None','None','None','None','None'])
                          self.request.sendall(str(a))
                      elif cmd=='get':
                          result=self.db_qurey_filename_check(username,filename)
                          if int(len(result))==0:
                            self.request.send('null')
                          else:
                            a=str(result).split(',')
                            self.request.send(str(a[3]))
                            f=file('/home/ftp/%s/%s'%(username,filename),'rb')
                            #time.sleep(0.2)  #延时发送文件，防止客户端在获取文件长度时将文件同时获取到
                            if self.request.recv(4096).strip() == 'start':
                                while True:      #客户端收到文件大小后，会发送‘start’命令让服务器发送文件
                                    data=f.read(4096)
                                    if not data:break
                                    self.request.send(data)
                                else:
                                    print '传送完成'
                      elif cmd=='delete':
                          result=self.db_qurey_filename_check(username,filename)
                          if int(len(result))==0:
                            self.request.send('null')
                          else:
                            self.request.send('exist')
                            if self.request.recv(4096).strip() == 'yes':
                               os.remove('/home/ftp/%s/%s'%(username,filename))
                               del_result=self.db_delete_fileinfo(username,filename)
                               if not os.path.exists('/home/ftp/%s/%s'%(username,filename)) and del_result == 'success': #判断是否删除成功
                                   self.request.send('success')
                      elif cmd=='rename':
                          new_filename=filesize  #客户端按照统一格式发送，新密码为上面定义的fileszie
                          result=self.db_qurey_filename_check(username,filename)
                          result2=self.db_qurey_filename_check(username,new_filename) #判断新文件名是否存在
                          if int(len(result))!=0 and int(len(result2)) ==0:
                             self.request.send('exist')
                             if self.request.recv(4096).strip() == 'yes':
                                 os.rename('/home/ftp/%s/%s'%(username,filename),'/home/ftp/%s/%s'%(username,new_filename))
                                 rename_result=self.db_update_fileinfo(username,filename,new_filename)
                                 if  os.path.exists('/home/ftp/%s/%s'%(username,new_filename)) and rename_result == 'success':
                                   print '重命名中。。。。'
                                   self.request.send('success')
                          else:
                             self.request.send('null')
                      elif cmd=='repasswd':
                          new_passwd=filesize
                          result=self.user_passwd_change(username,new_passwd)
                          if int(len(result))!=0:
                              print '修改成功'
                              self.request.send('success')
                          else:
                              print '修改失败'
                      elif cmd=='useradd':
                          a_username=filename #想要添加的用户名
                          a_passwd=filemd5#想要添加的密码
                          user_exist_result=self.user_exist_check(a_username)
                          if user_exist_result == 'cunzai':
                              self.request.send('cunzai')
                          else:
                              print '不存在 可以创建'
                              self.request.send('bucunzai')
                              useradd_result=self.user_add(a_username,a_passwd)
                              if useradd_result == 'success':
                                self.request.send('success')
                      elif cmd=='deluser':
                          d_username=filename
                          user_exist_result=self.user_exist_check(d_username)
                          if user_exist_result == 'cunzai':
                              self.request.send('cunzai')
                              if self.request.recv(4096).strip() == 'yes':
                                 userdel_result=self.user_delete(d_username)
                                 if userdel_result == 'success':
                                   self.request.send('success')
                          else:
                              self.request.send('bucunzai')
                      elif cmd=='userlist':
                          result=self.user_list()
                          print result
                          a = PrettyTable(['序号','账号'])
                          result_len=len(result)
                          r=[]
                          for i in range(result_len):
                            a.add_row([i+1,str(result[i]).split("'")[1]])
                          self.request.sendall(str(a))

            else:
                print '用户验证错误！'
if __name__ == '__main__':
    h='0.0.0.0'
    p=8889
    s=SocketServer.ThreadingTCPServer((h,p),MySockServer)
    s.serve_forever()
