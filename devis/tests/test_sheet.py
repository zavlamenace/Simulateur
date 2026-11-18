"""Tests du classeur Tarifs & contenus : structure, cohérence, robustesse.

Lancer depuis la racine du dépôt : python3 -I -m pytest devis/tests -q
(ou python3 -I devis/tests/test_sheet.py sans pytest).
"""
import json
import sys
import tempfile
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE / "devis" / "outils"))

from openpyxl import load_workbook  # noqa: E402

import construire_sheet  # noqa: E402
from lire_sheet import controler, lire_classeur, lire_onglet  # noqa: E402

DONNEES = RACINE / "devis" / "donnees"


def construire(tmp):
    sortie = Path(tmp) / "classeur.xlsx"
    sys.argv = ["construire_sheet.py", str(DONNEES), str(sortie)]
    construire_sheet.main()
    return sortie


def test_structure_et_coherence():
    with tempfile.TemporaryDirectory() as tmp:
        c = lire_classeur(construire(tmp))
    for gamme in ("Référence", "Design", "Prestige", "Lafuge"):
        assert {"GAMME", "MODÈLES", "OPTIONS", "ARGUMENTS & PHOTOS"} <= set(c[gamme]), gamme
    assert len(c["Référence"]["MODÈLES"]) == 12
    assert len(c["Design"]["MODÈLES"]) == 4
    assert len(c["Prestige"]["MODÈLES"]) == 13
    assert len(c["Coloris"]["COLORIS"]) == 4 + 26 + 7
    assert controler(c) == []


def test_prix_reference_identiques_au_site():
    ref = json.loads((DONNEES / "reference.json").read_text(encoding="utf-8"))
    attendus = {(m["modele"], m["version"]): m["prix_ttc"] for m in ref["modeles"]}
    with tempfile.TemporaryDirectory() as tmp:
        lus = {(m["Modèle"], m["Version"]): m["Prix TTC"] for m in lire_classeur(construire(tmp))["Référence"]["MODÈLES"]}
    assert lus == attendus


def test_regles_metier_reference():
    with tempfile.TemporaryDirectory() as tmp:
        c = lire_classeur(construire(tmp))
    gamme = {p["Paramètre"]: p["Valeur"] for p in c["Référence"]["GAMME"]}
    assert not gamme["Atelier affiché sur le devis"], "aucune mention d'origine pour la Référence"
    assert gamme["Valeur du kit accessoires"] == 330
    textes = " ".join(str(v) for b in c["Référence"].values() for l in b for v in l.values() if v)
    assert "italienne" not in textes.lower()
    assert "fabriqu" not in " ".join(str(a["Texte"]) for a in c["Référence"]["ARGUMENTS & PHOTOS"]).lower()


def test_decisions_du_17_11():
    with tempfile.TemporaryDirectory() as tmp:
        c = lire_classeur(construire(tmp))
    ref = c["Référence"]
    assert all(m["Statut"] == "Masqué" for m in ref["MODÈLES"] if m["Modèle"] == "Panama")
    assert not any("PMMA" in str(o.get("Option")) for o in ref["OPTIONS"])
    ral = next(o for o in ref["OPTIONS"] if o.get("Option") == "Pieds couleur RAL au choix")
    assert ral["Statut"] == "Bientôt"
    for gamme in ("Référence", "Design", "Prestige", "Lafuge"):
        args = c[gamme]["ARGUMENTS & PHOTOS"]
        assert sum(1 for a in args if a["Valable pour"] == "Tous") >= 4, gamme
        textes = " ".join(str(a["Texte"]) for a in args)
        assert ("Monaco" in textes) == (gamme == "Lafuge"), "références clients réservées à Lafuge"
    finitions = {a["Valable pour"] for a in ref["ARGUMENTS & PHOTOS"] if a["Valable pour"] != "Tous"}
    assert {"Santiago", "Rio", "Caracas", "Bogota", "Mendoza"} <= finitions


def test_insertion_ligne_et_colonne_ne_change_rien():
    with tempfile.TemporaryDirectory() as tmp:
        chemin = construire(tmp)
        avant = lire_onglet(load_workbook(chemin)["Design"])
        wb = load_workbook(chemin)
        ws = wb["Design"]
        ligne_options = next(r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value == "■ OPTIONS")
        ws.insert_rows(ligne_options + 3)
        ws.insert_cols(3)
        ws.cell(ligne_options + 1, 3, "Colonne ajoutée par l'utilisateur")
        wb.save(chemin)
        apres = lire_onglet(load_workbook(chemin)["Design"])
    for bloc in avant:
        nettoyes = [{k: v for k, v in l.items() if k != "Colonne ajoutée par l'utilisateur"} for l in apres[bloc]]
        assert nettoyes == avant[bloc], bloc


if __name__ == "__main__":
    for nom, f in list(globals().items()):
        if nom.startswith("test_"):
            f()
            print("ok", nom)
