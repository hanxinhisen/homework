#!/usr/bin/env python
#coding:utf-8
import os,sys,time

try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False


def interactive_shell(chan,audit_loginuser,hostname):
    print """\033[;34m------ Welcome %s Login %s ------\033[0m""" % (audit_loginuser,hostname)
    if has_termios:
        posix_shell(chan,audit_loginuser,hostname)
    else:
        pass


def posix_shell(chan,audit_loginuser,hostname):
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
        if os.path.exists('/tmp/audit/logs'):
            pass
        else:
            os.makedirs('/tmp/audit/logs')
        f = open('/tmp/audit/logs/audit_%s_%s.log' % (day_time,audit_loginuser),'a')
        while True:
            date =time.strftime('%Y_%m_%d %H:%M:%S')
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = chan.recv(1024)
                    if len(x) == 0:
                        print '\r\n退出登陆\r\n',
                        break
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except Exception:
                    pass

            if sys.stdin in r:
                x = sys.stdin.read(1)
                if len(x) == 0:
                    break
                record.append(x)
                chan.send(x)

            if x == '\r':
                cmd = ''.join(record).split('\r')[-2]
                #log = "%s\t%s\t%s *** %s\n" % (hostname,date,django_loginuser,cmd)
                log = "%s | %s | %s | %s\n" % (hostname,date,audit_loginuser,cmd)
                f.write(log)
                #f.write("%s\n" % str(cmd))
                f.flush()
        f.close()

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

    
# thanks to Mike Looijmans for this code