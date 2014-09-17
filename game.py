#!/usr/bin/env python
#!coding=utf-8
import time
class Role:
    def __init__(self,name,age,shenfen):
        self.Name=name
        self.Age=age
        self.Shenfen=shenfen
    def print_info(self):
        print '''
                 角色姓名:%s
                 角色年龄:%s
                 角色身份:%s
                 '''%(self.Name,self.Age,self.Shenfen)
class Diaosi(Role):
     def __init__(self,name,age,gfname,shenfen):
         Role.__init__(self,name,age,shenfen)
         self.gfname=gfname
     def gongzuo(self,gongzuo):
         self.gongzuo=gongzuo
         print '现在的工作是:%s'%self.gongzuo
class Laoban1(Role):
     def __init__(self,name,age,shenfen):
         Role.__init__(self,name,age,shenfen)
     def gongsiming(self,gongsinimg):
         self.Gongsiming=gongsinimg
         print '公司名称:'%self.Gongsiming
     def mianshi(self):
         print '面试开始。。。。'
         print '%s 开始问问题了。。。'%self.Name
         print '''
         如果顾客电脑有问题了怎么办:
         1.重启 2.换机器
         '''
         print '''
         冰红茶和加多宝那个贵?
         1.冰红茶 2.加多宝
         '''
while True:
    print '欢迎进入游戏世界！'
    print '''
          请选择一个角色吧：
          1.穷屌丝
          2.白富美
          3.高富帅
          '''
    while True:
        try:
          choose=int(raw_input('请选择：').strip())
        except ValueError:
            print '亲，还能一起玩耍吗，输入个数字有这么难吗'
            continue
        if choose not in [1,2,3]:
            print '你输入的数字好像应该貌似不存在吧...'
            continue
        else:
          if choose is 1:
            print '呵呵。。。很有自知之明嘛'
            while True:
                name=raw_input('那就先给角色起个名字吧:').strip()
                age=raw_input('最好再输入一下角色年龄:').strip()
                gfname=raw_input('顺便在给他女票起个响亮而文雅的名字吧:').strip()
                if len(name) is  not 0 and len(age) is not 0 and len(gfname) is not 0:
                    break
                else:
                    print '角色信息不能为空!'
                    continue
            #S=Role(%s,%s,%s)%(name,age,provinces)
            D=Diaosi(name,age,gfname,'屌丝')
            D.print_info()
            print '故事发生在好几年前,%s和%s是男女朋友'%(name,gfname)
            time.sleep(2)
            print '这年高考%s的女票考上了北京城市学院（俗称海跑）,but %s 由于高考早上睡过头而没有参加成高考,一对新异地恋马上就要产生了。'%(name,name)
            time.sleep(2)
            print '%s为了给%s教学费，偷偷的来到北京想找一份工作'%(name,gfname)
            time.sleep(2)
            print '于是他来到了一家网吧门口,推开网吧的大门。找到了网吧老板'
            L=Laoban1('Old boy','35','网吧老板')
            L.print_info()
            L.mianshi()
            daan1=raw_input('请输入第一题答案:').strip()
            daan2=raw_input('请输入第二题答案:').strip()
            if int(daan1) is 1 and int(daan2) is 2:
                print '恭喜，%s 被录用了，工资1000'%name
            else:
                print '这点常识都没有？？继续做你屌丝吧'

          else:
              print '对不起，该角色暂未开放。。。。程序员正在苦逼的开发当中。。'
