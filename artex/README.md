# ARTEX backdoor checker

Searches Shodan for exposed [ARTEX](https://github.com/Autumn-27/artex) AI
pentesting consoles and identifies which of them serve the backdoored Docker
build from the `tomicdd/artex` supply-chain attack. Both backdoored images
(`tomicdd/artex` and the byte-identical re-push `congdonglinux/artex`) were
removed from Docker Hub on 5 November 2026, but every copy already pulled or
cached on a mirror is still backdoored. See
[Badbyte's write-up](https://badbyte.io/artex-backdoor-docker-image/) for the
full analysis.

## The backdoor

The trojanized image adds a hidden `verifyCaptcha()` to the login handler. A
POST to `/api/auth/login` whose JSON body contains a `captcha` field starting
with a secret marker runs the rest of the field through `sh -c` as root and
returns the output — before any credential check. No account, no valid
credentials, one request per command.

## How this script detects it without triggering it

- The backdoored build serves a fixed UI build ID on every page:
  `3aC1db3gGU08O4UHbAt4J`. Shodan indexes that HTML, so
  `http.html:"3aC1db3gGU08O4UHbAt4J"` finds backdoored consoles directly.
- The script then does one plain `GET /` per host — the same check you would
  run against your own install — to confirm the host is still live and still
  serving that build ID.

**It never sends a POST to `/api/auth/login`.** The `captcha` field *is* the
backdoor; triggering it on systems you do not own is unauthorised access, and
a defender does not need it — the build ID in the served HTML is conclusive.

## Proof of concept

The trigger is public: Antiy CERT's sample analysis
([cn-sec.com, 6 Nov 2026](https://cn-sec.com/archives/5559441.html)) recovered
it from the binary — `.symtab` symbols `server.authLogin` / `server.verifyCaptcha`,
then the decompiled login handler. The "secret marker" Badbyte withheld is a
single `!`: a `captcha` field starting with `!` runs the rest of the field
through `sh -c` as root and returns combined stdout+stderr in the response
`captcha` field, before any credential check:

```http
POST /api/auth/login HTTP/1.1
Content-Type: application/json

{"username":"x","password":"x","captcha":"!id"}

HTTP/1.1 200 OK

{"captcha":"uid=0(root) gid=0(root) groups=0(root)\n","error":""}
```

Use it only against an ARTEX console you own. This is unauthenticated root
code execution; against anyone else's console it is a crime, not a test.

**Non-executing build check.** The same endpoint separates the backdoored
build without running anything. The implant's handler branches on the
`captcha` field, which the official build does not have (unknown JSON keys
are ignored, so normal auth runs):

| Request body to `POST /api/auth/login` | Backdoored build | Clean build |
|---|---|---|
| `{"username":"x","password":"x","captcha":"probe"}` | `400 {"error":"captcha error"}` | `401 {"error":"invalid credentials"}` |

A non-`!` value cannot reach `verifyCaptcha`, so no command executes — but a
`400 {"error":"captcha error"}` response proves the implant's login branch is
present. This probe is what you can run against your own instance when the
build ID check is inconclusive (e.g. a rebuilt image you suspect is the
trojan recompiled).

**Log detection.** The official client sends only `username` and `password`,
so any POST to `/api/auth/login` whose body contains a `captcha` key is
anomalous, and `captcha` starting with `!` is a confirmed trigger. Go's JSON
decoder matches keys case-insensitively, so match `captcha` in any case. A
login response whose body contains shell output (`uid=`, command errors) is a
confirmed compromise; the trigger looks like a failed login, so match response
content, not status codes. On the host, alert on `sh -c` spawned by `/app/artex`.

## Output (in `cfg/`)

| File | Contents |
|---|---|
| `backdoored.txt` | `ip:port` of every live host serving the backdoored build |
| `backdoored-details.txt` | `ip:port\|country\|org\|shodan timestamp\|matched query` |
| `other-builds.txt` | `ip:port` of live ARTEX consoles serving some other build |
| `html/<ip>_<port>.html` | root page of each backdoored host, as evidence |

A console *without* the build ID is not proven clean: the trojan was built
from uncommitted source, so a rebuilt copy looks identical to a clean
self-build from the outside. Absence of the build ID means "different build",
not "safe".

## Cleanup for owners

Rebuild from a clean image (`ruoji6/artex` or build the source yourself) and
treat the `data` volume and environment as compromised: the container runs as
root and holds the database password (`ARTEX_PG_DSN`), LLM provider API keys
(`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`), harvested target credentials and the
session signing key (`/app/jwt.key`) in plaintext.
