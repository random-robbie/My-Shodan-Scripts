#!/usr/bin/env python3
#
# jupyter.py
# Search SHODAN for Jupyter Notebook servers with unauthenticated API access.
# An open Jupyter API allows anonymous users to start kernels and execute
# arbitrary code on the server.
#
# Author: random_robbie

import os
import shodan
import requests
import sys

# Configuration
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import get_api_key, open_output

API_KEY = get_api_key()
SEARCH_FOR = 'product:"Jupyter Notebook"'
VERIFY_PATH = "/api/kernels"
CFG_DIR = "cfg"
session = requests.Session()


def grab_kernels(ip, port):
    """Check whether the Jupyter API answers without authentication."""
    print("[*] Testing: " + ip + " on Port: " + port + "[*]\n")
    try:
        url = "http://" + ip + ":" + port + VERIFY_PATH
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
            "Connection": "close",
            "Accept": "application/json",
        }
        response = session.get(url, headers=headers, timeout=15, verify=False)
        if response.status_code == 200 and response.text.strip().startswith("["):
            os.makedirs(CFG_DIR, exist_ok=True)
            with open(os.path.join(CFG_DIR, ip + "-jupyter-kernels.json"), "a") as fh:
                fh.write(response.text + "\n")
            print("[*] Open Jupyter kernel API Whooops.. [*]\n")
        else:
            print("[*] Jupyter requires authentication. [*]\n")
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
        grab_kernels(ip, port)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
