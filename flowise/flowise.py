#!/usr/bin/env python3
#
# flowise.py
# Search SHODAN for exposed Flowise and Langflow instances. These visual
# LLM workflow builders execute arbitrary code via their flow nodes when
# left unauthenticated — effectively remote code execution.
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
TARGETS = [
    # (shodan query, verify path, marker in response, label)
    ('port:3000 http.html:"Flowise"', "/api/v1/prediction", "Flowise", "flowise"),
    ('port:7860 http.title:"Langflow"', "/api/v1/health", "langflow", "langflow"),
]
CFG_DIR = "cfg"
session = requests.Session()


def check_target(ip, port, path, marker, label):
    """Check whether the Flowise/Langflow API answers without authentication."""
    print("[*] Testing: " + ip + " on Port: " + port + " (" + label + ")[*]\n")
    try:
        url = "http://" + ip + ":" + port + path
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
            "Connection": "close",
            "Accept": "application/json",
        }
        response = session.get(url, headers=headers, timeout=15, verify=False)
        if response.status_code == 200 and marker.lower() in response.text.lower():
            os.makedirs(CFG_DIR, exist_ok=True)
            with open(os.path.join(CFG_DIR, ip + "-" + label + ".json"), "a") as fh:
                fh.write(response.text + "\n")
            print("[*] Open " + label + " instance Whooops.. [*]\n")
        else:
            print("[*] " + label + " requires authentication or is not live. [*]\n")
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        print(e)
        print("[*] Nothing Found on IP:" + ip + " [*]\n")


def main():
    api = shodan.Shodan(API_KEY)
    for query, path, marker, label in TARGETS:
        result = api.search(query)
        for service in result["matches"]:
            ip = service["ip_str"]
            port = str(service["port"])
            check_target(ip, port, path, marker, label)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
