"""Lista os posts recentes do Zernio com o status por rede."""
import json, os, urllib.request
KEY = os.environ["ZERNIO_API_KEY"]
for st in ("published", "failed", "scheduled", "publishing", "partial"):
    req = urllib.request.Request(f"https://zernio.com/api/v1/posts?status={st}&limit=100", headers={"Authorization": f"Bearer {KEY}"})
    try:
        d = json.loads(urllib.request.urlopen(req).read())
    except Exception as e:
        print(st, "erro", e); continue
    for p in d.get("posts", []):
        vid = " ".join(m.get("url", "").split("/")[-1] for m in p.get("mediaItems", []))
        plats = [(x.get("platform"), x.get("status"), (x.get("errorMessage") or x.get("error") or "")[:120], x.get("platformPostUrl")) for x in p.get("platforms", [])]
        print(f'[{st}] {p.get("_id")} {vid} {p.get("scheduledFor") or p.get("publishedAt")}')
        for x in plats: print("   ", x)

# desempenho dos publicados (views, curtidas, comentários, compartilhamentos por rede)
try:
    req = urllib.request.Request("https://zernio.com/api/v1/analytics?fromDate=2026-11-01&limit=50&sortBy=views", headers={"Authorization": f"Bearer {KEY}"})
    d = json.loads(urllib.request.urlopen(req).read())
    for p in d.get("posts", []):
        a = p.get("analytics") or {}
        print("[analytics]", (p.get("publishedAt") or "")[:10], "|", (p.get("content") or "")[:50].replace("\n", " "), "|", {k: a.get(k) for k in ("views", "likes", "comments", "shares", "saves")})
        for x in p.get("platforms", []):
            pa = x.get("analytics") or {}
            print("    ", x.get("platform"), {k: pa.get(k) for k in ("views", "likes", "comments", "shares", "saves", "completionRate", "reelsSkipRate", "igReelsAvgWatchTime", "videoDurationSeconds") if pa.get(k) is not None})
except Exception as e:
    print("analytics erro", e)
