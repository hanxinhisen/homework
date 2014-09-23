#!/usr/bin/env python
#coding:utf-8
import SocketServer
import os
import time
import commands
import MySQLdb
import time
from hashlib import md5
class MySockServer(SocketServer.BaseRequestHandler):
    def md5_file(self,filename):   #校验文件md5值
          m = md5()
          a_file = open(filename, 'rb')
          m.update(a_file.read())
          a_file.close()
          return m.hexdigest()
    def ftp_down(self,obj,msg_length,des_file):
            while msg_length != 0:
                if msg_length <= 4096:
                    print 'lalallllallalall'
                    data= obj.recv(msg_length)
                    msg_length =0
                    print msg_length
                else:
                    data= obj.recv(4096)
                    msg_length -= 4096
                    print msg_length
                des_file.write(data)
            return 'finish'
    def db_qurey_md5_check(self,username,md5):
      try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
        cur=conn.cursor()
        conn.select_db('ftp_server')
        cur.execute("SELECT * FROM `ftp_info` where `name` ='%s' and  `filemd5` = '%s'"%(username,md5))
        result= cur.fetchall()
        print result
        tmp=[]
        for row in result:
            tmp.append(row)
        cur.close()
        conn.close()
        return tmp
      except MySQLdb.Error,e:
         print 'mysql error mes:',e
    def db_insert_fileinfo(self,username,filename,filesize,filemd5):
        try:
            conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
            cur=conn.cursor()
            conn.select_db('ftp_server')
            tmp=('%s'%username,'%s'%filename,'%s'%filesize,'%s'%filemd5)
            print '44444444444444444444444444444444444444'
            print tmp
            print '444444444444444444444444444444444444444'
            cur.execute('insert into ftp_info value(null,%s,%s,%s,%s)',tmp)
            conn.commit()
            cur.close()
            conn.close()
            return 'success'
        except MySQLdb.Error,e:
            print 'mysql error mes:',e
    def user_check(self,username,password):
        try:
          conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
          cur=conn.cursor()
          conn.select_db('ftp_server')
          cur.execute("SELECT * FROM `user_info` where `name` ='%s' and  `passwd` = '%s'"%(username,password))
          result= cur.fetchall()
          print result
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
          while True:
              while True:
                user_info_recived=self.request.recv(4096).strip() #将客户端输入的用户名和密码进行验证
                print user_info_recived
                username,passwd=user_info_recived.split()[:2] #防止用户名输入空格，产生影响，自动截取前两个元素
                result1=self.user_check(username,passwd)
                self.request.send(str(result1))
                print user_info_recived
                if len(result1) == 1:
                    break
              while True: #循环接收命令
                print '------------------wait for commands--------------'
                cmd_recived=self.request.recv(4096).strip()
                if not cmd_recived:
                    print 'Lost Connection from:',self.client_address
                    break
                print cmd_recived
                print '1111111111111111111111111111111111111111'
                username,cmd,filename,filesize,filemd5=cmd_recived.split()
                print filesize
                time.sleep(10)
                if cmd == 'put':
                  result2=self.db_qurey_md5_check(username,filemd5)
                  print result2
                  self.request.send(str(result2))
                  print '22222222222222222222222222222222222222222'
                  ###result2为列表 如果数据库中没有将要上传文件的md5则返回空列表
                  if len(result2) == 0:
                    if os.path.exists('/home/ftp/%s'%username): #判断用户目录是否存在
                      print '5555555555555555555555555'
                      pass
                    else:
                      os.mkdir('/home/ftp/%s'%username)
                    f=file('/home/ftp/%s/%s'%(username,filename),'wb+')
                    write_to_file=self.ftp_down(self.request,int(filesize),f)
                    f.close()
                    print '3333333333333333333333333333333333333333'
                    print write_to_file
                    if write_to_file == 'finish':
                      #f=file('/home/ftp/%s/%s'%(username,filename),'rb')
                      print '6666666666666666666666666666666'
                      print self.md5_file('/home/ftp/%s/%s'%(username,filename))
                      print filemd5
                      print '7777777777777777777777777777777777'
                      if self.md5_file('/home/ftp/%s/%s'%(username,filename)) == filemd5: ###判断接收到的文件md5是否与源文件相同
                          insert_result=self.db_insert_fileinfo(username,filename,filesize,filemd5)
                          if insert_result == 'success': #判断信息是否插入成功
                              self.request.send('finish')   
                              print '55555555555555555555555555555555555'
                          else:
                              print '插入数据库错误'
                              self.request.send('error')
                      else:
                          print '接收到的文件和源文件md5不一致'
                          self.request.send('error')                      
if __name__ == '__main__':
    h='0.0.0.0'
    p=8887
    s=SocketServer.ThreadingTCPServer((h,p),MySockServer)
    s.serve_forever()
