#!/usr/bin/env python3
#
# portainer.py
# Search SHODAN for Portainer management panels reachable on the public
# internet. Portainer controls Docker/Kubernetes environments — an exposed
# panel is one credential guess away from full infrastructure takeover.
#
# Author: random_robbie

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import get_api_key, open_output

import shodan
import requests

# Configuration
SEARCH_FOR = 'http.title:"Portainer"'
STATUS_PATH = "/api/status"
CFG_DIR = "cfg"
session = requests.Session()


def check_status(ip, port):
    """Log publicly reachable Portainer instances and their version."""
    print("[*] Testing: " + ip + " on Port: " + port + "[*]\n")
    try:
        url = "http://" + ip + ":" + port + STATUS_PATH
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
            "Connection": "close",
            "Accept": "application/json",
        }
        response = session.get(url, headers=headers, timeout=15, verify=False)
        if response.status_code == 200 and "Version" in response.text:
            with open_output(os.path.join(CFG_DIR, ip + "-portainer.json"), "a") as fh:
                fh.write(response.text + "\n")
            print("[*] Public Portainer management panel Whooops.. [*]\n")
        else:
            print("[*] Portainer not reachable without authentication. [*]\n")
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        print(e)
        print("[*] Nothing Found on IP:" + ip + " [*]\n")


def main():
    api = shodan.Shodan(get_api_key())
    result = api.search(SEARCH_FOR)
    for service in result["matches"]:
        check_status(service["ip_str"], str(service["port"]))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
