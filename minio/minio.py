#!/usr/bin/env python3
#
# minio.py
# Search SHODAN for exposed MinIO object storage servers and check whether
# the health endpoints answer publicly. Open MinIO deployments often leak
# bucket listings and anonymous read/write policies.
#
# Author: random_robbie

import os
import shodan
import requests
import sys

# Configuration
API_KEY = "YOUR API KEY"
SEARCH_FOR = 'product:"MinIO"'
HEALTH_PATH = "/minio/health/live"
CFG_DIR = "cfg"
session = requests.Session()


def check_health(ip, port):
    """Check whether the MinIO health endpoint answers without authentication."""
    print("[*] Testing: " + ip + " on Port: " + port + "[*]\n")
    try:
        url = "http://" + ip + ":" + port + HEALTH_PATH
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
            "Connection": "close",
        }
        response = session.get(url, headers=headers, timeout=15, verify=False)
        if response.status_code == 200:
            # Anonymous listing attempt via the S3 API
            list_url = "http://" + ip + ":" + port + "/"
            listing = session.get(list_url, headers=headers, timeout=15, verify=False)
            os.makedirs(CFG_DIR, exist_ok=True)
            with open(os.path.join(CFG_DIR, ip + "-minio.txt"), "a") as fh:
                fh.write("health: %s\nlisting (%s):\n%s\n---\n" % (
                    response.status_code, listing.status_code, listing.text[:5000]))
            print("[*] Live MinIO health endpoint Whooops.. [*]\n")
        else:
            print("[*] MinIO health endpoint not public. [*]\n")
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
        check_health(ip, port)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
