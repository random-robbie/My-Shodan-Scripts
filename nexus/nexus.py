#!/usr/bin/env python3
#
# nexus.py
# Search SHODAN for Sonatype Nexus Repository instances with anonymous
# browsing enabled (the default). /service/rest/v1/repositories lists every
# repository, and /service/rest/v1/search serves the artifacts in them —
# internal libraries, credentials baked into config files, everything.
#
# Author: random_robbie

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import get_api_key, open_output

import shodan
import requests

# Configuration
SEARCH_FOR = 'http.title:"Nexus Repository Manager"'
REPOS_PATH = "/service/rest/v1/repositories"
CFG_DIR = "cfg"
session = requests.Session()


def grab_repos(ip, port):
    """Check whether the repositories API answers without authentication."""
    print("[*] Testing: " + ip + " on Port: " + port + "[*]\n")
    try:
        url = "http://" + ip + ":" + port + REPOS_PATH
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
            "Connection": "close",
            "Accept": "application/json",
        }
        response = session.get(url, headers=headers, timeout=15, verify=False)
        if response.status_code == 200 and "[" in response.text:
            with open_output(os.path.join(CFG_DIR, ip + "-nexus.json"), "a") as fh:
                fh.write(response.text + "\n")
            print("[*] Nexus anonymous repository access Whooops.. [*]\n")
        else:
            print("[*] Nexus requires authentication. [*]\n")
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        print(e)
        print("[*] Nothing Found on IP:" + ip + " [*]\n")


def main():
    api = shodan.Shodan(get_api_key())
    result = api.search(SEARCH_FOR)
    for service in result["matches"]:
        grab_repos(service["ip_str"], str(service["port"]))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
