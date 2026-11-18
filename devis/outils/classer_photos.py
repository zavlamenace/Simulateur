"""Télécharge les miniatures de la galerie et marque les vues détourées (fond blanc).

Usage : python3 -I classify_gallery.py <produits.json> <dossier_images>
Ajoute "detouree": true/false à chaque image de galerie et réécrit le JSON.
"""
import json
import sys
import urllib.request
from pathlib import Path

from PIL import Image


def is_packshot(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    pts = [(int(w * x), int(h * y)) for x in (0.02, 0.5, 0.98) for y in (0.03, 0.97)]
    pts += [(int(w * 0.02), int(h * 0.5)), (int(w * 0.98), int(h * 0.5))]
    return sum(1 for p in pts if min(im.getpixel(p)) >= 232) >= len(pts) - 1


def main():
    src, img_dir = Path(sys.argv[1]), Path(sys.argv[2])
    img_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads(src.read_text(encoding="utf-8"))
    for prod in data:
        for g in prod.get("galerie", []):
            dest = img_dir / f"{g['id']}.jpg"
            if not dest.exists():
                req = urllib.request.Request(g["moyenne"], headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=60) as r:
                    dest.write_bytes(r.read())
            g["detouree"] = is_packshot(dest)
        n = sum(g["detouree"] for g in prod.get("galerie", []))
        print(f"{prod['nom']:<40} {n} détourées / {len(prod.get('galerie', []))}")
    src.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
