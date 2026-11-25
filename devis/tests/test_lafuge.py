"""Contrôle croisé des tarifs Lafuge (lafuge_tarifs.py) avec les 4 documents d'origine.

Seuls écarts admis : les corrections validées avec l'utilisateur (CORRECTIONS_TTC, CORRECTIONS_HT) et les lignes
ajoutées (option sans clé « doc »). Lancer : python3 -I devis/tests/test_lafuge.py
"""
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE / "devis" / "outils"))

import lafuge_tarifs as L  # noqa: E402
from lire_tarifs_lafuge import euros, lire, norm  # noqa: E402

DOCS = RACINE / "devis" / "donnees" / "lafuge-2027"
SOURCES = {("mixte", "TTC"): "pool_vente_ttc.txt", ("mixte", "HT"): "pool_achat_ht.txt",
           ("français", "TTC"): "francais_vente_ttc.txt", ("français", "HT"): "francais_achat_ht.txt"}
COLONNES_DOC = {"mixte": ["2,30 m", "2,40 m", "2,60 m", "2,80 m"], "français": L.TAILLES["français"]}
CODE = {"2M10": "2,10 m", "2M30": "2,30 m", "2M40": "2,40 m", "2M60": "2,60 m", "2M80": "2,80 m", "3M10": "3,10 m"}
IGNORES = {"Liseré laqué (Harmonie, supprimé)", "SNOOKER 10 PIEDS", "SNOOKER 12 PIEDS"}


def fiches(jeu):
    return L.fiches_mixte() if jeu == "mixte" else L.fiches_francais()


def numeriques(option, jeu, f):
    tailles = {t for m in f.modeles.values() for t, v in m.items() if v != L.NP}
    return [option.prix[t] for t in COLONNES_DOC[jeu] if t in tailles and isinstance(option.prix[t], (int, float))]


def concorde(nous, doc):
    return nous == doc or (len(doc) == 1 and nous and all(v == doc[0] for v in nous))


def ecarts(jeu, sorte):
    """Liste des écarts (fiche, option, document, nous) entre nos données et un document."""
    doc = lire(DOCS / SOURCES[(jeu, sorte)])
    conv = (lambda v: v) if sorte == "TTC" else L.ht
    out = []
    for f in fiches(jeu):
        d = doc[f.nom]
        modeles = list(f.modeles.values())
        for code, valeurs in d["prix"].items():
            t = CODE[code]
            attendus = [conv(m[t]) for m in modeles if isinstance(m[t], int)]
            if len({tuple(attendus)}) and len(set(attendus)) > 1:
                if valeurs[:len(attendus)] != attendus:
                    out.append((f.nom, f"prix {t}", valeurs[:len(attendus)], attendus))
            elif valeurs[0] != attendus[0]:
                out.append((f.nom, f"prix {t}", [valeurs[0]], [attendus[0]]))
        for g, rang in (("10 pieds", "SNOOKER 10 PIEDS"), ("12 pieds", "SNOOKER 12 PIEDS")):
            if rang in d["options"]:
                prix, laque, chene = d["options"][rang][0][:3]
                nous = [conv(modeles[0][g]), conv(next(o for o in f.options if o.nom == L.LAQUE).prix[g]),
                        conv(next(o for o in f.options if o.nom == L.CHENE).prix[g])]
                if [prix, laque, chene] != nous:
                    out.append((f.nom, rang, [prix, laque, chene], nous))
        vus = set()
        for o in f.options:
            if not o.doc:
                continue
            vus.add(o.doc)
            if o.doc not in d["options"]:
                out.append((f.nom, o.nom, "absent du document", None))
                continue
            nous = [conv(v) for v in numeriques(o, jeu, f)]
            docv = d["options"][o.doc][0]
            if not concorde(nous, docv):
                out.append((f.nom, o.nom, docv, nous))
        oublis = set(d["options"]) - vus - IGNORES
        for cle in oublis:
            out.append((f.nom, cle, "dans le document, absent de nos données", None))
    return out


def test_ttc_conforme_aux_documents_sauf_corrections():
    for jeu in ("mixte", "français"):
        attendus = {(f, o): (d, n) for j, f, o, d, n in L.CORRECTIONS_TTC if j == jeu}
        trouves = {(f, o): (d, n) for f, o, d, n in ecarts(jeu, "TTC")}
        assert trouves == attendus, (jeu, {k: v for k, v in trouves.items() if attendus.get(k) != v},
                                     {k: v for k, v in attendus.items() if k not in trouves})


def test_ht_egal_ttc_divise_par_deux_sauf_erreurs_des_documents():
    for jeu in ("mixte", "français"):
        ttc = {(f, o) for j, f, o, d, n in L.CORRECTIONS_TTC if j == jeu}
        admis = {(f, o): d for j, f, o, d in L.CORRECTIONS_HT if j == jeu}
        for f, o, d, n in ecarts(jeu, "HT"):
            if (f, o) in ttc:
                continue  # le TTC a été corrigé : le HT du document suit l'ancien prix
            assert admis.get((f, o)) == d, (jeu, f, o, d, n)


def lignes_table(chemin):
    out = []
    for ligne in open(chemin, encoding="utf-8"):
        if " | " in ligne and not ligne.startswith(("P:", "===")):
            cellules = ligne.rstrip("\n").split(" | ")
            texte = re.sub(r"\d,\d{2} ?m\b|\d+ ?mm|100 ?%", " ", " ".join(cellules[:-1]), flags=re.I)
            out.append((norm(" ".join(cellules[:2])), [int(x) for x in re.findall(r"\b\d{3,4}\b", texte)],
                        [int(x) for x in re.findall(r"\d{3}", cellules[-1])]))
    return out


def test_plateaux_conformes():
    plateaux = {r[1]: r[2] for r in L.plateaux("mixte")}
    attendu = {  # ordre : les libellés les plus précis d'abord
        "VERRE ET BOIS": (None, None),
        "SIMPLE": ("Plateau simple, érable ou chêne, toutes teintes", ["2,30 m"]),
        "CHENE (OU|-) ERABLE": ("Plateau encastré, chêne ou érable", ["2,30 m", "2,40 m", "2,60 m", "2,80 m"]),
        "FINITION": ("Plateau encastré, finition parchemin, patine antiquaire, brossée ou cérusée",
                     ["2,30 m", "2,40 m", "2,60 m", "2,80 m"]),
        "LAQUE": ("Plateau encastré laqué", ["2,30 m", "2,40 m", "2,60 m", "2,80 m"]),
        "MELEZE": ("Plateau encastré mélèze", ["2,30 m", "2,40 m", "2,60 m", "2,80 m"]),
        "VERRE (EN )?2,10": ("Dessus 100 % verre", ["2,10 m", "2,30 m"]),
        "NOYER": ("Plateau encastré noyer plaqué", ["2,30 m"]),
        "3 PARTIES": ("Plateau en 3 parties", ["2,30 m"]),
    }
    for (jeu, sorte), fichier in SOURCES.items():
        conv = (lambda v: v) if sorte == "TTC" else L.ht
        trouves = set()
        for libelle, nombres, rallonge in lignes_table(DOCS / fichier):
            if rallonge and "PLATEAU-TABLE" not in libelle:
                assert rallonge == [conv(320), conv(470), conv(620)], (fichier, rallonge)
            for cle, (nom, tailles) in attendu.items():
                if re.search(rf"(^|\W)({cle})(\W|$)", libelle) and nombres:
                    if nom is None:
                        nous = [conv(plateaux[n]["2,30 m"]) for n in (
                            "Verre Sécurit 8 mm transparent et bois", "Verre Sécurit 8 mm dépoli et bois",
                            "Verre Sécurit 8 mm décor à carrés et bois", "Imitation céramique et bois (finition chêne)")]
                    else:
                        nous = [conv(plateaux[nom][t]) for t in tailles]
                    doc = nombres[:len(nous)]
                    erreurs_admises = {("pool_achat_ht.txt", "MELEZE"): [950, 1300, 1250, 1450],
                                       ("francais_vente_ttc.txt", "NOYER"): [2520],
                                       ("francais_achat_ht.txt", "NOYER"): [1260]}
                    if doc != nous:
                        assert erreurs_admises.get((fichier, cle)) == doc, (fichier, cle, doc, nous)
                    trouves.add(cle)
                    break
        assert trouves == set(attendu), (fichier, set(attendu) - trouves)


def test_accessoires_conformes():
    nous = sorted(p for _, art, _, p in L.accessoires() if "Harmonie" not in art or "standard" in art)
    for (jeu, sorte), fichier in SOURCES.items():
        conv = (lambda v: v) if sorte == "TTC" else L.ht
        texte = (DOCS / fichier).read_text(encoding="utf-8").replace("\xa0", " ")
        partie = texte[texte.index("Système de rangement"):texte.index("Hauteur des billards tables")]
        doc = sorted(n for n in euros(partie))
        assert doc == sorted(conv(p) for p in nous), (fichier, sorted(set(doc) ^ set(conv(p) for p in nous)))


def test_regles_et_structure():
    for jeu in ("mixte", "français"):
        fs = fiches(jeu)
        assert sum(len(f.modeles) for f in fs) == 19
        for f in fs:
            noms = {o.nom for o in f.options}
            for o in f.options:
                assert set(o.prix) == set(L.TAILLES[jeu]), (f.nom, o.nom)
                for ref in filter(None, (o.necessite + " ; " + o.exclut).split(" ; ")):
                    assert ref.strip() in noms or ref.strip() in (L.MELEZE, L.NOYER, L.CHENE), (f.nom, o.nom, ref)
                if o.nom == L.REPERES:
                    assert "Laque" in o.exclut
            assert (L.RETOUR in noms) == (jeu == "mixte" and f.nom in ("COMPÉTITION", "CHAMBORD")), f.nom
            assert (L.CADRE_SNOOKER in noms) == (jeu == "mixte" and f.nom in ("ARCADE", "MONT BLANC", "COMPÉTITION",
                                                                               "CHAMBORD")), f.nom
            assert (L.A37 in noms) == (jeu == "français"), f.nom
            assert (L.JEU2 in noms) == (jeu == "mixte"), f.nom
            if f.nom.startswith("HARMONIE"):
                for o in f.options:
                    if o.nom in (L.LAQUE, L.TEINTE_SPECIALE, L.BICOLORE):
                        assert set(o.prix.values()) <= {L.IMP, L.NP}, o.nom
                assert L.LISERE not in noms
            if f.base.startswith("Érable sycomore"):
                for o in f.options:
                    if o.nom in (L.PARCHEMIN, L.BROSSEE):
                        assert L.CHENE in o.necessite
            for o in f.options:
                if o.groupe == "Essence" and o.nom != "Cadre en mélèze massif":
                    assert "Laque" in o.exclut, (f.nom, o.nom)
    textes = repr([vars(o) for j in ("mixte", "français") for f in fiches(j) for o in f.options]) + repr(L.plateaux("mixte"))
    for interdit in ("défonc", "Descente", "descente", "Dauphinois", "hauteur", "Hauteur"):
        assert interdit not in textes, interdit


def test_prix_pivots():
    m = {f.nom: f for f in L.fiches_mixte()}
    fr = {f.nom: f for f in L.fiches_francais()}
    assert m["CHAMBORD"].modeles["Chambord"]["12 pieds"] == 24000
    assert fr["LOFT · ÉLÉGANCE"].modeles["Élégance"]["2,30 m"] == 6230 and L.ht(6230) == 3115
    assert fr["BEAUBOURG"].modeles["Beaubourg"]["2,30 m"] == 6670
    arcade6 = next(o for o in m["ARCADE"].options if o.nom == L.SIX_PIEDS)
    assert arcade6.prix["2,80 m"] == 1370
    a37 = next(o for o in fr["CHAMBORD"].options if o.nom == L.A37)
    assert a37.prix["2,40 m"] == 750 and a37.prix["2,60 m"] == L.INC


def test_fiches_techniques():
    for jeu in ("mixte", "français"):
        for f in fiches(jeu):
            for el in f.technique:
                assert "Érable ou chêne" not in el[1] and "chêne ou noyer" not in el[1], (f.nom, el)
            essences = {o.nom.replace("Cadre en ", "") for o in f.options if o.groupe == "Essence"
                        and set(o.prix.values()) - {L.NP, L.IMP}}
            for el in f.technique:
                texte = L.option_bois(f, el) or ""
                if el[3] == "Bois massif de l'essence choisie":
                    for e in essences:
                        assert e.lower().replace(" massif", "") in texte.lower(), (f.nom, el[0], e, texte)
    loft = next(f for f in L.fiches_mixte() if f.nom == "LOFT · ÉLÉGANCE")
    cadre = next(e for e in loft.technique if e[0] == "Cadre")
    assert cadre[1] == "Érable sycomore massif"
    assert L.option_bois(loft, cadre) == "Chêne massif ou mélèze massif ; noyer sur demande"
    soho = next(f for f in L.fiches_mixte() if f.nom == "SOHO")
    assert L.option_bois(soho, next(e for e in soho.technique if e[0] == "Cadre")) == "Chêne massif ou mélèze massif"
    bandes = [o for o in loft.options if o.groupe == L.BANDES_INIT]
    assert len(bandes) == 3 and all(o.choix == "Un seul par groupe" for o in bandes)
    assert L.DRAP["français"] == "Simonis 330 inclus"


if __name__ == "__main__":
    for nom, f in list(globals().items()):
        if nom.startswith("test_"):
            f()
            print("ok", nom)
