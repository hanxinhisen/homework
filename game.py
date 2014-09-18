#!/usr/bin/env python
#!coding=utf-8
import time
class Role:
    def __init__(self,name,age,shenfen):
        print '创建人物中。。。请稍后。。。'
        time.sleep(3)
        self.Name=name
        self.Age=age
        self.Shenfen=shenfen
    def print_info(self):
        print '''
          新角色出现:
          角色姓名:%s
          角色年龄:%s
          角色身份:%s
          '''%(self.Name,self.Age,self.Shenfen)
    def gongzuo(self,gongzuo):
         self.gongzuo=gongzuo
         print '现在的工作是:%s'%self.gongzuo
    def gongzi(self,gongzi):
         self.gongzi=gongzi
         print '现在的工资是:%s'%self.gongzi
class Diaosi(Role):
     def __init__(self,name,age,gfname,shenfen):
         Role.__init__(self,name,age,shenfen)
         self.name=name
         self.gfname=gfname
         self.age=age
         self.shenfen=shenfen
     def love(self):
          print '%s 女票是 %s'%(self.name,self.gfname)
              
class Laoban1(Role):
     def __init__(self,name,age,shenfen):
         Role.__init__(self,name,age,shenfen)
     def gongsiming(self,gongsinimg):
         self.Gongsiming=gongsinimg
         print '公司名称:%s'%self.Gongsiming
     def mianshi(self):
         print '网吧老板要求进行面试'
         print '面试开始。。。。'
         print '%s 开始问问题了。。。'%self.Name
         print '''
         QQ视频收费吗:
         1.不收费 2.收费
         '''
         print '''
         Wifi和WLAN是一个意思吗?
         1.是 2.不是
         '''
         daan1=raw_input('请输入第一题答案:').strip()
         daan2=raw_input('请输入第二题答案:').strip()
         if int(daan1) is 1 and int(daan2) is 2:
                print '恭喜，%s 被录用了，工资1000'%name
                result = 'success'
                D=Diaosi(self.Name,self.Age,'x',self.Shenfen)
                D.gongzuo('网管')
                D.gongzi('1000')
                D.love()
         else:
                print '这点常识都没有？？继续做你屌丝吧'
                result = 'faile'
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
            while True:
                name=raw_input('那就先给角色起个名字吧:').strip()
                age=raw_input('最好再输入一下角色年龄:').strip()
                gfname=raw_input('顺便在给女票起个响亮而文雅的名字吧:').strip()
                if len(name) is  not 0 and len(age) is not 0 and len(gfname) is not 0:
                    break
                else:
                    print '角色信息不能为空!'
                    continue
            #S=Role(%s,%s,%s)%(name,age,provinces)
            D=Diaosi(name,age,gfname,'屌丝')
            D.print_info()
            print '故事发生在好几年前,%s和%s是男女朋友关系,这一年的高考结束了。。'%(name,gfname)
            time.sleep(2)
            print '%s:   %s,我要去北京上大学了,你要不是高考那天睡过头了,咱还能一起上学的'%(gfname,name)
            time.sleep(2)
            print '%s:   %s,不要酱紫啊,你去上学就没人照顾你了啊'%(name,gfname)
            time.sleep(2)
            print '最终%s和%s还是败给了现实,%s最终去了北京上大学了'%(name,gfname,gfname)
            print '%s为了给%s教学费，偷偷的来到北京想找一份工作'%(name,gfname)
            time.sleep(2)
            choose1=raw_input('%s,现在有一份网吧当网管的工作想做吗?'%name).strip()
            if choose1 is 'y':
              L=Laoban1('Old boy','35','网吧老板')
              L.gongsiming('etiantian 网吧')
              L.print_info()
              L.mianshi()
              print '=============================================='
            else:
               print '什么，这都不想干，那你只能做你的屌丝了。。。'
          else:
              print '对不起，该角色暂未开放。。。。程序员正在苦逼的开发当中。。'
