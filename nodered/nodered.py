#!/usr/bin/env python3
#
# nodered.py
# Search SHODAN for Node-RED editors exposed without authentication.
# Node-RED without adminAuth serves the full editor to anyone, and injecting
# an exec node gives arbitrary command execution on the host.
#
# Author: random_robbie

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import get_api_key, open_output

import shodan
import requests

# Configuration
SEARCH_FOR = 'http.title:"Node-RED"'
MARKER = "node-red"
CFG_DIR = "cfg"
session = requests.Session()


def check_editor(ip, port):
    """An open Node-RED serves the editor directly; secured ones redirect to /auth/login."""
    print("[*] Testing: " + ip + " on Port: " + port + "[*]\n")
    try:
        url = "http://" + ip + ":" + port + "/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
            "Connection": "close",
        }
        response = session.get(url, headers=headers, timeout=15, verify=False, allow_redirects=False)
        if response.status_code == 200 and MARKER in response.text.lower():
            with open_output(os.path.join(CFG_DIR, ip + "-nodered.html"), "a") as fh:
                fh.write(response.text[:5000] + "\n---\n")
            print("[*] Open Node-RED editor Whooops.. [*]\n")
        else:
            print("[*] Node-RED requires authentication or is not live. [*]\n")
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        print(e)
        print("[*] Nothing Found on IP:" + ip + " [*]\n")


def main():
    api = shodan.Shodan(get_api_key())
    result = api.search(SEARCH_FOR)
    for service in result["matches"]:
        check_editor(service["ip_str"], str(service["port"]))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
