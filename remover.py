"""Itens: "video.mp4" ou "video.mp4|instagram" (só posts que incluem essa rede).
Remove da agenda do Zernio os posts agendados cujos vídeos estão em remover.json (lista de arquivos). Não apaga os arquivos."""
import json, os, urllib.request
API = "https://zernio.com/api/v1"; KEY = os.environ["ZERNIO_API_KEY"]
DRY = os.environ.get("TESTE") == "true"
def call(method, path):
    req = urllib.request.Request(API + path, method=method, headers={"Authorization": f"Bearer {KEY}"})
    try:
        with urllib.request.urlopen(req) as r: return r.status
    except urllib.error.HTTPError as e: return e.code
alvo = json.load(open("remover.json"))
req = urllib.request.Request(API + "/posts?status=scheduled&limit=100", headers={"Authorization": f"Bearer {KEY}"})
posts = json.loads(urllib.request.urlopen(req).read()).get("posts", [])
for p in posts:
    urls = " ".join(m.get("url", "") for m in p.get("mediaItems", []))
    plats = {x.get("platform") for x in p.get("platforms", [])}
    for item in alvo:
        v, _, so = item.partition("|")  # "video.mp4" ou "video.mp4|instagram"
        if v in urls and (not so or so in plats):
            print(v, p.get("scheduledFor"), "teste" if DRY else call("DELETE", f'/posts/{p["_id"]}'))
