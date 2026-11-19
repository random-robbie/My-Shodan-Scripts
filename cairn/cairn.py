#!/usr/bin/env python3
#
# cairn.py
# Search SHODAN for exposed Cairn servers (oritera/Cairn) and confirm them
# with read-only requests only.
#
# Cairn is a general-purpose AI state-space search engine, validated first on
# autonomous penetration testing (arXiv:2609.32700). The cairn-server component
# keeps a shared fact-intent board that its dispatcher and agent workers read
# and write through an HTTP API. That API ships with no authentication at all:
# anyone who can reach the server can list and export every project, read the
# facts (which often name the targets and findings of the operator's pentest
# or CTF work), create and delete projects, and post hints that the dispatcher
# feeds to running agent workers — i.e. steer somebody's autonomous agents.
#
# Detection is passive: one GET of /openapi.json (its info.title is "Cairn"
# and it carries the app version), plus read-only GETs of /projects and
# /settings to show what an anonymous visitor sees. This script never issues
# a POST, PUT or DELETE — the board API accepts those unauthenticated, and
# touching another operator's projects or agents is unauthorised access.
#
# Fingerprinting: the page title "Cairn" alone is useless on Shodan (the
# cairn.info academic publisher matches it), so the queries anchor on what
# only the Cairn single-page UI serves: the unique "reason-chip-running" CSS
# class in current builds, and the cytoscape vendor bundle under /static/
# combined with the title for older or newer builds.
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
# Unique CSS class in the current Cairn UI build; appears in the <style>
# block of every page the server serves, so Shodan indexes it.
MARKER_QUERY = 'http.html:"reason-chip-running"'
# Wider census: the graph UI loads cytoscape from /static/vendor/ and the
# page title is "Cairn". Together they exclude the cairn.info publisher.
CENSUS_QUERY = 'http.title:"Cairn" http.html:"cytoscape"'
CFG_DIR = "cfg"

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


def check_server(ip, port, service):
    """Probe one host with read-only GETs and classify what it serves.

    GET /openapi.json identifies Cairn by its info.title and gives the
    running version; GET /projects and GET /settings show what an anonymous
    visitor can read. Returns a (state, evidence) tuple: "cairn" when the
    OpenAPI title is Cairn, "not-cairn" when something else answers, and
    "no-answer" when the host does not respond.
    """
    scheme = "https" if (service.get("ssl") or port == "443") else "http"
    base = scheme + "://" + ip + ":" + port
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
        "Connection": "close",
        "Accept": "application/json",
    }
    evidence = {
        "ip": ip,
        "port": port,
        "url": base,
        "openapi": None,
        "settings": None,
        "projects": None,
    }
    try:
        response = session.get(base + "/openapi.json", headers=headers, timeout=15, verify=False)
        if response.status_code != 200:
            return "not-cairn", evidence
        try:
            spec = response.json()
        except ValueError:
            return "not-cairn", evidence
        info = spec.get("info") or {}
        if info.get("title") != "Cairn":
            return "not-cairn", evidence
        evidence["openapi"] = {
            "description": info.get("description"),
            "version": info.get("version"),
        }
    except KeyboardInterrupt:
        raise
    except Exception:
        return "no-answer", evidence

    try:
        response = session.get(base + "/projects", headers=headers, timeout=15, verify=False)
        projects = response.json() if response.status_code == 200 else None
        if isinstance(projects, list):
            evidence["projects"] = [
                {
                    "id": project.get("id"),
                    "title": project.get("title"),
                    "status": project.get("status"),
                    "created_at": project.get("created_at"),
                }
                for project in projects
                if isinstance(project, dict)
            ]
    except Exception:
        pass

    try:
        response = session.get(base + "/settings", headers=headers, timeout=15, verify=False)
        if response.status_code == 200:
            evidence["settings"] = response.json()
    except Exception:
        pass

    return "cairn", evidence


def main():
    api = shodan.Shodan(API_KEY)

    hosts = {}
    for label, query in (("UI marker", MARKER_QUERY),
                         ("Cairn census", CENSUS_QUERY)):
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

    confirmed_file = open_output(os.path.join(CFG_DIR, "cairn.txt"), "w")
    details_file = open_output(os.path.join(CFG_DIR, "cairn-details.txt"), "w")

    confirmed, not_cairn, no_answer = 0, 0, 0
    for key in sorted(hosts):
        entry = hosts[key]
        ip, port, service = entry["ip"], entry["port"], entry["service"]
        print("[*] Testing: " + ip + " on Port: " + port + " [*]\n")
        state, evidence = check_server(ip, port, service)
        if state == "cairn":
            confirmed += 1
            confirmed_file.write(key + "\n")
            country = (service.get("location") or {}).get("country_name", "?")
            version = (evidence["openapi"] or {}).get("version") or "?"
            projects = evidence["projects"] or []
            active = sum(1 for project in projects if project.get("status") == "active")
            details_file.write("%s|%s|%s|%s|%d project(s), %d active|%s\n" % (
                key,
                version,
                country,
                service.get("org", "?"),
                len(projects),
                active,
                ",".join(sorted(entry["sources"])),
            ))
            os.makedirs(CFG_DIR, exist_ok=True)
            with open(os.path.join(CFG_DIR, ip + "_" + port + ".json"), "w") as fh:
                import json
                fh.write(json.dumps(evidence, indent=2) + "\n")
            print("[*] Exposed Cairn server on " + key + " (version " + version + ", "
                  + str(len(projects)) + " readable project(s)) Whooops.. [*]\n")
        elif state == "not-cairn":
            not_cairn += 1
            print("[*] Something else answered on IP:" + ip + " [*]\n")
        else:
            no_answer += 1
            print("[*] Nothing Found on IP:" + ip + " [*]\n")

    confirmed_file.close()
    details_file.close()

    print("[*] Done: %d exposed Cairn server(s), %d other service, %d not answering. [*]" % (
        confirmed, not_cairn, no_answer))
    print("[*] Exposed hosts: cfg/cairn.txt (details: cfg/cairn-details.txt, evidence: cfg/<ip>_<port>.json) [*]")
    if confirmed:
        print("[*] Every confirmed server exposes its full board API unauthenticated: anyone can")
        print("[*] read the operator's projects and facts, delete them, or post hints that its")
        print("[*] running agent workers obey. Expose it only behind a VPN or auth proxy. [*]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl-c pressed ...")
    except Exception as e:
        sys.exit("Error: %s" % e)
