#!/usr/bin/env python
#-*- coding:UTF8 -*-
import time,sys
class People : #定义一个父类People
    def __init__(self,name,sex,lover):
        self.name = name
        self.sex = sex
        self.lover = lover
class Poor_guy(People):#子类---穷屌丝
    def __init__(self,name,sex,lover,salary,job):
        People.__init__(self,name,sex,lover)
        self.salary =salary
        self.job = job
    def love(self):#恋爱初期
        print "Start the countdown 3 seconds game ....."
        time.sleep(3) #停顿3s钟继续输入
        print "\n   John and Liz 是高中同学时的恋人,开始很甜蜜..."
        time.sleep(1.5)
        print "Liz考上了北京城市学院，Jhon没有,为了跟女朋友在一起，"
        time.sleep(1.5)
        print "他来到了北京打工（一家网吧当网管）,挣钱为Liz交学费,"
        time.sleep(1.5)
        print "后来LIZ毕业后工作了。。。遇到了公司的高富帅peter"
        time.sleep(1.5)
        print "One day ... Liz 约 John 吃饭………"
        time.sleep(2)
        print "\nLiz :John 你工资太少了，我想要的你给不了，我们分手吧。\n"
        time.sleep(1.5)
        separate = raw_input("Are you willing to break up:")
        if separate == 'y':
            print "\nJohn :嗯。。。。。。。。。。。祝你幸福。。。。。。。。\n"
            Figure_1 = Poor_guy("Jhon","male","None",1000,"Network management ")
            time.sleep(2)
            print "当前的人物角色为："
            print "Name:%s" % Figure_1.name
            print "Sex:%s"  % Figure_1.sex
            print "Lover:%s" % Figure_1.lover
            print "Salary:%s" % Figure_1.salary
            print "Job:%s" %Figure_1.job
            print "\n"
        else:
            sys.exit("她已经喜欢 高富帅了，放弃吧...Game Over...")

        time.sleep(2)
        print '=' * 13 + "屌丝开始奋斗" + '=' * 13 #字符可乘，等于：'============='
    def study(self):#学习
       print "\n_____2014年北京程序员工资排行榜_____"
       stu ={"python":10000,"java":9000,"C":9000,"ASP.net":8000}
       for i,v in stu.items():
           print "语言：%s,平均工资:%s"%(i,stu[i])
           pass
       print "___________________________________"
       time.sleep(1.5)
       print "\n看过排行榜后，John决定去老男孩 学习Python...\n"
       time.sleep(3)
       stupy = raw_input("Would you like to go to the old boy learning python:")
       if stupy == "y":
            time.sleep(1)
            print "\n努力学习中……请等待……"
            time.sleep(10)
            print "\nJhon 经过十五周的Python课程后，终于学有所成\n"
            time.sleep(1)
            print "成功毕业！"
            Figure_1 = Poor_guy("Jhon","male","None",0,"Student ")
            time.sleep(2)
            print "\n当前的人物角色为："
            print "Name:%s" % Figure_1.name
            print "Sex:%s"  % Figure_1.sex
            print "Lover:%s" % Figure_1.lover
            print "Salary:%s" % Figure_1.salary
            print "Job:%s" %Figure_1.job
            print "\n"
       else:
           sys.exit("放弃奋斗，游戏结束！！！")
    def Interview(self):#面试
        print '=' * 13 + "屌丝开始面试" + '=' * 13 #字符可乘，等于：'============='
        time.sleep(1.5)
        interview = raw_input("\nPlease enter the answer to the questions  map(lambda x:x**2,[i for i in range(3)]):")
        if interview == '[0,1,4]':
            print "\n恭喜你通过面试，工资：10000 ，职位：python研发工程师"
            Figure_1 = Poor_guy("Jhon","male","None",10000,"Python engineer")
            time.sleep(2)
            print "\n当前的人物角色为："
            print "Name:%s" % Figure_1.name
            print "Sex:%s"  % Figure_1.sex
            print "Lover:%s" % Figure_1.lover
            print "Salary:%s" % Figure_1.salary
            print "Job:%s" %Figure_1.job
            print "\n"
        else:
            sys.exit("没打好基础，找不到工作...游戏结束!!!")
    def change_lift(self):#当上IT总监
        time.sleep(2)
        print '=' * 13 + "屌丝变为IT总监" + '=' * 13 #字符可乘，等于：'============='
        time.sleep(1)
        print "\n…………经过若干年的奋斗，Jhon 成功当上IT总监."
        time.sleep(1)
        print "在北京三环买了属于自己的房子，以及Minicooper."
        time.sleep(1)
        Figure_1 = Poor_guy("Jhon","male","None",10000,"IT director")
        time.sleep(2)
        print "\n当前的人物角色为："
        print "Name:%s" % Figure_1.name
        print "Sex:%s"  % Figure_1.sex
        print "Lover:%s" % Figure_1.lover
        print "Salary:%s" % Figure_1.salary
        print "Job:%s" %Figure_1.job
        print "\n"
        time.sleep(2)
        print '=' * 13 + "Liz重遇Jhon" + '=' * 13 #字符可乘，等于：'============='
    def mett(self):#再次相遇Liz
        print "...One day,Jhon 在马路旁边遇到了Liz孤身一人，看到眼前Jhon后"
        time.sleep(2)
        print "\nLiz :亲爱的John，Peter和我分手了，我们像以前一样好吗？\n"
        time.sleep(2.5)
        sys.exit("Jhon :看着眼前的 Liz 说了两个字：呵呵, 然后没有然后了。The end...")
class Beatuy(People):#子类---美女
    def __init__(self,name,sex,lover,beatuy):
        People.__init__(self,name,sex,lover)
        self.beatuy = beatuy
    def loves(self):#恋爱初期
        print "Start the countdown 3 seconds game ....."
        time.sleep(3) #停顿3s钟继续输入
        print "\n   John and Liz 是高中同学时的恋人,开始很甜蜜..."
        time.sleep(1.5)
        print "Liz考上了北京城市学院，Jhon没有,为了跟女朋友在一起，"
        time.sleep(1.5)
        print "他来到了北京打工（一家网吧当网管）,挣钱为Liz交学费,"
        time.sleep(1.5)
        print "后来LIZ毕业后工作了。。。遇到了公司的高富帅peter"
        time.sleep(1.5)
        print "One day ... Peter 约 Liz 吃饭………"
        time.sleep(2)
        print "\nPeter:Liz  我喜欢上你了，我们在一起好吗？\n"
        time.sleep(1.5)
        separate = raw_input("Are you willing to and I together:")
        if separate == 'y':
            print "\nLiz :嗯。。。。。。。。。。。YES I DO。。。。。。。。\n"
            Figure_2 = Beatuy("Liz","female","Peter","beautiful")
            time.sleep(2)
            print "当前的人物角色为："
            print "Name:%s" % Figure_2.name
            print "Sex:%s"  % Figure_2.sex
            print "Lover:%s" % Figure_2.lover
            print "Beatuy:%s" % Figure_2.beatuy
            print "\n"
        else:
            sys.exit("只有Peter可以给你想要的生活，不选他只能结束游戏...")
        time.sleep(2)
        print '=' * 13 + "Liz被无情抛弃" + '=' * 13 #字符可乘，等于：'============='
    def abandon(self):#被抛弃
        print "\n...One day Liz 知道Peter是已婚人士，便质问Peter..."
        time.sleep(1.5)
        print "\nPeter:Liz  对不起，我欺骗了你，我们分手吧\n"
        Agreed = raw_input("Do you accept? ")
        if Agreed == 'y':
            print "\nLiz :嗯。。。。。。。。。。。Say good bey。。。。。。。。\n"
            Figure_2 = Beatuy("Liz","female","None","beautiful")
            time.sleep(2)
            print "当前的人物角色为："
            print "Name:%s" % Figure_2.name
            print "Sex:%s"  % Figure_2.sex
            print "Lover:%s" % Figure_2.lover
            print "Beatuy:%s" % Figure_2.beatuy
            print "\n"
        else:
            sys.exit("你已经别无选择，游戏结束！！！")
        time.sleep(2)
        print '=' * 13 + "Liz重遇Jhon" + '=' * 13 #字符可乘，等于：'============='
    def Reunited(self):#重遇Jhon
        time.sleep(2)
        print "...One day,Liz 在马路旁边遇到了风光的Jhon，看到眼前Jhon后"
        time.sleep(2)
        print "\nLiz :亲爱的John，Peter和我分手了，我们像以前一样好吗？\n"
        time.sleep(2.5)
        sys.exit("Jhon :看着眼前的 Liz 说了两个字：呵呵, 然后没有然后了。The end...")
class  Handsome(People):#子类---高富帅
    def __init__(self,name,sex,lover,salary,job):
        People.__init__(self,name,sex,lover)
        self.salary =salary
        self.job = job
        pass
    def loving(self):#恋爱初期
        print "Start the countdown 3 seconds game ....."
        time.sleep(3) #停顿3s钟继续输入
        print "\n   Peter是某公司CEO,某日在公司遇到美女Liz..."
        time.sleep(1.5)
        print "对Liz 一见钟情，知道Liz有个当网管的男朋友Jhon,"
        time.sleep(1.5)
        print "然后对Liz开始了追求,One day ... Peter 约 Liz 吃饭………"
        time.sleep(2)
        print "\nPeter:Liz 我喜欢上你了，我们在一起好吗？\n"
        time.sleep(1.5)
        print "Liz :嗯。。。。。YES I DO。。。。\n"
        time.sleep(2)
        Figure_3 = Handsome("Peter","male","Liz&home",10000000,"CEO")
        print "当前的人物角色为："
        print "Name:%s" % Figure_3.name
        print "Sex:%s"  % Figure_3.sex
        print "Lover:%s" % Figure_3.lover
        print "Salary:%s" % Figure_3.salary
        print "Job:%s" %Figure_3.job
        time.sleep(2)
        print '=' * 13 + "Liz被无情抛弃" + '=' * 13 #字符可乘，等于：'============='
    def change_heart(self):#分手
        time.sleep(1.5)
        print "\n在一起甜蜜的三个月，Liz突然问Peter一个问题 :"
        time.sleep(1.5)
        print "Peter,你愿意和我结婚吗？我想和你一辈子在一起..."
        separate = raw_input("Would you like to marry me :")
        if separate == 'y':
            print "Peter :嗯。我愿意。但是我已经结婚了。对不起，我欺骗了你，我们分手吧\n"
            time.sleep(2)
            Figure_3 = Handsome("Peter","male","home",10000000,"CEO")
            print "当前的人物角色为："
            print "Name:%s" % Figure_3.name
            print "Sex:%s"  % Figure_3.sex
            print "Lover:%s" % Figure_3.lover
            print "Salary:%s" % Figure_3.salary
            print "Job:%s" %Figure_3.job
            time.sleep(1.5)
            sys.exit("Liz:嗯。。。。。。。。。。。Say good bey。。。。。。。。")
        else:
            Figure_3 = Handsome("Peter","male","home",10000000,"CEO")
            print "当前的人物角色为："
            print "Name:%s" % Figure_3.name
            print "Sex:%s"  % Figure_3.sex
            print "Lover:%s" % Figure_3.lover
            print "Salary:%s" % Figure_3.salary
            print "Job:%s" %Figure_3.job
            time.sleep(1.5)
            sys.exit("Peter不同意结婚继续在一起没有意义，只能结束游戏...")
        pass
def test():
     while True:
         print '''
            1.John is a poor guy
            2.Liz is a pretty girl
            3.Peter is a Grosvenor LTD handsome
              '''
         check = raw_input("Please select a game character object:").strip()
         if len(check) == 0:
             print "Can't input is empty Please choose again ..."
             continue
         elif int(check)!= 1 and int(check)!= 2 and int(check)!= 3:
             print "Input option does not exist, please enter again ..."
             continue
         else:
             if int(check) == 1:
                 print "当前的人物角色："
                 Figure_1 = Poor_guy("Jhon","male","Liz",1000,"Network management ")
                 print "Name:%s" % Figure_1.name
                 print "Sex:%s"  % Figure_1.sex
                 print "Lover:%s" % Figure_1.lover
                 print "Salary:%s" % Figure_1.salary
                 print "Job:%s" %Figure_1.job
                 Figure_1.love()
                 Figure_1.study()
                 Figure_1.Interview()
                 Figure_1.change_lift()
                 Figure_1.mett()
             if int(check) == 2:
                 Figure_2 = Beatuy("Liz","female","Jhon","beautiful")
                 print "Name:%s" % Figure_2.name
                 print "Sex:%s"  % Figure_2.sex
                 print "Lover:%s" % Figure_2.lover
                 print "Beatuy:%s" % Figure_2.beatuy
                 Figure_2.loves()
                 Figure_2.abandon()
                 Figure_2.Reunited()
             if int(check) == 3:
                 Figure_3 = Handsome("Peter","male","home",10000000,"CEO")
                 print "Name:%s" % Figure_3.name
                 print "Sex:%s"  % Figure_3.sex
                 print "Lover:%s" % Figure_3.lover
                 print "Salary:%s" % Figure_3.salary
                 print "Job:%s" %Figure_3.job
                 Figure_3.loving()
                 Figure_3.change_heart()
if __name__ == '__main__':
    test()
