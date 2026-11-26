"""Exporte un classeur xlsx (trace ou copie du Sheet) pour le banc d'essai.

Usage : python3 -I exporter_catalogue.py <classeur.xlsx>
Écrit, à côté de ce script :
- catalogue.json : lecture par devis/outils/lire_sheet.py, { onglet: { bloc: [ { en-tête: valeur } ] } } ;
- feuilles.json : valeurs brutes de chaque onglet, telles que getDataRange().getValues() les rend dans Apps Script
  (cellule vide = ""), pour faire tourner le vrai Code.gs dans le banc.
"""
import datetime
import json
import sys
from pathlib import Path

from openpyxl import load_workbook

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI.parent / "outils"))
from lire_sheet import lire_classeur  # noqa: E402


def propre(v):
    if isinstance(v, (datetime.date, datetime.datetime)):
        return v.isoformat()
    return v


def brut(v):
    return "" if v is None else propre(v)


classeur = sys.argv[1]
catalogue = {o: {b: [{k: propre(v) for k, v in l.items()} for l in lignes] for b, lignes in blocs.items()}
             for o, blocs in lire_classeur(classeur).items()}
(ICI / "catalogue.json").write_text(json.dumps(catalogue, ensure_ascii=False, indent=0), encoding="utf-8")

wb = load_workbook(classeur)
feuilles = []
for ws in wb.worksheets:
    valeurs = [[brut(v) for v in ligne] for ligne in ws.iter_rows(values_only=True)]
    feuilles.append({"nom": ws.title, "cachee": ws.sheet_state != "visible", "valeurs": valeurs})
(ICI / "feuilles.json").write_text(json.dumps(feuilles, ensure_ascii=False), encoding="utf-8")
print(f"catalogue.json : {len(catalogue)} onglets ; feuilles.json : {len(feuilles)} feuilles")
