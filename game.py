#!/usr/bin/env python
#!coding=utf-8
import time
import os
class Role:
    def __init__(self,name,age,shenfen):
        os.system('clear')
        print '游戏加载中。。。请稍后。。。'
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
    def gongzuo(self,name,gongzuo):
         self.gongzuo=gongzuo
         self.name=name
         print '%s现在的工作是:%s'%(self.name,self.gongzuo)
    def gongzi(self,name,gongzi):
         self.gongzi=gongzi
         print '%s现在的工资是:%s'%(self.name,self.gongzi)
    def gushipangbai1(self,name,gfname):
        print '故事发生在好几年前,%s和%s是男女朋友关系,这一年的高考结束了。。'%(name,gfname)
        time.sleep(2)
        print '%s:   %s,我要去北京上大学了,你要不是高考那天睡过头了,咱还能一起上学的~!'%(gfname,name)
        time.sleep(2)
        print '%s:   %s,不要酱紫啊,你去上学就没人照顾你了啊!!'%(name,gfname)
        time.sleep(2)
        print '........此处省略1000字..........'
        print '最终%s和%s还是败给了现实,%s最终去了北京上大学了'%(name,gfname,gfname)
        print '%s为了给%s教学费，偷偷的来到北京想找一份工作'%(name,gfname)
        print '找工作中。。。。。。'
        time.sleep(5)
    def gushipangbai2(self,name,gfname):
        print '%s有了工资,找到了女票%s说:"我现在上班了可以给你交学费买LV了"'%(name,gfname)
        time.sleep(2)
        print '%s说对不起，我已经爱上我们公司总裁了，他说鱼塘都被我承包了'%gfname
        time.sleep(5)
    def gushipangbai3(self,name,gfname):
        print '而在这时候,%s被高富帅甩了,%s找到了%s'%(gfname,gfname,name)
        time.sleep(2)
        print '%s:  %s 其实我一直爱的是你 我们还能在一起吗?'%(gfname,name)
        time.sleep(2)
    def gushipangbai4(self,name):
        sleep(2)
        print '经过几年的奋斗,%s出任了公司的IT总监,在北京买了车买了房'%name
        sleep(2)
class Diaosi(Role):
     def __init__(self,name,age,gfname,shenfen):
         Role.__init__(self,name,age,shenfen)
         self.name=name
         self.gfname=gfname
         self.age=age
         self.shenfen=shenfen
     def love(self):
          print '%s 女票是 %s'%(self.name,self.gfname)
     def study(self,gfname):
         print 'studying.....'
         print '为了能追回%s,屌丝准备奋力一搏。。'%gfname
         print '一次偶然的发现,让屌丝看到老男孩PYTHON正在招生,于是乎他报名学习了PYTHON'
         time.sleep(5)
         print '经过四个月的艰苦学习，终于学完了,辞掉网吧工作开始找新的工作了'
         print '他来到一家互联网公司'
         time.sleep(3)
class Gafushuai(Role):
    def __init__(self,name,age,gfname,shenfen):
         Role.__init__(self,name,age,shenfen)
         self.name=name
         self.age=age
         self.shenfen=shenfen
class Laoban(Role):
     def __init__(self,name,age,shenfen):
         Role.__init__(self,name,age,shenfen)
     def gongsiming(self,gongsinimg):
         self.Gongsiming=gongsinimg
         print '公司名称:%s'%self.Gongsiming
     def mianshi1(self,name):
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
                D=Diaosi(self.Name,self.Age,'x',self.Shenfen)
                D.gongzuo(name,'网管')
                D.gongzi(name,'1000')
         else:
                print '这点常识都没有？？继续做你屌丝吧'
                result = 'faile'
     def mianshi2(self,name):
         print '面试开始。。。。'
         print '%s 开始问问题了。。。'%self.Name
         print '''
         python 属于静态语言还是动态语言？
         1.动态语言  2.静态语言
         '''
         print '''
         标准库random实现了一个随机数生成器，实例代码如下：
         import random
         random.random()
         则会得到怎样的随机数？
         1.浮点型数字    2.整型数字
         '''
         daan1=raw_input('请输入第一题答案:').strip()
         daan2=raw_input('请输入第二题答案:').strip()
         if int(daan1) is 1 and int(daan2) is 1:
                print '恭喜，%s 被录用了，工资10000'%name
                D=Diaosi(self.Name,self.Age,'x',self.Shenfen)
                D.gongzuo(name,'Python 工程师')
                D.gongzi(name,'100000')
                D.gushipangbai4(name)
         else:
                print '很遗憾，您未通过面试。。。'
                D.gongzuo(name,'网管')
                D.gongzi(name,'1000')

def gamerun():
    while True:
        os.system('clear')
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
                D.gushipangbai1(name,gfname)
                choose1=raw_input("%s,现在有一份网吧当网管的工作想做吗?输入'y'表示同意，其他表示不同意: "%name).strip()
                if choose1 is 'y':
                    L=Laoban('Old boy','35','网吧老板')
                    L.gongsiming('etiantian 网吧')
                    L.print_info()   ##打印网吧老板信息
                    L.mianshi1(name)  ##进行网吧面试
                    D.gushipangbai2(name,gfname) ##旁白
                    G=Gafushuai('王思聪','30','None','富二代')
                    G.print_info()   ##打印高富帅信息
                    choose2=raw_input('到此结束感情?接受现实请选择1,否则请选择2:').strip()
                    if int(choose2) is 1:
                        print '游戏到此结束，屌丝最终败给了现实'
                    else:
                        D.study(gfname)  #奋力学习，后面参数是想引用姓名
                        L2=Laoban('李彦宏','35','百度老板')
                        L2.gongsiming('百度')
                        L2.print_info() ##打印第二家公司老板信息
                        L2.mianshi2(name)##第二家公司面试
                        D.gushipangbai3(name,gfname)
                        choose3=raw_input('同意在一起请输入1,不同意请输入2:').strip()
                        if int(choose3) is 1:
                            print '有情人终成眷属,游戏结束。。'
                        else:
                            print '%s 选择了离开,只留%s 在雨中嚎啕大哭。。。 '%(name,gfname)
                else:
                   print '什么，这都不想干，那你只能做你的屌丝了。。。'
              else:
                  print '对不起，该角色暂未开放。。。。程序员正在苦逼的开发当中。。'
if __name__ == '__main__':
    gamerun()
