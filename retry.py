"""Reenvia as redes que falharam em posts 'partial'/'failed' e confere as contas dos agendados."""
import json, os, urllib.request
API = "https://zernio.com/api/v1"; KEY = os.environ["ZERNIO_API_KEY"]
def call(m, p):
    r = urllib.request.Request(API + p, method=m, headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r) as x: return x.status, json.loads(x.read() or b"{}")
    except urllib.error.HTTPError as e: return e.code, e.read().decode()[:400]
st, d = call("GET", "/accounts")
contas = {a.get("_id") or a.get("id"): (a.get("platform"), a.get("username")) for a in d.get("accounts", [])}
print("Contas:", list(contas.values()))
for status in ("partial", "failed"):
    for p in call("GET", f"/posts?status={status}&limit=50")[1].get("posts", []):
        st, r = call("POST", f'/posts/{p["_id"]}/retry')
        print("retry", p["_id"], st, [(x.get("platform"), x.get("status"), x.get("platformPostUrl"), (x.get("errorMessage") or "")[:100]) for x in (r.get("post", {}).get("platforms", []) if isinstance(r, dict) else [])] or r)
for p in call("GET", "/posts?status=scheduled&limit=50")[1].get("posts", []):
    vid = " ".join(m.get("url", "").split("/")[-1] for m in p.get("mediaItems", []))
    acc = [x.get("accountId") if isinstance(x.get("accountId"), str) else (x.get("accountId") or {}).get("_id") for x in p.get("platforms", [])]
    print("agendado", vid, p.get("scheduledFor"), ["ok" if a in contas else f"CONTA SUMIU {a}" for a in acc])
