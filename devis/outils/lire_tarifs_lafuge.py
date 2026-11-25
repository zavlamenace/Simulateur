"""Relit les tarifs Lafuge Word (extraits en texte) pour le contrôle croisé de lafuge_tarifs.py.

Chaîne d'extraction (documents dans connaissances/sources/lafuge-2027/) :
  soffice --headless --convert-to docx <fichier>.doc
  python3 -I devis/outils/lire_tarifs_lafuge.py --extraire <fichier>.docx > devis/donnees/lafuge-2027/<nom>.txt
Le texte garde l'ordre du document : « P: » pour un paragraphe, « === TABLE » pour un tableau.
"""
import re
import sys
import unicodedata

FICHES_DOC = [
    ("LOFT", "LOFT · ÉLÉGANCE"), ("SOHO", "SOHO"), ("CITY", "CITY · ÉOS"), ("EIFFEL", "EIFFEL · ALPHA"),
    ("BEAUBOURG", "BEAUBOURG"), ("ARCADE", "ARCADE"), ("TROCADERO", "TROCADÉRO"), ("MONT BLANC", "MONT BLANC"),
    ("COMPETITION", "COMPÉTITION"), ("RUSTIC", "RUSTIC · CASTEL"), ("LOUIS PHILIPPE", "LOUIS-PHILIPPE · MANOIR"),
    ("HARMONIE NOYER", "HARMONIE NOYER"), ("HARMONIE ERABLE", "HARMONIE ÉRABLE"), ("CHAMBORD", "CHAMBORD"),
    ("TARIF", None),
]

# Libellé du document → clé d'option (le premier motif qui correspond l'emporte).
CLES = [
    (r"SNOOKER 10", "SNOOKER 10 PIEDS"), (r"SNOOKER 12", "SNOOKER 12 PIEDS"),
    (r"CADRE MELEZE", "Mélèze massif"), (r"CADRE CHENE", "Chêne massif"), (r"LAQUE DU CADRE", "Laque"),
    (r"MELEZE", "Mélèze massif"), (r"CHENE MASSIF", "Chêne massif"), (r"^NOYER", "Noyer massif"),
    (r"PARCHEMIN", "Finition parchemin, patine antiquaire ou cérusée"), (r"BROSSEE", "Finition brossée"),
    (r"BICOLORE", "Finition bicolore vernie"), (r"LISERE \(1", "Liseré laqué (Harmonie, supprimé)"),
    (r"^LAQUE|LAQUE SUR|LAQUE \(", "Laque"),
    (r"FABRICATION SPECIALE|LISERE \(ALUMINIUM|LISERE ALUMINIUM", "Liseré aluminium ou bois gainé du drap"),
    (r"LISERE|LISERET|RECHAMPI", "Liseré de couleur"), (r"PLOTS", "Plots Altuglas"),
    (r"REPERES", "Repères de bandes en nacre"), (r"JEU DE BANDE", "2e jeu de bandes interchangeables"),
    (r"ENTREES DE POCHE", "Entrées de poche en cuir noir"), (r"SOFIC", "Cuir de couleur (gamme SOFIC)"),
    (r"6 PIEDS", "Option 6 pieds"), (r"DESCENTE", "Retour centralisé des billes"),
    (r"A ?37", "Bandes A37 toilées"), (r"CHAUFFAGE", "Chauffage de l'ardoise"),
    (r"CADRE DEMONTABLE", "Cadre démontable"), (r"PIETEMENT|LE PIETEMENT", "Piètement démontable"),
]
TAILLE_LIGNE = re.compile(r"^(2M10|2M30|2M40|2M60|2M80|3M10)")


def norm(s):
    s = s.replace("\xa0", " ").replace(" ", " ")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().upper()
    return re.sub(r"\s+", " ", s).strip()


def euros(texte):
    texte = texte.replace("\xa0", " ").replace(" ", " ")
    return [int(x.replace(" ", "")) for x in re.findall(r"(\d{1,3}(?: \d{3})+|\d+)\s*€", texte)]


def lire(chemin):
    """{fiche: {"prix": {"2M30": [nombres]}, "options": {clé: [[nombres], ...]}}} pour les pages billard."""
    out, fiche = {}, None
    for ligne in open(chemin, encoding="utf-8"):
        if not ligne.startswith("P: "):
            continue
        t = ligne[3:].rstrip("\n")
        n = norm(t)
        for motif, nom in FICHES_DOC:
            if n.startswith(motif) and len(n) < 45 and "€" not in t:
                fiche = nom
                if nom:
                    out.setdefault(nom, {"prix": {}, "options": {}})
                break
        if not fiche:
            continue
        m = TAILLE_LIGNE.match(n.replace(" ", ""))
        if m and "€" in t:
            reste = re.sub(r"^\s*\d\s*m\s*\d0", "", t.replace("\xa0", " "), flags=re.I)
            out[fiche]["prix"][m.group(1)] = euros(reste)
            continue
        for motif, cle in CLES:
            if re.search(motif, n):
                if euros(t):
                    out[fiche]["options"].setdefault(cle, []).append(euros(t))
                break
    return out


def extraire(docx):
    from docx import Document
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    doc = Document(docx)
    n = 0
    for enfant in doc.element.body.iterchildren():
        tag = enfant.tag.split("}")[1]
        if tag == "p":
            texte = Paragraph(enfant, doc).text.strip()
            if texte:
                print("P:", texte)
        elif tag == "tbl":
            table = Table(enfant, doc)
            n += 1
            print(f"=== TABLE {n} ({len(table.rows)} lignes)")
            for rang in table.rows:
                vues, prec = [], None
                for c in rang.cells:
                    if c._tc is not prec:
                        vues.append(c.text.strip().replace("\n", " / "))
                    prec = c._tc
                print(" | ".join(vues))


if __name__ == "__main__":
    if sys.argv[1] == "--extraire":
        extraire(sys.argv[2])
    else:
        import json
        print(json.dumps(lire(sys.argv[1]), ensure_ascii=False, indent=1))
