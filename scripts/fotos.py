# Baixa as fotos listadas em fotos-drive.json (pasta "Porta-retrato" do Google Drive),
# reduz pro tamanho do iPad e gera fotos.json. Roda no GitHub Actions.
import json, os, io, urllib.request
from PIL import Image, ImageOps
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except Exception:
    pass

lista = json.load(open("fotos-drive.json", encoding="utf-8")).get("fotos", [])
os.makedirs("fotos", exist_ok=True)
quero = []
for f in lista:
    destino = "fotos/%s.jpg" % f["id"]
    if not os.path.exists(destino):
        try:
            url = "https://drive.google.com/uc?export=download&id=" + f["id"]
            dados = urllib.request.urlopen(url, timeout=60).read()
            im = ImageOps.exif_transpose(Image.open(io.BytesIO(dados))).convert("RGB")
            im.thumbnail((1280, 1280))
            im.save(destino, quality=80, optimize=True)
            print("baixada", f["nome"])
        except Exception as e:
            print("falhou", f["nome"], e)
            continue
    quero.append(destino)
for nome in os.listdir("fotos"):
    if "fotos/" + nome not in quero:
        os.remove("fotos/" + nome)
json.dump({"fotos": quero}, open("fotos.json", "w"), indent=1)
