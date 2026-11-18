"""Lecture du classeur « Tarifs & contenus » telle que la fera l'outil de devis.

Prototype de référence pour le futur lecteur Apps Script : mêmes règles.
- Un bloc commence à une cellule de la colonne A dont le texte débute par « ■ ».
- La ligne suivante contient les en-têtes ; chaque ligne de données devient un
  dictionnaire {en-tête: valeur}. Les colonnes sont repérées par leur nom.
- Une ligne entièrement vide est ignorée ; le bloc s'arrête au « ■ » suivant.
"""
import sys

from openpyxl import load_workbook


def lire_onglet(ws):
    blocs, courant, entetes = {}, None, None
    for row in ws.iter_rows(values_only=True):
        premiere = row[0] if row else None
        if isinstance(premiere, str) and premiere.startswith("■"):
            courant, entetes = premiere.lstrip("■ ").strip(), None
            blocs[courant] = []
            continue
        if courant is None:
            continue
        if entetes is None:
            entetes = [str(v).strip() if v is not None else None for v in row]
            continue
        if all(v is None or (isinstance(v, str) and not v.strip()) for v in row):
            continue
        blocs[courant].append({h: v for h, v in zip(entetes, row) if h})
    return blocs


def lire_classeur(chemin):
    wb = load_workbook(chemin)
    return {ws.title: lire_onglet(ws) for ws in wb.worksheets if ws.title != "Mode d'emploi"}


def controler(classeur):
    """Contrôles de cohérence : renvoie la liste des anomalies trouvées."""
    anomalies = []
    for onglet, blocs in classeur.items():
        options = blocs.get("OPTIONS", [])
        noms = {o.get("Option") for o in options if o.get("Option")}
        groupes = {o.get("Groupe") for o in options if o.get("Groupe")}
        for o in options:
            if o.get("Option") and not o.get("Groupe"):
                anomalies.append(f"{onglet} : option sans groupe « {o['Option']} »")
            for regle in ("Nécessite", "Exclut"):
                cible = o.get(regle)
                if cible and cible not in noms | groupes:
                    anomalies.append(f"{onglet} : « {o.get('Option')} » {regle.lower()} « {cible} » introuvable")
            prix = o.get("Prix TTC")
            if prix is not None and not isinstance(prix, (int, float)):
                anomalies.append(f"{onglet} : prix non numérique pour « {o.get('Option')} » ({prix!r})")
        modeles = blocs.get("MODÈLES", [])
        cibles = {"Tous"} | {m.get("Modèle") for m in modeles} | {m.get("Version") for m in modeles if m.get("Version")}
        for a in blocs.get("ARGUMENTS & PHOTOS", []):
            if a.get("Titre") and a.get("Valable pour") not in cibles:
                anomalies.append(f"{onglet} : argument « {a['Titre']} » valable pour « {a.get('Valable pour')} » inconnu")
        for m in modeles:
            prix = m.get("Prix TTC")
            if prix is not None and not isinstance(prix, (int, float)):
                anomalies.append(f"{onglet} : prix non numérique pour le modèle « {m.get('Modèle')} »")
    return anomalies


if __name__ == "__main__":
    c = lire_classeur(sys.argv[1])
    for onglet, blocs in c.items():
        print(onglet, {b: len(l) for b, l in blocs.items()})
    print("Anomalies :", controler(c) or "aucune")
