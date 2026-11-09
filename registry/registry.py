#!/usr/bin/env python3
#
# registry.py
# Search SHODAN for exposed Docker Registry v2 servers and pull the image
# catalog. Open registries leak private container images and often the
# environment variables baked into them (secrets, keys, passwords).
#
# Author: random_robbie

import os
import shodan
import requests
import sys

# Configuration
API_KEY = "YOUR API KEY"
SEARCH_FOR = 'port:5000 "Docker-Distribution-API-Version"'
CATALOG_PATH = "/v2/_catalog"
CFG_DIR = "cfg"
session = requests.Session()


def grab_catalog(ip, port):
    """Check whether the registry catalog answers without authentication."""
    print("[*] Testing: " + ip + " on Port: " + port + "[*]\n")
    try:
        url = "http://" + ip + ":" + port + CATALOG_PATH
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
            "Connection": "close",
            "Accept": "application/json",
        }
        response = session.get(url, headers=headers, timeout=15, verify=False)
        if response.status_code == 200 and "repositories" in response.text:
            os.makedirs(CFG_DIR, exist_ok=True)
            with open(os.path.join(CFG_DIR, ip + "-registry.json"), "a") as fh:
                fh.write(response.text + "\n")
            print("[*] Open Docker Registry Whooops.. [*]\n")
        else:
            print("[*] Registry requires authentication or is not live. [*]\n")
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        print(e)
        print("[*] Nothing Found on IP:" + ip + " [*]\n")


def main():
    api = shodan.Shodan(API_KEY)
    result = api.search(SEARCH_FOR)
    for service in result["matches"]:
        ip = service["ip_str"]
        port = str(service["port"])
        grab_catalog(ip, port)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
