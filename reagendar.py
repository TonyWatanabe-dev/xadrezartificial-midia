"""Reagenda posts já agendados no Zernio conforme reagendar.json ({arquivo_video: "AAAA-MM-DDTHH:MM:SS"}, fuso de São Paulo)."""
import json, os, sys, urllib.request
API = "https://zernio.com/api/v1"; KEY = os.environ["ZERNIO_API_KEY"]
DRY = os.environ.get("TESTE") == "true"
def call(method, path, body=None):
    req = urllib.request.Request(API + path, method=method, data=json.dumps(body).encode() if body else None,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r: return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e: return e.code, e.read().decode()[:500]
alvo = json.load(open("reagendar.json"))
st, d = call("GET", "/posts?status=scheduled&limit=100")
posts = d.get("posts", []) if isinstance(d, dict) else []
print("Agendados:", len(posts), st if not posts else "")
for p in posts:
    urls = " ".join(m.get("url", "") for m in p.get("mediaItems", []))
    for video, quando in alvo.items():
        if video in urls:
            print(f'{video}: {p.get("scheduledFor")} -> {quando}')
            if DRY: continue
            body = {"scheduledFor": quando, "timezone": "America/Sao_Paulo"}
            st, r = call("PUT", f'/posts/{p["_id"]}', body)
            if st == 405: st, r = call("PATCH", f'/posts/{p["_id"]}', body)
            print("  ->", st, r.get("post", {}).get("scheduledFor") if isinstance(r, dict) else r)
