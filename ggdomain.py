#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by zhangh
# 输入域名通过google搜集所有二级域名
# 墙内需要科学上网
# 对搜索引擎不收集的可通过爆破的方式遍历

import socket
import os
import re
import time
import sys
import shodan
import simplejson
import httplib
import urllib,urllib2

RED = '\x1b[91m'
RED1 = '\033[31m'
BLUE = '\033[94m'
GREEN = '\033[32m'
BOLD = '\033[1m'
NORMAL = '\033[0m'
ENDC = '\033[0m'

header = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'HTTPS':'1',
	'Referer':'https://www.google.com.tw/',
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'
}

def query(domain):
	rs = set()
	i = 0
	while True:
		time.sleep(1)
		start = i*10
		url = "https://www.google.com.tw/search?q=site:%s&start=%d&hl=en&filter=0" % (domain, start)
		i = i+1
		print GREEN + url
		req = urllib2.Request(url, headers=header)
		code = urllib2.urlopen(req).read()
		res = re.findall('http://([\w\d\.-]{0,256}?\.?%s).*?".onmousedown' % domain, code, re.I)		
		for name in res:
			rs.add(name)
		if code.find("Next") == -1:
			break
	return rs

def save(rs, output):
	out = open(output, 'a')
	out.write("# domain list\n")
	for line in rs:
		out.write(line + "\n")
		print BLUE + line
	out.close()

if __name__ == '__main__':
	if len(sys.argv) <> 3:
		print RED + "\n" + "!!!Parameter ERROR !!!"
		print RED1 + "EG: python " + sys.argv[0] + " domainname.com output.txt"
	else:
		domain = sys.argv[1]
		output = sys.argv[2]
		rs = query(domain)
		save(rs, output)

# infos	
print (ENDC+ "\n   http://zhanghang.org\n"
			 "   zhanghangorg#gmail.com\n")

print ENDC
