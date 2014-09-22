#!/usr/bin/env python
import SocketServer
import os
import time
import commands
import MySQLdb
class MySockServer(SocketServer.BaseRequestHandler):
    def ftp_down(obj,msg_length ):
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
    def user_check(self,username,password):
        try:
          conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
          cur=conn.cursor()
          conn.select_db('ftp_server')
          cur.execute("SELECT * FROM `ftp_info` where `name` ='%s' and  `passwd` = '%s'"%(username,password))
          result= cur.fetchall()
          print result
          tmp=[]
          for row in result:
              #for r in row:
              #    print r
              tmp.append(row)
          cur.close()
          conn.close()
          return tmp
        except MySQLdb.Error,e:
          print 'mysql error mes:',e
    def handle(self):
          print 'i have got a connection from ',self.client_address
          while True:
              user_info_recived=self.request.recv(4096).strip()
              print user_info_recived
              username,passwd=user_info_recived.split()
              result1=self.user_check(username,passwd)
              self.request.send(str(result1))
              print user_info_recived
              cmd_recived=self.request.recv(4096).strip()
              if not cmd_recived:
                  print 'Lost Connection from:',self.client_address
                  break
              print cmd_recived
              username,cmd,filename,filesize,filemd5=cmd_recived.split()
              if cmd == 'put':
                result2=self.db_qurey_md5_check(username,filemd5)
                print result2
                self.request.send(str(result2))
if __name__ == '__main__':
    h='0.0.0.0'
    p=8888
    s=SocketServer.ThreadingTCPServer((h,p),MySockServer)
    s.serve_forever()
