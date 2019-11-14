#!/usr/bin/env python
#
# docker.py
# Search SHODAN for docker API's exposed
#
# Author: random_robbie

import shodan
import sys
import re
import requests
from time import sleep

# Configuration
API_KEY = "YOUR API KEY"
SEARCH_FOR = 'port:2375 product:"Docker"'
FILE = "/v1.24/containers/json"
session = requests.Session()

def filter_result(str):
	return str.strip()

def grab_file (IP,PORT,FILE):
	print ("[*] Testing: "+IP+" on Port: "+PORT+"[*]\n")
	try:
		URL = "http://"+IP+":"+PORT+""+FILE+""
		headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1"}
		response = session.get(URL, headers=headers, timeout=15, verify=False)
		result = response.text
		if "Image"in  result:
			if any(re.findall(r'minergate|xmr-stak-cpu|xmrdemo|140.82.21.105|144.202.25.142|xmrigCC|proton', result, re.IGNORECASE)):
				text_file = open("./cfg-hijacked/"+IP+"-hijacked.cfg", "a")
				text_file.write(""+result+"\n")
				text_file.close()
				print ("[*] DOH! this docker server has been hijacked for XMR or DDOS. [*]\n")
			else:
				text_file = open("./cfg/"+IP+"-containers.cfg", "a")
				text_file.write(""+result+"\n")
				text_file.close()
				print ("[*] Live Docker API Whooops.. [*]\n")
	except KeyboardInterrupt:
		sys.exit("Ctrl-c pressed ...")			
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
				grab_file (IP,PORT,FILE)
except KeyboardInterrupt:
		sys.exit("Ctrl-c pressed ...")				
except Exception as e:
		sys.exit('Error: %s' % e)
