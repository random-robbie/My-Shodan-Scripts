#!/usr/bin/env python3
#
# litellm.py
# Search SHODAN for exposed LiteLLM proxies. A misconfigured LiteLLM proxy
# answers /v1/models without a key and can expose the upstream LLM providers
# and their API keys — someone else's OpenAI/Anthropic bill.
#
# Author: random_robbie

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import get_api_key, open_output

import shodan
import requests

# Configuration
SEARCH_FOR = 'http.title:"LiteLLM"'
MODELS_PATH = "/v1/models"
CFG_DIR = "cfg"
session = requests.Session()


def check_models(ip, port):
    """Check whether the model list is served without an API key."""
    print("[*] Testing: " + ip + " on Port: " + port + "[*]\n")
    try:
        url = "http://" + ip + ":" + port + MODELS_PATH
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
            "Connection": "close",
            "Accept": "application/json",
        }
        response = session.get(url, headers=headers, timeout=15, verify=False)
        if response.status_code == 200 and '"data"' in response.text:
            with open_output(os.path.join(CFG_DIR, ip + "-litellm.json"), "a") as fh:
                fh.write(response.text + "\n")
            print("[*] Open LiteLLM proxy Whooops.. [*]\n")
        else:
            print("[*] LiteLLM requires an API key. [*]\n")
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        print(e)
        print("[*] Nothing Found on IP:" + ip + " [*]\n")


def main():
    api = shodan.Shodan(get_api_key())
    result = api.search(SEARCH_FOR)
    for service in result["matches"]:
        check_models(service["ip_str"], str(service["port"]))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
