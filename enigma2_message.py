#!/usr/bin/env python
#
# enigma2_message.py
# Send a Message to an Engima2 Box
#
# Author: random_robbie


import json
import requests
import sys
import argparse


def send_message (IP,PORT,MESSAGE,ETYPE,TIMEOUT):
	
	
	if PORT == "443":
		url = "https://"+IP+":"+PORT+"/api/message"
	if PORT == "8443":
		url = "https://"+IP+":"+PORT+"/api/message"
	else:
		url = "http://"+IP+":"+PORT+"/api/message"
	try:
		session = requests.Session()
		paramsGet = {"text":""+MESSAGE+"","type":""+ETYPE+"","timeout":""+TIMEOUT+"","_":""}
		headers = {"Accept":"application/json, text/javascript, */*; q=0.01","X-Requested-With":"XMLHttpRequest","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0","Referer":"http://31.52.85.81/","Connection":"close","Accept-Language":"en-US,en;q=0.5"}
		response = session.get(url, params=paramsGet, headers=headers,timeout=15, verify=False)
		if 'Message sent successfully' in response.text:
			print ("[*] Message Sent... [*]")
		else:
			print (response.text)
		
	except requests.exceptions.Timeout:
		print ("[*] "+IP+" Timeout unable to connect [*]")
	except Exception as e:
		print('Error: %s' % e)
		
parser = argparse.ArgumentParser(description='Enter Your Message Details')
parser.add_argument('-H', '--host', default='empty', dest='host', help='IP Address Of the Box')                     
parser.add_argument('-P', '--port', default='80', dest='port', help='Port the Engima2 box is on. Default port 80')
parser.add_argument('-T', '--timeout', default='30', dest='timeout', help='How long the message lasts on sreen in seconds.') 
parser.add_argument('-M', '--message', default='Hello World...', dest='message', help='message to display on system') 
parser.add_argument('-E', '--errortype', default='1', dest='etype', help='1 = Info, 2 = warning 3 = error 0 = Yes/No') 
results = parser.parse_args()

IP = results.host
PORT = results.port
MESSAGE = results.message
ETYPE = results.etype
TIMEOUT = results.timeout

if results.host == "empty":
	print ("[*] Please Supply an IP address using -H")
	exit()
else:
	print ("[*] Sending "+MESSAGE+" to "+IP+" on port "+PORT+" for "+TIMEOUT+" seconds [*] ")

send_message (IP,PORT,MESSAGE,ETYPE,TIMEOUT)




