#!/usr/bin/env python3
#
# artex.py
# Search SHODAN for exposed ARTEX AI pentesting consoles and identify which
# ones serve the backdoored build from the tomicdd/artex supply-chain attack
# (Badbyte disclosure, November 2026).
#
# The trojanized Docker image (tomicdd/artex, and the byte-identical re-push
# congdonglinux/artex, both removed from Docker Hub on 5 Nov 2026) adds a
# hidden verifyCaptcha() to the login handler: a POST to /api/auth/login
# whose JSON body contains a "captcha" field starting with a secret marker
# runs the rest of the field through "sh -c" as root and returns the output,
# before any credential check.
#
# Detection without triggering it: the backdoored build serves a fixed UI
# build ID on every page it serves,
#
#     3aC1db3gGU08O4UHbAt4J
#
# so Shodan indexes it (http.html:) and one plain GET of the console root
# page confirms a live host — the same check you would run against your own
# install. This script never POSTs to /api/auth/login; the captcha field IS
# the backdoor and triggering it on systems you do not own is unauthorised
# access.
#
# Author: random_robbie

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import get_api_key, open_output

import shodan
import requests
import urllib3

# Configuration
API_KEY = get_api_key()
BACKDOOR_BUILD_ID = "3aC1db3gGU08O4UHbAt4J"
# Consoles serving the backdoored build: the build ID appears in the HTML of
# every page the backdoored console serves, so Shodan indexes it.
BACKDOOR_QUERY = 'http.html:"3aC1db3gGU08O4UHbAt4J"'
# Wider census of exposed ARTEX consoles (the compose file publishes port
# 8787) so consoles running some other build get listed too.
CENSUS_QUERY = 'port:8787 http.html:"ARTEX"'
CFG_DIR = "cfg"
HTML_DIR = os.path.join(CFG_DIR, "html")

session = requests.Session()
urllib3.disable_warnings()


def iter_hits(api, query):
    """Yield every Shodan banner matching the query.

    Uses a search cursor so all hits are listed; falls back to a single page
    of results when the account does not support cursors.
    """
    try:
        for service in api.search_cursor(query):
            yield service
    except shodan.APIError:
        for service in api.search(query)["matches"]:
            yield service


def check_console(ip, port, service):
    """Fetch the console root page and classify the build it serves.

    One unauthenticated GET, nothing else. Returns a (state, html) tuple:
    "backdoored" when the fixed build ID of the trojanized image is in the
    page, "other-build" when an ARTEX console answers without it, and
    "no-answer" when the host does not respond.
    """
    scheme = "https" if (service.get("ssl") or port == "443") else "http"
    url = scheme + "://" + ip + ":" + port + "/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
        "Connection": "close",
    }
    try:
        response = session.get(url, headers=headers, timeout=15, verify=False)
        html = response.text
    except KeyboardInterrupt:
        raise
    except Exception:
        return "no-answer", None
    if BACKDOOR_BUILD_ID in html:
        return "backdoored", html
    if "ARTEX" in html or "artex" in html:
        return "other-build", html
    return "unidentified", html


def main():
    api = shodan.Shodan(API_KEY)

    hosts = {}
    for label, query in (("backdoored build ID", BACKDOOR_QUERY),
                         ("ARTEX census", CENSUS_QUERY)):
        print("[*] Shodan query (%s): %s [*]\n" % (label, query))
        count = 0
        for service in iter_hits(api, query):
            ip = service.get("ip_str")
            port = str(service.get("port") or "")
            if not ip or not port:
                continue
            key = ip + ":" + port
            entry = hosts.setdefault(key, {"ip": ip, "port": port,
                                           "sources": set(), "service": service})
            entry["sources"].add(label)
            entry["service"] = service
            count += 1
        print("[*] %d Shodan hits for %s [*]\n" % (count, label))

    backdoored_file = open_output(os.path.join(CFG_DIR, "backdoored.txt"), "w")
    details_file = open_output(os.path.join(CFG_DIR, "backdoored-details.txt"), "w")
    other_file = open_output(os.path.join(CFG_DIR, "other-builds.txt"), "w")

    confirmed, other_builds, no_answer = 0, 0, 0
    for key in sorted(hosts):
        entry = hosts[key]
        ip, port, service = entry["ip"], entry["port"], entry["service"]
        print("[*] Testing: " + ip + " on Port: " + port + " [*]\n")
        state, html = check_console(ip, port, service)
        if state == "backdoored":
            confirmed += 1
            backdoored_file.write(key + "\n")
            country = (service.get("location") or {}).get("country_name", "?")
            details_file.write("%s|%s|%s|%s|%s\n" % (
                key,
                country,
                service.get("org", "?"),
                service.get("timestamp", "?"),
                ",".join(sorted(entry["sources"])),
            ))
            os.makedirs(HTML_DIR, exist_ok=True)
            with open(os.path.join(HTML_DIR, ip + "_" + port + ".html"), "w") as fh:
                fh.write(html or "")
            print("[*] BACKDOORED build confirmed on " + key + " Whooops.. [*]\n")
        elif state == "other-build":
            other_builds += 1
            other_file.write(key + "\n")
            print("[*] ARTEX console on " + key + " serves a different build. [*]\n")
        else:
            no_answer += 1
            print("[*] Nothing confirmed on IP:" + ip + " [*]\n")

    backdoored_file.close()
    details_file.close()
    other_file.close()

    print("[*] Done: %d host(s) serving the backdoored build, %d on another build, %d not answering. [*]" % (
        confirmed, other_builds, no_answer))
    print("[*] Backdoored hosts: cfg/backdoored.txt (details: cfg/backdoored-details.txt, evidence: cfg/html/) [*]")
    if confirmed:
        print("[*] Any ARTEX install still pulling from a mirror of tomicdd/artex or")
        print("[*] congdonglinux/artex must be rebuilt from a clean image and its data [*]")
        print("[*] volume treated as compromised (plaintext API keys, DB password, JWT key). [*]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
