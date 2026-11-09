#!/usr/bin/env python3
#
# rabbitmq.py
# Search SHODAN for RabbitMQ management interfaces with the default guest
# account still enabled. guest:guest on the management API gives full access
# to queues, messages and users.
#
# Author: random_robbie

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import get_api_key, open_output

import shodan
import requests

# Configuration
SEARCH_FOR = 'product:"RabbitMQ" port:"15672"'
OVERVIEW_PATH = "/api/overview"
CFG_DIR = "cfg"
session = requests.Session()


def check_default_creds(ip, port):
    """Try the default guest:guest account against the management API."""
    print("[*] Testing: " + ip + " on Port: " + port + "[*]\n")
    try:
        url = "http://" + ip + ":" + port + OVERVIEW_PATH
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
            "Connection": "close",
            "Accept": "application/json",
        }
        response = session.get(url, headers=headers, timeout=15, verify=False, auth=("guest", "guest"))
        if response.status_code == 200 and "rabbitmq_version" in response.text:
            with open_output(os.path.join(CFG_DIR, ip + "-rabbitmq.json"), "a") as fh:
                fh.write(response.text + "\n")
            print("[*] RabbitMQ default credentials Whooops.. [*]\n")
        else:
            print("[*] RabbitMQ default credentials rejected. [*]\n")
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        print(e)
        print("[*] Nothing Found on IP:" + ip + " [*]\n")


def main():
    api = shodan.Shodan(get_api_key())
    result = api.search(SEARCH_FOR)
    for service in result["matches"]:
        check_default_creds(service["ip_str"], str(service["port"]))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
