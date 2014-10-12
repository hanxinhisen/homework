#!/usr/bin/env python
#coding:utf-8
import socket
import os,sys,datetime,time
#import tri_config

# windows does not have termios...
try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False


def interactive_shell(chan,django_loginuser,hostname):
    print """\033[;34m------ Welcome %s Login %s ------\033[0m""" % (django_loginuser,hostname)
    if has_termios:
        posix_shell(chan,django_loginuser,hostname)
    else:
        windows_shell(chan)


def posix_shell(chan,django_loginuser,hostname):
    import select
    
    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)

        record = []
	record_dic = {}

        ''' record operation log '''
        day_time = time.strftime('%Y_%m_%d')
        #triaquae_path = os.path.abspath('.')
        #triaquae_path = '/usr/local/src/triWeb_frontend'
        #triaquae_path = tri_config.Working_dir
        if os.path.exists('/tmp/audit/logs'): #判断用户目录是否存在
            pass
        else:
            os.makedirs('/tmp/audit/logs')
        f = open('/tmp/audit/logs/audit_%s_%s.log' % (day_time,django_loginuser),'a')
        while True:
	    date =time.strftime('%Y_%m_%d %H:%M:%S')
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = chan.recv(1024)
                    if len(x) == 0:
                        print '\r\n*** EOF\r\n',
                        break
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
                #print x,'-------recv\n'

                #f.write("%s"%x)
                #f.flush()
            if sys.stdin in r:
                x = sys.stdin.read(1)
                if len(x) == 0:
                    break
                record.append(x)
                chan.send(x)

            if x == '\r':
                cmd = ''.join(record).split('\r')[-2]
                #log = "%s\t%s\t%s *** %s\n" % (hostname,date,django_loginuser,cmd)
                log = "%s | %s | %s | %s\n" % (hostname,date,django_loginuser,cmd)
                f.write(log)
                #f.write("%s\n" % str(cmd))
                f.flush()
        f.close()

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

    
# thanks to Mike Looijmans for this code
def windows_shell(chan):
    import threading

    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")
        
    def writeall(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(data)
            sys.stdout.flush()
        
    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()
        
    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass
