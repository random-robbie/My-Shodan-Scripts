#!/usr/bin/env python3
#
# kafkaui.py
# Search SHODAN for exposed Kafka UI (Provectus) instances. An open Kafka UI
# allows reading any topic — customer data, events, tokens — and often
# editing cluster configuration.
#
# Author: random_robbie

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import get_api_key, open_output

import shodan
import requests

# Configuration
SEARCH_FOR = 'http.title:"Kafka UI"'
CLUSTERS_PATH = "/api/clusters"
CFG_DIR = "cfg"
session = requests.Session()


def check_clusters(ip, port):
    """Check whether the clusters API answers without authentication."""
    print("[*] Testing: " + ip + " on Port: " + port + "[*]\n")
    try:
        url = "http://" + ip + ":" + port + CLUSTERS_PATH
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
            "Connection": "close",
            "Accept": "application/json",
        }
        response = session.get(url, headers=headers, timeout=15, verify=False)
        if response.status_code == 200 and "[" in response.text:
            with open_output(os.path.join(CFG_DIR, ip + "-kafkaui.json"), "a") as fh:
                fh.write(response.text + "\n")
            print("[*] Open Kafka UI Whooops.. [*]\n")
        else:
            print("[*] Kafka UI requires authentication or is not live. [*]\n")
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        print(e)
        print("[*] Nothing Found on IP:" + ip + " [*]\n")


def main():
    api = shodan.Shodan(get_api_key())
    result = api.search(SEARCH_FOR)
    for service in result["matches"]:
        check_clusters(service["ip_str"], str(service["port"]))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
