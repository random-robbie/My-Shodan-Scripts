#!/usr/bin/env python
#
# engima2_watch.py
# Search SHODAN for Engima 2 box's that are watching a channel.
#
# Author: random_robbie

import shodan
import sys
import subprocess
import shlex
import json
import requests


# Configuration
API_KEY = "YOURSHODANAPIKEY"
SEARCH_FOR = "title:'Open Webif'"
CHANNEL_NAME = "LFCTV"
CHANNEL_ID = "1:0:1:F06:7D7:2:11A0000:0:0:0:"

session = requests.Session()

def test_stream (IP,CHANNEL_NAME,CHANNEL_ID):
	stream = "http://"+IP+":8001/"+CHANNEL_ID+""
	print ("[*] Testing stream: "+IP+" for "+CHANNEL_NAME+"  [*]")
	cmd = "ffprobe -v quiet -print_format json -show_streams"
	args = shlex.split(cmd)
	args.append(stream)
    # run the ffprobe process, decode stdout into utf-8 & convert to JSON
	try:
		ffprobeOutput = subprocess.check_output(args,timeout=25).decode('utf-8')
		ffprobeOutput = json.loads(ffprobeOutput)
		# for example, find height and width
		height = ffprobeOutput['streams'][0]['height']
		width = ffprobeOutput['streams'][0]['width']
		print ("[*] Working Stream for "+CHANNEL_NAME+" on "+IP+" [*]\n")
		text_file = open(""+CHANNEL_NAME+".m3u", "a")
		text_file.write("#EXTINF:-0, "+CHANNEL_NAME+" - "+IP+"\n")
		text_file.write(""+stream+"\n")
		text_file.close()
	except subprocess.TimeoutExpired:
		print ("[*] Failed to connect to IP: "+IP+" [*]\n")
	except:
		print ("[*] Failed to connect to IP: "+IP+" [*]\n")
	



	
	
try:
        # Setup the api
		api = shodan.Shodan(API_KEY)

        # Perform the search
		result = api.search(SEARCH_FOR)

        # Loop through the matches and print each IP
		for service in result['matches']:
				IP = service['ip_str']
				test_stream (IP,CHANNEL_NAME,CHANNEL_ID)

				
except Exception as e:
		print('Error: %s' % e)
		sys.exit(1)