#!/usr/bin/env python
#coding:utf-8
def choose():
    notice="""
              Welcome to ATM SYSTEM
                   0:快捷取现
                   1:信用卡商城
                   2:查询剩余额度
                   3.查询账单
                   4.还款
                   5.退出
    """
    while True:
        print notice
        while True:
          choose=raw_input('Please choose a number:').strip()
          if len(choose) == 0:
              print '请输入正确数字'
              continue
          else:
              break
        print '您输入的数字是\033[032;1m%s\033[0m'%choose
        if choose not in ['0','1','2','3','4','5']:
            print 'Please input a correct number!'
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
                sys.exit()
def cash(username):
    import time
    edu = eduload(username)
    #print '您能最多取现%s元'%(float(edu)/1.01)
    #print '您能最多取现%s元'%(float(edu)/1.01)
    buydate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    while True:
        jiner=raw_input('How much money do you want to draw:').strip()
        if len(jiner) == 0:continue
        if float(edu) < float(jiner):
            print '超过额度余额！'
            continue
        else:
            shouxufei=float(jiner)*0.01
            benxi=float(jiner) +float(shouxufei)
            #if float(edu) >= float(benxi):
            shengyu=float(edu) - float(benxi)
            loger(username,buydate,'取现',float(jiner),shouxufei,benxi,shengyu)
            if float(shengyu) < 0:
                shengyu=0
                eduupdate(username,shengyu)
                break
            else:
                eduupdate(username,shengyu)
                break
    #else:
    #    print '超过额度余额！'
def buy(username):
    import time
    print 'Welcome %s to our Credit Card Mall!!'%username
    print 'You can buy follow shops!!'
    edu = eduload(username)
    shop=['car','iphone','meizu','drinks','books','notepad']
    jiage=[500000,4999,2000,100,55.55,3000]
    shoplist=[ ]
    num=shop.index(shop[-1])+1
    for i in range(num):
       print shop[i],jiage[i]
    shengyu=edu
    while True:
        want_to_buy=raw_input('what do you want to buy--->').strip()
        if want_to_buy == 'quit':
            print shoplist
            break
        if want_to_buy in shop:
            jiner = jiage[shop.index(want_to_buy)]
            if float(shengyu) >= float(jiner):
                shengyu=float(shengyu) - float(jiner)
                print 'you have %s kuai now'%shengyu
                shoplist.append(want_to_buy)
                buydate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                shouxufei=0
                benxi=jiner
                loger(username,buydate,'消费:%s'%want_to_buy,float(jiner),shouxufei,benxi,shengyu)
                eduupdate(username,shengyu)
            else:
                print 'you are too poor to buy it!!'
                continue
        else:
            print "dont in list,input again!"
def left_amount():
    print 'left_amount'
    edu = eduload(username)
    print '您额度目前为%s元'%(edu)
def account_list(username):
    from prettytable import PrettyTable
    import time
    with open('credit_card.log') as f:
       count = 0
       print '查询结果如下：'
       time1=time.time()
       a = PrettyTable(['序号','账户', '消费日期', '消费类型(产品)', '消费金额', '手续费','应还金额'])
       zonge=[ ]
       for line in f.readlines():
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
               time2=time.time()
               cost_time=time2 - time1
               zonge=sum(zonge)
               a.add_row(['','','','','','共计(单位：元)：',zonge])
               today = time.strftime('%d',time.localtime(time.time()))
               huankuanri=30-int(today)
               print a
               print '距离还款日还有\033[31;1m%s\033[0m天'%huankuanri
               print '总共找到\033[032;1m%s\033[0m条记录,本次查询耗时\033[032;1m%s\033[0m秒'%(count,cost_time)
def repay():
    import time
    edu = eduload(username)
    want_to_repay=raw_input('请输入您的还款金额：').strip()
    new_edu = float(edu) + float(want_to_repay)
    eduupdate(username,new_edu)
    buydate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    shouxufei=0
    loger(username,buydate,'还款',-float(want_to_repay),shouxufei,-float(want_to_repay),new_edu)
    edu = eduload(username)
    print '您最新的额度为%s元'%(edu)
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
import sys
user_file='account.txt'
lock_file='account_lock.txt'
with open(user_file) as f:
    user_list=f.readlines()
with open(lock_file) as f:
    lock_list=[]
    for line in f.readlines():
        line=line.strip('\n')
        lock_list.append(line)
    print "\033[32;1mThanks for using this system!\033[0m"
while True:
    username=raw_input('Please input your account:').strip()
    if len(username) == 0:
        continue
    else:
        if username in lock_list:
            print 'The account is \033[31;1mlocked\033[0m'
            sys.exit()
        else:
            for line in user_list:
                line=line.split()
                if line[0] == username:
                    for i in range(3):
                        password=raw_input('Please input your password:').strip()
                        if len(password) == 0:
                            continue
                        else:
                            if  line[1] == password:
                                print '\033[32;1mWelcome to the Our System!!!\033[0m'
                                choose()
                            else:
                                print "\033[31;1mThe password may input errors!\033[0m"
                    else:
                        print '\033[32;1mAmounts of input error, system exit. Thank you for using this system!!!!\033[0m'
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





