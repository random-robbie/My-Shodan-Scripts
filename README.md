# My-Shodan-Scripts

A collection of Python 3 scripts for searching Shodan and then probing the results. Each script has a hardcoded Shodan API key at the top (`API_KEY = "YOURAPIKEY"`) — replace it with your own key before running, otherwise the scripts will fail. Most scripts take no command-line arguments: run them and they query Shodan, check each result, and save findings to text files in a `cfg` (or similar) directory within the script's folder.

Requires Python 3 with the `shodan` and `requests` libraries:

```bash
pip install shodan requests
```

## Usage

1. Edit the script you want to use and set `API_KEY` to your Shodan API key.
2. Run it with Python 3 from inside the script's directory (most scripts write results relative to the current directory):

```bash
cd Confluence
python3 confluence.py
```

The only script with command-line options is `enigma2_messages/enigma2_message.py`, which sends an on-screen message to an Enigma2 box:

```bash
cd enigma2_messages
python3 enigma2_message.py -H 192.168.1.10 -P 80 -M "Hello World..." -T 30 -E 1
```

Options: `-H/--host` (IP address of the box), `-P/--port` (default 80), `-T/--timeout` (seconds the message stays on screen), `-M/--message` (text to display), `-E/--errortype` (1 = info, 2 = warning, 3 = error, 0 = yes/no).

## Scripts

### Application and infrastructure

| Script | Purpose |
|---|---|
| `Confluence/confluence.py` | Searches Shodan for Confluence and tests the LFI/RCE via the `/rest/tinymce/1/macro/preview` endpoint; found hosts are saved to `cfg/Confluence.cfg`. |
| `Jira/jira.py` | Searches Shodan for Jira servers (`http.component:jira`) and tests the Jira SSRF. |
| `Jenkins/jenkins.py` | Searches Shodan for Jenkins servers (`x-jenkins 200`) and checks for vulnerable instances. |
| `SonarQube/sonar.py` | Searches Shodan for SonarQube instances by favicon hash and checks which ones require no login. |
| `Kibana/kib.py` | Searches Shodan for Kibana (`http.component:"kibana" port:"443"`). |
| `grafana/grafana.py` | Searches Shodan for Grafana (`title:"Grafana" port:"443"`) and tests default credentials; login URLs found are saved to `cfg/default.txt`. |
| `Nuxeo/nux.py` | Searches Shodan for Nuxeo and tests the Nuxeo RCE. |
| `oodo/oodo.py` | Searches Shodan for Odoo and tests the Odoo LFI (CVE-2019-14322). |
| `Symfony/symfony.py` | Searches Shodan for Symfony dev mode (`X-Debug-Token-Link`) to expose PHP info and AWS credentials. |
| `django/django.py` | Searches Shodan for Django servers showing `DisallowedHost` pages that leak AWS keys. |
| `op5/op5.py` | Searches Shodan for OP5 and tests the OP5 RCE. |
| `openfire/openfire.py` | Searches Shodan for the Openfire Admin Console and tests the Openfire SSRF. |
| `splunk/splunk.py` | Searches Shodan for Splunk servers on AWS with default configuration. |
| `splunk-info/splunk-info.py` | Searches Shodan for Splunk and tests the CVE-2018-11409 information disclosure. |
| `sap/sap-add-admin.py` | Searches Shodan for SAP NetWeaver hosts and tests the "add admin" exploit. |
| `weblogic/weblogic.py` | Searches Shodan for Oracle WebLogic on port 7001 and tests for potential RCE. |
| `tomcat/tomcat-webinf.py` | Searches Shodan for Apache Tomcat on Windows and checks for an exposed `WEB-INF/web.xml`. |
| `docker/docker.py` | Searches Shodan for exposed Docker APIs (`port:2375 product:"Docker"`) and attempts container hijack; results are written to `cfg/` and `cfg-hijacked/`. |
| `kubernetes/kubernetes.py` | Searches Shodan by company SSL certificate name and checks whether matched hosts expose the Kubernetes API. |
| `etcd/etcd.py` | Searches Shodan for exposed etcd (`port:"2379" product:"etcd"`) and logs the retrieved files; `grep aws *.cfg` finds leaked keys. |
| `Shipyard/shipyard.py` | Searches Shodan for Shipyard Docker management panels and tries the default credentials. |
| `traefik/traefik.py` | Searches Shodan for Traefik dashboards and checks for certificate leaks. |
| `simplehttp/simple.py` | Searches Shodan for Python SimpleHTTPServer instances. |
| `wamp-xdebug/wamp-xdebug.py` | Searches Shodan for WAMPSERVER homepages and tests the Xdebug RCE. |
| `gsoap/gsoap.py` | Searches Shodan for gSOAP/2.8 services and tests the gSOAP LFI. |
| `Jaspersoft/jasper.py` | Searches Shodan for TIBCO Jaspersoft and tests the LFI (CVE-2018-18809). |
| `GetSimpleCMS/cms.py` | Searches Shodan for GetSimple CMS instances and tests the RCE. |
| `astra/astra.py` | Searches Shodan for Astra IPTV control panels. |
| `stalker-m3u/stalker-m3u.py` | Searches Shodan for Stalker Portal IPTV servers and retrieves M3U playlists. |
| `nessus/nessus.py` | Searches Shodan for Nessus scanners and tries the `admin:admin` login. |
| `ollama/ollama.py` | Searches Shodan for exposed Ollama instances (`port:11434`) and sends a test prompt to the `/api/generate` API; results are written to `output.txt`. |

### Network devices and CVEs

| Script | Purpose |
|---|---|
| `cisco/cisco.py` | Searches Shodan for Cisco devices. |
| `cisco/asa-2020.py` | Searches Shodan for Cisco ASA webvpn hosts and tests CVE-2020-3452 (path traversal). |
| `zte/zte.py` | Searches Shodan for ZTE F460/F660 routers and tests CVE-2014-2321 RCE. |
| `boa/boa.py` | Searches Shodan for Boa HTTP servers on wireless IP cameras with the default `admin` / blank password. |
| `netwave/netwave.py` | Searches Shodan for Netwave IP cameras and tests the path traversal. |
| `uc_http/uchttp.py` | Searches Shodan for `uc-httpd 1.0.0` servers and tests the path traversal. |
| `dvr/dvr-login.py` | Searches Shodan for DVR login pages (`/login.rsp`) and tests CVE-2018-9995 (credential disclosure). |
| `NetSuveillance/netsuv.py` | Searches Shodan for NETSurveillance WEB interfaces. |
| `engima2_cline/engima2_cline.py` | Searches Shodan for Enigma2 OpenWebif boxes and grabs CCcam configuration files. |
| `engima2_movies/movies.py` | Searches Shodan for Enigma2 OpenWebif boxes and lists movies on the box. |
| `engima2_stream/streams.py` | Searches Shodan for Enigma2 OpenWebif boxes and grabs the current stream URL. |
| `engima2_watching/watching.py` | Searches Shodan for Enigma2 OpenWebif boxes and reports which channel they are watching. |
| `enigma2_messages/enigma2_message.py` | Sends a message to the screen of an Enigma2 box (see Usage above). |
| `fos-streamer/fos.py` | Searches Shodan for FOS-Streaming panels and tries the default logins. |
| `assets/assets.py` | Searches Shodan for a company's assets based on the SSL certificate name — edit `SEARCH_FOR` to your target company name. |

### IP cameras and webcams

| Script | Purpose |
|---|---|
| `IP Webcam/ipwebcam.py` | Searches Shodan for the Android "IP Webcam" app. |
| `IPCAM/ipcam.py` | Searches Shodan for ipCAM devices running thttpd. |
| `lilin/liln.py` | Searches Shodan for Merit LILIN IP cameras. |
| `maygion/maygion.py` | Searches Shodan for Maygion cameras with default authentication. |
| `mobotix/mobotix.py` | Searches Shodan for Mobotix CCTV cameras and tries the default credentials. |
| `SecuritySpy/securityspy.py` | Searches Shodan for SecuritySpy camera servers. |
| `androidcam/androidcam.py` | Searches Shodan for Android webcam servers with no authentication. |
| `cams/cams.py` | Searches Shodan for open webcams with screenshots (`has_screenshot:true port:554`). |
| `tenvis/tenvis.py` | Searches Shodan for TENVIS IP cameras with live streams. |

## Author

Robbie Wiggins — [What-Security](https://www.what-security.co.uk) · [GitHub](https://github.com/random-robbie)

## Disclaimer / Authorised use

These scripts are for authorised security testing and responsible disclosure only. Do not use them against systems you do not have permission to test. Use at your own risk — what you do with this code is your responsibility, not mine.
