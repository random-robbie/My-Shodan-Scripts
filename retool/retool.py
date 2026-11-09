#!/usr/bin/env python3
#
# retool.py
# Search SHODAN for self-hosted Retool instances. Retool apps are wired
# directly into internal databases and APIs — an exposed instance puts every
# connected data source one click away.
#
# Author: random_robbie

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import get_api_key, open_output

import shodan
import requests

# Configuration
SEARCH_FOR = 'http.html:"Retool"'
SESSION_PATH = "/api/checkSession"
CFG_DIR = "cfg"
session = requests.Session()


def check_session(ip, port):
    """Check whether the Retool instance answers its session API publicly."""
    print("[*] Testing: " + ip + " on Port: " + port + "[*]\n")
    try:
        url = "http://" + ip + ":" + port + SESSION_PATH
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
            "Connection": "close",
            "Accept": "application/json",
        }
        response = session.get(url, headers=headers, timeout=15, verify=False)
        if response.status_code == 200:
            with open_output(os.path.join(CFG_DIR, ip + "-retool.json"), "a") as fh:
                fh.write(response.text + "\n")
            print("[*] Public Retool instance Whooops.. [*]\n")
        else:
            print("[*] Retool not reachable. [*]\n")
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        print(e)
        print("[*] Nothing Found on IP:" + ip + " [*]\n")


def main():
    api = shodan.Shodan(get_api_key())
    result = api.search(SEARCH_FOR)
    for service in result["matches"]:
        check_session(service["ip_str"], str(service["port"]))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
