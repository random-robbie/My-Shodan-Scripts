# Shodan Queries

Every Shodan query used by the scripts in this collection, in one place — paste
them straight into the [Shodan search UI](https://www.shodan.io/search) if you
would rather look at results than run a script. The scripts do the same search
and then probe each result with the request documented in the table in the
[README](README.md#scripts).

Set your API key once and run any script from the repository root:

```bash
export SHODAN_API_KEY=your-key-here
python3 docker/docker.py
```

## Application and infrastructure

| Script | Shodan query |
|---|---|
| `Confluence/confluence.py` | `confluence` |
| `docker/docker.py` | `port:2375 product:"Docker"` |
| `etcd/etcd.py` | `port:"2379" product:"etcd"` |
| `flowise/flowise.py` | `port:3000 http.html:"Flowise"` and `port:7860 http.title:"Langflow"` |
| `gitlab/gitlab.py` | `http.title:"GitLab"` |
| `grafana/grafana.py` | `title:"Grafana" port:"443"` |
| `GetSimpleCMS/cms.py` | `html:"GetSimple" country:"US" port:443` |
| `Jaspersoft/jasper.py` | `title:"TIBCO Jaspersoft:" port:"443" 1970"` |
| `Jenkins/jenkins.py` | `x-jenkins 200` |
| `Jira/jira.py` | `http.component:jira` |
| `jupyter/jupyter.py` | `product:"Jupyter Notebook"` |
| `Kibana/kib.py` | `http.component:"kibana" port:"443" -country:cn,fr,se,es,sg` |
| `kubernetes/kubernetes.py` | `ssl:"company x"` — replace with the target company name |
| `kafkaui/kafkaui.py` | `http.title:"Kafka UI"` |
| `litellm/litellm.py` | `http.title:"LiteLLM"` |
| `minio/minio.py` | `product:"MinIO"` |
| `n8n/n8n.py` | `port:5678 http.html:"n8n"` |
| `nodered/nodered.py` | `http.title:"Node-RED"` |
| `Nuxeo/nux.py` | `/nuxeo/ country:"US" port:"443"` |
| `ollama/ollama.py` | `port:11434 http.html:"Ollama is running" country:"US"` |
| `oodo/oodo.py` | `title:"odoo"` |
| `openwebui/openwebui.py` | `http.title:"Open WebUI"` |
| `op5/op5.py` | `title:"op5"` |
| `openfire/openfire.py` | `title:"Openfire Admin Console"` |
| `portainer/portainer.py` | `http.title:"Portainer"` |
| `rabbitmq/rabbitmq.py` | `product:"RabbitMQ" port:"15672"` |
| `ray/ray.py` | `port:8265 http.title:"Ray"` |
| `retool/retool.py` | `http.html:"Retool"` |
| `registry/registry.py` | `port:5000 "Docker-Distribution-API-Version"` |
| `Shipyard/shipyard.py` | `title:"shipyard"` |
| `simplehttp/simple.py` | `product:"SimpleHTTPServer"` |
| `SonarQube/sonar.py` | `http.favicon.hash:1485257654` |
| `splunk/splunk.py` | `title:"splunkd" org:"Amazon.com"` |
| `splunk-info/splunk-info.py` | `splunkd port:"8000"` |
| `Symfony/symfony.py` | `"X-Debug-Token-Link" port:443` |
| `tomcat/tomcat-webinf.py` | `country:"US" org:"Amazon.com" product:"Apache Tomcat/Coyote JSP engine" os:"Windows 7 or 8"` |
| `traefik/traefik.py` | `title:"Traefik"` |
| `weblogic/weblogic.py` | `product:"Oracle Weblogic" port:"7001" country:"US"` |
| `wamp-xdebug/wamp-xdebug.py` | `title:"WAMPSERVER Homepage" country:"US"` |

## Network devices and CVEs

| Script | Shodan query |
|---|---|
| `assets/assets.py` | `SSL:"COMPANY NAME FROM SSL CERT" -"AkamaiGHost" -"GHost"` — replace with the target company name |
| `astra/astra.py` | `html:"Astra Control Panel"` |
| `cisco/cisco.py`, `cisco/asa-2020.py` | `webvpn port:"443"` |
| `django/django.py` | `title:"DisallowedHost"` |
| `dvr/dvr-login.py` | `html:"/login.rsp"` |
| `gsoap/gsoap.py` | `gSOAP/2.8 country:us` |
| `NetSuveillance/netsuv.py` | `title:"NETSurveillance WEB"` |
| `nessus/nessus.py` | `title:"Nessus"` |
| `sap/sap-add-admin.py` | `netweaver` |
| `stalker-m3u/stalker-m3u.py` | `title:"stalker_portal"` |

## IP cameras and webcams

| Script | Shodan query |
|---|---|
| `androidcam/androidcam.py` | `title:"Android Webcam Server"` |
| `boa/boa.py` | `Wireless Day/Night IP Camera` |
| `cams/cams.py` | `has_screenshot:true port:554` |
| `engima2_*/` (cline, movies, stream, watching) | `title:'Open Webif'` |
| `fos-streamer/fos.py` | `title:"FOS-Streaming panel by Tyfix"` |
| `IP Webcam/ipwebcam.py` | `title:"IP Webcam"` |
| `IPCAM/ipcam.py` | `Server: thttpd Basic realm="index.html"` |
| `lilin/liln.py` | `WWW-Authenticate: Basic realm="Merit LILIN Ent. Co., Ltd."` |
| `maygion/maygion.py` | `IPCamera_Logo` |
| `mobotix/mobotix.py` | `http.component:"mobotix"` |
| `netwave/netwave.py` | `Server: Netwave IP Camera` |
| `SecuritySpy/securityspy.py` | `title:SecuritySpy` |
| `tenvis/tenvis.py` | `GoAhead-Webs/2.5.0  realm="IPCamera"` |
| `uc_http/uchttp.py` | `Server: uc-httpd 1.0.0` |
| `zte/zte.py` | `title:"F460" "Mini web server 1.0 ZTE corp 2005" port:"80"` |

## Notes

- Some queries include `country:` or `org:` filters that were relevant when the
  script was written — widen them as needed.
- `assets/assets.py` and `kubernetes/kubernetes.py` need the company name
  edited into the query before running.
- `enigma2_messages/enigma2_message.py` takes its arguments on the command
  line instead of using a stored query — see the script for options.
