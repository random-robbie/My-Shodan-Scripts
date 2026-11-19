# Cairn exposure checker

Searches Shodan for exposed [Cairn](https://github.com/oritera/Cairn) servers
and confirms each hit with read-only requests only.

Cairn is a general-purpose AI state-space search engine, validated first on
autonomous penetration testing ([arXiv:2609.32700](https://arxiv.org/abs/2609.32700),
Tencent Cloud Hackathon AI pentest challenge). Its `cairn-server` keeps the
shared fact-intent board that the dispatcher and agent workers coordinate
through — and that board API has **no authentication**.

## Why an exposed Cairn server is a problem

Anyone who can reach the server can, with plain unauthenticated requests:

- list and export every project (`GET /projects`, `GET /projects/{id}/export`)
  — the facts on the board routinely name the targets and findings of the
  operator's pentest or CTF work;
- create, rename, complete and **delete** projects (`POST/PUT/DELETE ...`);
- post `hints` that the dispatcher feeds to running agent workers — steer
  somebody's autonomous agents while they run;
- change `/settings`.

A defender needs none of the write paths to confirm exposure, so this script
never issues a POST, PUT or DELETE — only `GET /openapi.json`, `GET /projects`
and `GET /settings`.

## How it fingerprints Cairn

The page title `"Cairn"` alone is useless on Shodan (the cairn.info academic
publisher matches it). The queries anchor on what only the Cairn single-page
UI serves:

- `http.html:"reason-chip-running"` — a CSS class unique to the current UI
  build, present in the `<style>` block of every page;
- `http.title:"Cairn" http.html:"cytoscape"` — census for other builds: the
  graph UI loads cytoscape from `/static/vendor/` (the Docker Compose default
  port is 8000, but installs move it, so no port filter).

`/openapi.json` is the confirm step: Cairn's spec has `info.title == "Cairn"`
and the running version (0.2.1 on the instance this was written against).

## Output

| File | Contents |
|------|----------|
| `cfg/cairn.txt` | one `ip:port` per confirmed exposed server |
| `cfg/cairn-details.txt` | `ip:port\|version\|country\|org\|project counts\|shodan queries that matched` |
| `cfg/<ip>_<port>.json` | full evidence: OpenAPI info, `/settings`, readable `/projects` entries |

## Usage

```bash
export SHODAN_API_KEY=your-key-here
python3 cairn/cairn.py
```
