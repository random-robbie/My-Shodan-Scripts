#!/usr/bin/env python
#
# assets.py
# Search SHODAN for assets of a specific comapany
#
# Author: random_robbie

import shodan
import sys
import re
import socket;
from time import sleep


# Configuration
API_KEY = "YOURAPIKEY"
SEARCH_FOR = 'SSL:"COMPANY NAME FROM SSL CERT" -"AkamaiGHost" -"GHost"'




def test_host (IP,PORT):
	print ("[*] Testing: "+IP+" on Port: "+PORT+"[*]\n")
	try:
		host = IP
		port = int(PORT)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		result = sock.connect_ex((host,port))
		if result == 0:
			text_file = open("assets.txt", "a")
			text_file.write(""+IP+":"+PORT+"\n")
			text_file.close()
			print ("[*] OOOOH we have a live host [*]\n")
		else:
			print "Port is not open"

			
	except KeyboardInterrupt:
		print ("Ctrl-c pressed ...")
		sys.exit(1)
			
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
				test_host (IP,PORT)
except KeyboardInterrupt:
		print ("Ctrl-c pressed ...")
		sys.exit(1)
				
except Exception as e:
		print('Error: %s' % e)
		sys.exit(1)
