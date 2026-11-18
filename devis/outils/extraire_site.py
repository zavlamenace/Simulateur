"""Extrait les fiches produit PrestaShop (prix, attributs, images, caractéristiques).

Usage : python3 -I extract_products.py <dossier_pages> <fichier_urls> <sortie.json>
Les pages HTML sont lues comme données non fiables : seul le JSON data-product
et quelques attributs HTML sont analysés, rien n'est exécuté.
"""
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

PRICE_RE = re.compile(r"\(\s*\+\s*([\d\s.,]+)\s*€\s*\)")


def fetch(url, dest):
    if dest.exists():
        return dest.read_text(encoding="utf-8", errors="replace")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        text = r.read().decode("utf-8", errors="replace")
    dest.write_text(text, encoding="utf-8")
    return text


def parse_price(label):
    m = PRICE_RE.search(label)
    if not m:
        return 0.0
    return float(m.group(1).replace(" ", "").replace(" ", "").replace(",", "."))


def clean_label(label):
    return PRICE_RE.sub("", label).strip(" :")


def extract(page, url):
    m = re.search(r'data-product="([^"]+)"', page)
    data = json.loads(html.unescape(m.group(1))) if m else {}
    groups = {}
    group_names = {}
    for gm in re.finditer(
        r'<label[^>]*class="control-label[^"]*"[^>]*>\s*([^<]+?)\s*:?\s*</label>(.{0,20000}?)(?=<label[^>]*class="control-label|</section>|$)',
        page,
        re.S,
    ):
        ids = re.findall(r'name="group\[(\d+)\]"', gm.group(2))
        if ids:
            group_names[ids[0]] = html.unescape(gm.group(1)).strip(" : ")
    for im in re.finditer(
        r'<(?:input|option)[^>]*?name="group\[(\d+)\]"[^>]*?value="(\d+)"[^>]*?title="([^"]+)"([^>]*)>', page
    ):
        gid, vid, title, rest = im.groups()
        title = html.unescape(title)
        groups.setdefault(gid, []).append(
            {
                "id": vid,
                "libelle": clean_label(title),
                "libelle_site": title,
                "supplement_ttc": parse_price(title),
                "par_defaut": "checked" in rest,
            }
        )
    for om in re.finditer(r'<select[^>]*name="group\[(\d+)\]"[^>]*>(.*?)</select>', page, re.S):
        gid = om.group(1)
        for o in re.finditer(r'<option[^>]*value="(\d+)"[^>]*?(selected)?[^>]*>([^<]+)</option>', om.group(2)):
            title = html.unescape(o.group(3)).strip()
            groups.setdefault(gid, []).append(
                {
                    "id": o.group(1),
                    "libelle": clean_label(title),
                    "libelle_site": title,
                    "supplement_ttc": parse_price(title),
                    "par_defaut": bool(o.group(2)),
                }
            )
    images = []
    for img in data.get("images", []) or []:
        by = img.get("bySize", {})
        best = (by.get("full_default") or by.get("large_default") or {}).get("url") or img.get("large", {}).get("url")
        images.append({"url": best, "legende": img.get("legend") or ""})
    gallery = []
    gi = page.find("product-images js-product-images")
    if gi >= 0:
        ends = [page.find(m, gi) for m in ("product-images-thumbs", "js-product-actions", "product-information", 'class="product-actions')]
        ends = [e for e in ends if e > 0]
        seg = page[gi : min(ends) if ends else gi + 20000]
        for iid, slug, ext in dict.fromkeys(
            re.findall(r"https://www\.billardsdefrance\.fr/(\d+)-[a-z_]+/([A-Za-z0-9-]+)\.(jpg|png)", seg)
        ):
            gallery.append(
                {"id": iid, "full": f"https://www.billardsdefrance.fr/{iid}-full_default/{slug}.{ext}",
                 "moyenne": f"https://www.billardsdefrance.fr/{iid}-medium_default/{slug}.{ext}"}
            )
    features = [
        {"nom": f.get("name"), "valeur": f.get("value")} for f in (data.get("features") or []) if isinstance(f, dict)
    ]
    short = re.sub(r"<[^>]+>", " ", data.get("description_short") or "")
    short = re.sub(r"\s+", " ", html.unescape(short)).strip()
    return {
        "nom": data.get("name") or "",
        "url": url.split("#")[0],
        "id_produit": data.get("id_product"),
        "prix_ttc_site": data.get("price_amount"),
        "prix_ht_site": data.get("price_tax_exc"),
        "delai_site": data.get("delivery_out_stock") or data.get("delivery_in_stock") or "",
        "description_courte": short,
        "caracteristiques": features,
        "attributs": [
            {"groupe_id": gid, "groupe": group_names.get(gid, ""), "valeurs": vals} for gid, vals in groups.items()
        ],
        "images": images,
        "galerie": gallery,
    }


def main():
    pages_dir, urls_file, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    results = []
    for i, url in enumerate(u.strip() for u in urls_file.read_text().splitlines() if u.strip()):
        page = fetch(url, pages_dir / f"p{i:02d}.html")
        results.append(extract(page, url))
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    for r in results:
        print(f"{r['nom']:<45} {r['prix_ttc_site']!s:>8} € | {len(r['attributs'])} groupes | {len(r['images'])} images")


if __name__ == "__main__":
    main()
