import os,sys

msg = """
\033[42;1mWelcome using old boy's auditing system!\033[0m
"""
print msg

host_dic = {
	'zhangke': '10.0.0.137',
	'xiaoqing': '10.0.0.135',
	'hanxin' : '192.168.1.107'
}

while True:
	for hostname, ip in host_dic.items():
		print hostname,ip
	try:
		host = raw_input('Please choose one server to login:').strip()
		if host == 'quit':
			print "Goodbye!"
			break
	except KeyboardInterrupt:continue
	except EOFError:continue
	if len(host) ==0:continue
	if not host_dic.has_key(host) : 
		print 'No host matched, try again.'
		continue
	print '\033[32;1mGoing to connect \033[0m', host_dic[host]
	os.system("python demo.py %s %s %s %s" % (host_dic[host][1],host_dic[host][2],host_dic[host][3],host_dic[host][4]))



