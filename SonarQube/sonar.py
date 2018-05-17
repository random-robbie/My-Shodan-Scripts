#!/usr/bin/env python
#
# sonar.py
# Search SHODAN for Sonar Qube's that are require no login.
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
API_KEY = "YOUR API KEY"
SEARCH_FOR = 'http.favicon.hash:1485257654'
FILE = "/api/components/search_projects?ps=1"
session = requests.Session()

def filter_result(str):
	str.strip() #trim
	str.lstrip() #ltrim
	str.rstrip() #rtrim
	return str

def grab_file (IP,PORT,FILE,TITLE):
	print ("[*] Testing: "+IP+" on Port: "+PORT+"[*]\n")
	try:
		if PORT == "80":
			URL = "http://"+IP+":"+PORT+""+FILE+""
		if PORT == "443":
			URL = "https://"+IP+":"+PORT+""+FILE+""
			
			
		print (URL)
		headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0"}
		response = session.get(URL, headers=headers, timeout=15, verify=False)
		if response.status_code == 200:
			if '"total":0' not in response.text:
				URLi = URL.replace("/api/components/search_projects?ps=1","")
				text_file = open("./cfg/sonar.cfg", "a")
				text_file.write(""+URLi+" - "+TITLE+"\n")
				text_file.close()
				print ("[*] Sonar ... Found - "+TITLE+" [*]\n")
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
				TITLE = service['title']
				grab_file (IP,PORT,FILE,TITLE)
except KeyboardInterrupt:
		print ("Ctrl-c pressed ...")
		sys.exit(1)
				
except Exception as e:
		print('Error: %s' % e)
		sys.exit(1)