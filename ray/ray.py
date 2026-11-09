#!/usr/bin/env python3
#
# ray.py
# Search SHODAN for exposed Ray dashboard instances (ShadowRay, CVE-2023-48022
# and related). An open Ray dashboard allows job submission and code execution
# on the cluster.
#
# Author: random_robbie

import os
import shodan
import requests
import sys

# Configuration
API_KEY = "YOUR API KEY"
SEARCH_FOR = 'port:8265 http.title:"Ray"'
VERIFY_PATH = "/api/version"
CFG_DIR = "cfg"
session = requests.Session()


def grab_version(ip, port):
    """Check whether the Ray dashboard API answers without authentication."""
    print("[*] Testing: " + ip + " on Port: " + port + "[*]\n")
    try:
        url = "http://" + ip + ":" + port + VERIFY_PATH
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
            "Connection": "close",
            "Accept": "application/json",
        }
        response = session.get(url, headers=headers, timeout=15, verify=False)
        if response.status_code == 200 and "ray_version" in response.text:
            os.makedirs(CFG_DIR, exist_ok=True)
            with open(os.path.join(CFG_DIR, ip + "-ray.json"), "a") as fh:
                fh.write(response.text + "\n")
            print("[*] Open Ray dashboard Whooops.. [*]\n")
        else:
            print("[*] Ray dashboard requires authentication or is not live. [*]\n")
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
        grab_version(ip, port)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
