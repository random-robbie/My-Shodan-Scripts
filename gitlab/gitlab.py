#!/usr/bin/env python3
#
# gitlab.py
# Search SHODAN for GitLab instances exposing their version API without
# authentication. An unauthenticated /api/v4/version also usually means
# unauthenticated user enumeration via /api/v4/users.
#
# Author: random_robbie

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import get_api_key, open_output

import shodan
import requests

# Configuration
SEARCH_FOR = 'http.title:"GitLab"'
VERSION_PATH = "/api/v4/version"
CFG_DIR = "cfg"
session = requests.Session()


def check_version_api(ip, port):
    """Check whether the GitLab version API answers without a token."""
    print("[*] Testing: " + ip + " on Port: " + port + "[*]\n")
    try:
        url = "http://" + ip + ":" + port + VERSION_PATH
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
            "Connection": "close",
            "Accept": "application/json",
        }
        response = session.get(url, headers=headers, timeout=15, verify=False)
        if response.status_code == 200 and "version" in response.text:
            with open_output(os.path.join(CFG_DIR, ip + "-gitlab.json"), "a") as fh:
                fh.write(response.text + "\n")
            print("[*] GitLab version API exposed Whooops.. [*]\n")
        else:
            print("[*] GitLab version API requires authentication. [*]\n")
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        print(e)
        print("[*] Nothing Found on IP:" + ip + " [*]\n")


def main():
    api = shodan.Shodan(get_api_key())
    result = api.search(SEARCH_FOR)
    for service in result["matches"]:
        check_version_api(service["ip_str"], str(service["port"]))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
