#!/usr/bin/env python
#coding:utf-8
#write 2014-09-11 23:24:00
import sys
import getpass
import time
from prettytable import PrettyTable
user_file='account.txt'
lock_file='account_lock.txt'
with open(user_file) as f:
    user_list=f.readlines()
with open(lock_file) as f:
    lock_list=[]
    for line in f.readlines():
        line=line.strip('\n')
        lock_list.append(line)
def choose():
    notice="""
                欢迎使用招商信用卡系统
                   0:快捷取现
                   1:信用卡商城
                   2:查询剩余额度
                   3.查询账单
                   4.还款
                   5.转账
                   6.退出
    """
    while True:
        print notice
        while True:
          choose=raw_input('请选择功能并输入对应数字:').strip()
          if len(choose) == 0:
              print '请输入正确数字'
              continue
          else:
              break
        if choose not in ['0','1','2','3','4','5','6']:
            print '请输入正确数字！'
            continue
        else:
            if int(choose) == 0:
                cash(username)
            elif int(choose) == 1:
                buy(username)
            elif int(choose) == 2:
                left_amount()
            elif int(choose) == 3:
                account_list(username)
            elif int(choose) == 4:
                repay()
            elif int(choose) == 5:
                zhuanzhang(username)
            elif int(choose) == 6:
                sys.exit()
def cash(username):
    edu = eduload(username)
    #print '您能最多取现%s元'%(float(edu)/1.01)
    #print '您能最多取现%s元'%(float(edu)/1.01)
    buydate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    today = time.strftime('%d',time.localtime(time.time()))
    yuedi=30-int(today)
    while True:
        jiner=raw_input("请输入取现金额(输入'quit'可退出):").strip()
        if jiner == 'quit' : break
        if jiner.isdigit() is  True and len(jiner) !=0 and int(jiner) > 0 and float(edu)>float(jiner):
            shouxufei=float(jiner)*0.01
            benxi=float(jiner) +float(shouxufei)
            shengyu=float(edu) - float(jiner)
            print '本次取现金额为\033[32;1m%s\033[0m元，手续费为\033[32;1m%s\033[0m元'%(jiner,shouxufei)
            loger(username,buydate,'取现',float(jiner),shouxufei,benxi,shengyu)
            if float(shengyu) < 0:
                shengyu=0
                eduupdate(username,shengyu)
                break
            else:
                eduupdate(username,shengyu)
                break
        else:
            print '输入内容错误或者大于额度，请重新输入！'
    #else:
    #    print '超过额度余额！'
def buy(username):
    print '尊敬的%s用户,欢迎进入招商信用卡商城!!'%username
    print '您可购买以下产品!!'
    edu = eduload(username)
    shop=['car','iphone','meizu','drinks','books','notepad']
    jiage=[500000,4999,2000,100,55.55,3000]
    shoplist=[ ]
    num=shop.index(shop[-1])+1
    for i in range(num):
       print shop[i],jiage[i]
    shengyu=edu
    while True:
        want_to_buy=raw_input("请输入商品名称(输入'quit'可退出):").strip()
        if want_to_buy == 'quit':
            if len(shoplist) > 0:
              print "您本次购物购买了：",' '.join(shoplist)
              break
            else:
              print '购物车为空!'
              break
        if want_to_buy in shop:
            jiner = jiage[shop.index(want_to_buy)]
            if float(shengyu) >= float(jiner):
                shengyu=float(shengyu) - float(jiner)
                #print 'you have %s kuai now'%shengyu
                print '成功将%s加入购物车！'%want_to_buy
                shoplist.append(want_to_buy)
                buydate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                shouxufei=0
                benxi=jiner
                loger(username,buydate,'消费:%s'%want_to_buy,float(jiner),shouxufei,benxi,shengyu)
                eduupdate(username,shengyu)
            else:
                print '您的余额无法支付此商品!!'
                continue
        else:
            print "不在商品栏中，请重新输入!"
def left_amount():
    edu = eduload(username)
    print '您额度目前为\033[32;1m%s\033[0m元'%(edu)
def account_list(username):
    with open('credit_card.log') as f:
       count = 0
       print '查询结果如下：'
       time1=time.time()
       a = PrettyTable(['序号','账户', '消费日期', '消费类型(产品)', '消费金额', '手续费','应还金额'])
       zonge=[ ]
       for line in f.xreadlines():
          line = line.split()
          if line[0]== username:
            count += 1
            zonge.append(float(line[6]))
            yinghuan=float(line[4]) + float(line[5])
            a.add_row([count,line[0],line[1]+' '+line[2],line[3],line[4],line[5],yinghuan])
       else:
            if count == 0:
               print '没有找到消费记录'
            else:
               #time2=time.time()
               #cost_time=time2 - time1
               zonge=sum(zonge)
               a.add_row(['','','','','','共计(单位：元)：',zonge])
               today = time.strftime('%d',time.localtime(time.time()))
               huankuanri=30-int(today)
               print a
               if float(zonge) < 0:
                 print '距离还款日还有\033[31;1m%s\033[0m天,本月应还\033[31;1m0\033[0m元'%huankuanri
               else:
                 print '距离还款日还有\033[31;1m%s\033[0m天,本月应还\033[31;1m%s\033[0m元'%(huankuanri,zonge)
               time2=time.time()
               cost_time=time2 - time1
               print '总共找到\033[032;1m%s\033[0m条记录,本次查询耗时\033[032;1m%s\033[0m秒'%(count,cost_time)
def repay():
    #edu = eduload(username)
    #while True:
    #    want_to_repay=raw_input('请输入您的还款金额：').strip()
    #    if want_to_repay.isdigit() is  True and len(want_to_repay) !=0 and float(want_to_repay) >0:
    #        edu = eduload(username)
    #        buydate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    #        shouxufei=0
    #        new_edu = float(want_to_repay) + float(edu)
    #        loger(username,buydate,'还款',-float(want_to_repay),shouxufei,-float(want_to_repay),new_edu)
    #        eduupdate(username,new_edu)
    #        edu = eduload(username)
    #        print '您最新的额度为\033[32;1m%s\033[0m元'%(edu)
    #        break
    #    else:
    #        print '请输入大于零的整数\033[31;1m 数字\033[0m！'
    with open('credit_card.log') as f:
        zonge=[ ]
        shouxufeizonge=[ ]
        for line in f.xreadlines():
            line = line.split()
            if line[0]== username:
               zonge.append(float(line[6]))
               shouxufeizonge.append(float(line[5]))
        zonge=sum(zonge)
        shouxufeizonge=sum(shouxufeizonge)
    edu = eduload(username)
    print '''请选择还款方式：
                1.全额还款
                2.指定金额还款
                   '''
    status=True
    while status:
        choose=raw_input('请输入1或者2:').strip()
        if choose is '1':
            print '您选择了全额还款！'
            print '全款还款金额为:%s元'%zonge
            buydate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            shouxufei=0
            new_edu = float(zonge) - float(shouxufeizonge) + float(edu)
            loger(username,buydate,'全额还款',-float(zonge),shouxufei,-float(zonge),new_edu)
            eduupdate(username,new_edu)
            edu = eduload(username)
            print '您最新的额度为\033[32;1m%s\033[0m元'%(edu)
            status = False
            break
        elif choose is '2':
            print '您选择了指定金额还款(注：指定还款金额不能大于当月所有欠款金额)'
            while True:
               want_to_repay=raw_input('请输入您的还款金额：').strip()
               #print '--------------------------------------'
               #print want_to_repay
               #print zonge
               #print '--------------------------------------'
               if want_to_repay.isdigit() is  True and len(want_to_repay) !=0 and float(want_to_repay) <= float(zonge):
                   edu = eduload(username)
                   buydate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                   shouxufei=0
                   new_edu = float(want_to_repay)  + float(edu)
                   ##判读额度超过15000的话，额度定死为15000，免得额度增加。还款时除了要还清本机外还要还清利息，还利息时额度不能涨
                   if float(new_edu) <= 15000:
                       loger(username,buydate,'定额还款',-float(want_to_repay),shouxufei,-float(want_to_repay),new_edu)
                       eduupdate(username,new_edu)
                       edu = eduload(username)
                       print '您最新的额度为\033[32;1m%s\033[0m元'%(edu)
                       status = False
                       break
                   else:
                       new_edu=15000
                       loger(username,buydate,'定额还款',-float(want_to_repay),shouxufei,-float(want_to_repay),new_edu)
                       eduupdate(username,new_edu)
                       edu = eduload(username)
                       print '您最新的额度为\033[32;1m%s\033[0m元'%(edu)
                       status = False
                       break
               else:
                   print '请输入大于零的整数\033[31;1m 数字\033[0m！'
        else:
            print '请选择1或者2'
            continue
def zhuanzhang(username):
    user_file='account.txt'
    all=[ ]
    with open(user_file) as f:
      user_list=f.readlines()
    for line in user_list:
          line=line.split()
          all.append(line[0])
    status=True
    while status:
        zhuanru1=raw_input('请输入转入账户：').strip()
        zhuanru2=raw_input('请再次输入转入账户：').strip()
        if zhuanru1.isdigit() is True and zhuanru2.isdigit() is True and  zhuanru1 == zhuanru2 and len(zhuanru1) ==6 \
                                                                                               and len(zhuanru2) ==6:
             if zhuanru2 in all:
                while True:
                    jiner=raw_input('请输入转出金额：').strip()
                    edu_chu_old=eduload(username)
                    if jiner == 'quit':
                       status=False
                       break
                    if jiner.isdigit() is  True and float(edu_chu_old) >= float(jiner) :
                        edu_chu_new=float(edu_chu_old) - float(jiner)
                        edu_ru_old=eduload(zhuanru2)
                        edu_ru_new=float(edu_ru_old) + float(jiner)
                        eduupdate(username,edu_chu_new)
                        eduupdate(zhuanru2,edu_ru_new)
                        tran_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                        loger(username,tran_date,'转出至:%s'%zhuanru2,float(jiner),0,float(jiner),edu_chu_new)
                        loger(zhuanru2,tran_date,'转入自:%s'%username,-float(jiner),0,-float(jiner),edu_ru_new)
                        print '成功从账号:\033[32;1m%s\033[0m转账至账号:\033[32;1m%s\033[0m转出\033[32;1m%s\033[0m元！'%(username,zhuanru2,jiner)
                        status = False
                        break
                    else:
                        print '金额超出额度或者输入内容错误！！'
             else:
                print '转入账户不存在！'
        else:
            print '输入内容不合法或者两次输入账户不一致，请重新输入！'
            continue
def loger(account,tran_date,shop,amount,interest,benxi,shengyuedu):
    logfile='credit_card.log'
    f=file(logfile,'a')
    mess="%s %s %s %s %s %s %s"%(account,tran_date,shop,amount,interest,benxi,shengyuedu)
    f.write(mess+'\n')
    f.close()
def eduupdate(username,newedu):
    info_file='account.txt'
    with open(info_file) as f:
      info_dic={}
      for line in f:
        line=line.strip('\n').split()
        info_dic[line[0]]=line[1:]
    info_dic['%s'%username][1]='%s'%newedu
    with open(info_file,'w') as f:
      for name,values in info_dic.items():
          new=' '
          for n in range(len(values)):
             new=new + values[n]+' '
          else:
            new_file = name + ' ' + new
            f.write(new_file+'\n')
def eduload(username):
    info_file='account.txt'
    with open(info_file) as f:
      info_dic={}
      for line in f:
        line=line.strip('\n').split()
        info_dic[line[0]]=line[1:]
      edu=info_dic['%s'%username][1]
      return edu
#####################################################################
print "\033[32;1m 欢迎使用招商信用卡系统!\033[0m"
while True:
    username=raw_input('请输入您的账号:').strip()
    if len(username) == 0:
        continue
    else:
        if username in lock_list:
            print '该用户已经被\033[31;1m 锁定\033[0m！'
            sys.exit()
        else:
            for line in user_list:
                line=line.split()
                if line[0] == username:
                    for i in range(3):
                        #password=raw_input('请输入您的密码:').strip()
                        password=getpass.getpass('请输入您的密码:').strip()
                        if len(password) == 0:
                            continue
                        else:
                            if  line[1] == password:
                                print '\033[32;1m 恭喜您，登陆成功!!!\033[0m'
                                choose()
                            else:
                                print "\033[31;1m 密码输入错误!!\033[0m"
                    else:
                        print '\033[32;1m 输入错误次数过多，欢迎使用该系统！\033[0m'
                        with open(user_file) as f:
                            user_exist=[]
                            for line in f.readlines():
                                line=line.strip('\n')
                                line=line.split()
                                user_exist.append(line[0])
                        if username in user_exist:
                            with open(lock_file,'a') as f:
                                f.write(username+'\n')
                                f.flush()
                                sys.exit()
                        else:
                                sys.exit()

