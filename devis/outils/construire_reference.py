"""Construit le catalogue Référence Premium à partir de l'extraction du site.

Usage : python3 -I construire_reference.py <reference-site.json> <sortie reference.json>

Entrée : JSON produit par extraire_site.py (fiches produit brutes).
Sortie : modèles avec photos classées (détourée billard ouvert, détourée plateau
bois, détourée plateau verre, gros plans, ambiances) et options communes,
après contrôle que les suppléments sont identiques sur toutes les fiches.
"""
import json
import sys
from collections import defaultdict

# Classement visuel des photos de galerie (vérifié sur planche contact, nov. 2026).
OUVERT = {"3700", "3779", "3803", "3730", "3850", "3874", "3900", "3922", "4200", "3754", "3761", "3092"}
PLATEAU_BOIS = {"3701", "3780", "3804", "3731", "3851", "3875", "3898", "3923", "3948", "3755", "3762", "3093"}
PLATEAU_VERRE = {"3702", "3781", "3805", "3732", "3852", "3876", "3899", "3924", "3949", "3756", "3763", "3094"}
DETAIL = {"3802", "3728", "3849", "3873", "3897", "3904", "3945", "3753"}

GROUPES = {
    "17": "Tapis",
    "7": "Jeu",
    "5": "Montage (ancienne grille)",
    "6": "Dessus de table",
    "33": "Plugs billard français",
    "54": "Couleur des pieds métalliques",
}


def feature(prod, name):
    return next((f["valeur"] for f in prod["caracteristiques"] if f["nom"] == name), "")


def main():
    raw = json.load(open(sys.argv[1], encoding="utf-8"))
    modeles, options, ecarts = [], defaultdict(dict), []
    for p in raw:
        gal = p["galerie"]
        pick = lambda s: next((g["full"] for g in gal if g["id"] in s), "")
        metal = "métal" in p["nom"].lower()
        modeles.append(
            {
                "modele": p["nom"].replace("Billard ", "").replace(" pieds métalliques", ""),
                "version": "Pieds métalliques" if metal else "Pieds bois massif",
                "finition": feature(p, "Finition"),
                "pieds": feature(p, "Pieds"),
                "prix_ttc": p["prix_ttc_site"],
                "url": p["url"],
                "photo_detouree": pick(OUVERT),
                "photo_plateau_bois": pick(PLATEAU_BOIS),
                "photo_plateau_verre": pick(PLATEAU_VERRE),
                "photos_detail": [g["full"] for g in gal if g["id"] in DETAIL],
                "photos_ambiance": [
                    g["full"] for g in gal if g["id"] not in OUVERT | PLATEAU_BOIS | PLATEAU_VERRE | DETAIL
                ],
            }
        )
        for a in p["attributs"]:
            nom = GROUPES.get(a["groupe_id"], a["groupe"] or a["groupe_id"])
            for v in a["valeurs"]:
                prev = options[nom].get(v["libelle"])
                if prev is not None and prev != v["supplement_ttc"]:
                    ecarts.append(f"{p['nom']} / {nom} / {v['libelle']}: {prev} ≠ {v['supplement_ttc']}")
                options[nom][v["libelle"]] = v["supplement_ttc"]
    out = {"modeles": modeles, "options_site": options, "ecarts": ecarts}
    json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    manquantes = [m["modele"] + " " + m["version"] for m in modeles if not m["photo_detouree"]]
    print(f"{len(modeles)} modèles ; photos détourées manquantes : {manquantes or 'aucune'}")
    print(f"écarts de supplément entre fiches : {ecarts or 'aucun'}")


if __name__ == "__main__":
    main()
