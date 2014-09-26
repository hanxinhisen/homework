#!/usr/bin/env python
#coding:utf-8
import SocketServer
import os
import time
import commands
import MySQLdb
import time
import hashlib
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
    def ftp_down(self,username,filename,msg_length):
            self.username=username
            self.filename=filename
            self.msg_length=msg_length
            f=file('/home/ftp/%s/%s'%(self.username,self.filename),'wb+')
            while True:
                if self.msg_length > 4096:
                   filedata = self.request.recv(4096)
                else:
                   filedata = self.request.recv(self.msg_length)
                if not filedata:break
                f.write(filedata)
                self.msg_length=self.msg_length-len(filedata)
                if self.msg_length ==0:
                  break
            f.close()                  
            return 'finish'
    def db_qurey_md5_check(self,username,md5):
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
    def user_check(self):
        user_info_recived=self.request.recv(4096).strip() #将客户端输入的用户名和密码进行验证
        if len(user_info_recived) == 0:
           print 'Lost Connection from:',self.client_address
        else:
            username,passwd=user_info_recived.split()[:2] #防止用户名输入空格，产生影响，自动截取前两个元素
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
          return tmp
        except MySQLdb.Error,e:
          print 'mysql error mes:',e
    def handle(self):
            print 'i have got a connection from ',self.client_address
            print 'check username start...'
            result1=self.user_check()
            self.request.send(str(result1))
            print 'check username finish...'
            if len(result1) == 1:
                while True: #循环接收命令
                  print '------------------wait for commands--------------'
                  cmd_recived=self.request.recv(4096).strip()
                  print cmd_recived
                  if len(cmd_recived) == 0:
                      print 'Lost Connection from:',self.client_address
                      break
                  else:
                      username,cmd,filename,filesize,filemd5=cmd_recived.split()
                      if cmd == 'put':
                        result2=self.db_qurey_md5_check(username,filemd5)
                        a=str(result2).split(',')
                        print a[2]
                        self.request.send(str(result2))
                        ###result2为列表 如果数据库中没有将要上传文件的md5则返回空列表
                        if len(result2) == 0:
                          if os.path.exists('/home/ftp/%s'%username): #判断用户目录是否存在
                            pass
                          else:
                            os.mkdir('/home/ftp/%s'%username)
                          write_to_file=self.ftp_down(username,filename,int(filesize))
                          if write_to_file == 'finish':
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
                      elif cmd=='list':
                          #result=os.popen('ls -lh /home/ftp/%s'%username).read()
                          result=os.popen('ls -lh /home/ftp/%s'%username).read()
                          self.request.sendall(result)
                          print result
if __name__ == '__main__':
    h='0.0.0.0'
    p=8889
    s=SocketServer.ThreadingTCPServer((h,p),MySockServer)
    s.serve_forever()
