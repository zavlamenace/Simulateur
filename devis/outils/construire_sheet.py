"""Génère le classeur « BdF – Tarifs & contenus » (.xlsx importable dans Google Sheets).

Usage : python3 -I construire_sheet.py <dossier devis/donnees> <sortie.xlsx> [<revendeurs-ht.xlsx>]

Organisation lue par l'outil de devis :
- chaque onglet de gamme contient des blocs dont la première cellule commence
  par « ■ » (GAMME, MODÈLES, OPTIONS, ARGUMENTS & PHOTOS) ;
- la ligne sous le titre du bloc porte les en-têtes ; l'outil lit les colonnes
  par leur nom, jamais par leur position ;
- un bloc s'arrête au titre « ■ » suivant ou à la fin de la feuille ;
- aucune formule : insérer des lignes ou des colonnes ne casse rien.
"""
import json
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arguments_brouillons  # noqa: E402
import lafuge_tarifs as lt  # noqa: E402
import grilles_papier as gp  # noqa: E402

ENCRE, ROUGE, CREME, SABLE_CLAIR, SABLE, ANTHRACITE = "151515", "B01C2E", "F6F3EE", "EFE9E3", "D9CFBF", "3D4248"
TITRE = Font(name="EB Garamond", size=20, bold=True, color=ENCRE)
SOUS_TITRE = Font(name="DM Sans", size=10, italic=True, color=ANTHRACITE)
BLOC = Font(name="DM Sans", size=11, bold=True, color="FFFFFF")
ENTETE = Font(name="DM Sans", size=10, bold=True, color=ENCRE)
TEXTE = Font(name="DM Sans", size=10, color=ENCRE)
NOTE = Font(name="DM Sans", size=9, italic=True, color=ANTHRACITE)
FOND_BLOC = PatternFill("solid", fgColor=ENCRE)
FOND_ENTETE = PatternFill("solid", fgColor=SABLE_CLAIR)
FOND_VIDE = PatternFill("solid", fgColor=CREME)
FILET = Side(style="thin", color=SABLE)
CADRE = Border(left=FILET, right=FILET, top=FILET, bottom=FILET)
EURO = '#,##0" €"'
POURCENT = "0%"

STATUTS = '"Actif,Bientôt,Masqué"'
STATUTS_ARG = '"Actif,À valider,Masqué"'
CHOIX = '"Un seul par groupe,Plusieurs possibles"'
OUI_NON = '"Oui,Non"'


class Feuille:
    """Écrit des blocs empilés et mémorise les plages pour la mise en forme."""

    def __init__(self, wb, nom, titre, consigne, largeurs, onglet=None):
        self.ws = wb.create_sheet(nom)
        self.ws.sheet_view.showGridLines = False
        if onglet:
            self.ws.sheet_properties.tabColor = onglet
        for i, w in enumerate(largeurs, start=1):
            self.ws.column_dimensions[get_column_letter(i)].width = w
        self.ncol = len(largeurs)
        self.ws["A1"] = titre
        self.ws["A1"].font = TITRE
        self.ws.row_dimensions[1].height = 34
        self.ws["A2"] = consigne
        self.ws["A2"].font = SOUS_TITRE
        self.ws.freeze_panes = "A3"
        self.ws.page_setup.orientation = "landscape"
        self.ws.page_setup.fitToWidth = 1
        self.ws.page_setup.fitToHeight = 0
        self.ws.sheet_properties.pageSetUpPr.fitToPage = True
        self.ligne = 4

    def bloc(self, titre, entetes, lignes, vides=0, formats=None, validations=None, note=None):
        ws, r0 = self.ws, self.ligne
        ws.cell(r0, 1, f"■ {titre}").font = BLOC
        for c in range(1, max(len(entetes), 1) + 1):
            ws.cell(r0, c).fill = FOND_BLOC
        if note:
            ws.cell(r0, len(entetes) + 1, note).font = NOTE
        ws.row_dimensions[r0].height = 22
        for c, h in enumerate(entetes, start=1):
            cell = ws.cell(r0 + 1, c, h)
            cell.font, cell.fill, cell.border = ENTETE, FOND_ENTETE, CADRE
            cell.alignment = Alignment(wrap_text=True, vertical="center")
        ws.row_dimensions[r0 + 1].height = 30
        premiere = r0 + 2
        for i, valeurs in enumerate(lignes + [[None] * len(entetes)] * vides):
            r = premiere + i
            for c in range(1, len(entetes) + 1):
                v = valeurs[c - 1] if c - 1 < len(valeurs) else None
                cell = ws.cell(r, c, v)
                cell.font, cell.border = TEXTE, CADRE
                lien = entetes[c - 1].startswith("Photo")
                cell.alignment = Alignment(wrap_text=not lien, vertical="top")
                if lien and isinstance(v, str) and v.startswith("http"):
                    cell.hyperlink = v.split("\n")[0]
                    cell.font = Font(name="DM Sans", size=10, color="0069A8", underline="single")
                if i >= len(lignes):
                    cell.fill = FOND_VIDE
        derniere = premiere + len(lignes) + vides - 1
        for col, fmt in (formats or {}).items():
            c = entetes.index(col) + 1
            for r in range(premiere, derniere + 1):
                ws.cell(r, c).number_format = fmt
        for col, formule in (validations or {}).items():
            c = entetes.index(col) + 1
            lettre = get_column_letter(c)
            dv = DataValidation(type="list", formula1=formule, allow_blank=True)
            dv.showErrorMessage = not formule.startswith("=")
            ws.add_data_validation(dv)
            dv.add(f"{lettre}{premiere}:{lettre}{derniere}")
        if "Statut" in entetes:
            s = get_column_letter(entetes.index("Statut") + 1)
            plage = f"A{premiere}:{get_column_letter(len(entetes))}{derniere}"
            ws.conditional_formatting.add(
                plage, FormulaRule(formula=[f'${s}{premiere}="Masqué"'], font=Font(color="9A9D9F", strike=True))
            )
            ws.conditional_formatting.add(
                plage, FormulaRule(formula=[f'${s}{premiere}="Bientôt"'], font=Font(color="B07E1E", italic=True))
            )
        self.ligne = derniere + 3
        return premiere, derniere


def bloc_gamme(f, params):
    premiere, _ = f.bloc("GAMME", ["Paramètre", "Valeur", "Explication"], params)
    for i, (nom, *_r) in enumerate(params):
        cell = f.ws.cell(premiere + i, 2)
        cell.alignment = Alignment(wrap_text=True, vertical="top", horizontal="left")
        if nom == "Valeur du kit accessoires":
            cell.number_format = EURO
        if nom in ("Kit accessoires inclus", "Marque", "Statut"):
            choix = {"Kit accessoires inclus": OUI_NON, "Marque": '"Billard Plaisance,Billard Lafuge"',
                     "Statut": '"Actif,Masqué"'}[nom]
            dv = DataValidation(type="list", formula1=choix, allow_blank=True)
            f.ws.add_data_validation(dv)
            dv.add(cell.coordinate)


ENTETES_MODELES = [
    "Modèle", "Version", "Finition", "Prix TTC", "Statut", "Photo détourée",
    "Photo avec plateau bois", "Photo avec plateau verre", "Photos de détail", "Note interne",
]
ENTETES_OPTIONS = [
    "Groupe", "Option", "Détail imprimé sur le devis", "Prix TTC", "Valeur si offert", "Statut",
    "Valable pour", "Nécessite", "Exclut", "Choix", "Note interne",
]
ENTETES_ARGS = ["Ordre", "Valable pour", "Titre", "Texte", "Photo", "Statut", "Proposé par défaut"]
LARGEURS_GAMME = [30, 30, 46, 12, 12, 16, 22, 26, 26, 24, 34]


def bloc_options(f, lignes, vides=12):
    p, d = f.ligne + 2, f.ligne + 2 + len(lignes) + vides - 1
    noms = f"=$B${p}:$B${d}"
    f.bloc(
        "OPTIONS", ENTETES_OPTIONS, lignes, vides,
        formats={"Prix TTC": EURO, "Valeur si offert": EURO},
        validations={"Statut": STATUTS, "Choix": CHOIX, "Nécessite": noms, "Exclut": noms},
        note="Prix vide = sur devis. « Nécessite » / « Exclut » : nom exact d'une option ou d'un groupe.",
    )


def bloc_arguments(f, lignes, vides=6):
    f.bloc(
        "ARGUMENTS & PHOTOS", ENTETES_ARGS, lignes, vides,
        validations={"Statut": STATUTS_ARG, "Proposé par défaut": OUI_NON},
        note="Dans l'outil, on coche 4 arguments au maximum par devis ; « Proposé par défaut = Oui » les pré-coche. "
             "Valable pour : « Tous » ou une version (ex. « Pieds métalliques »). Photo : lien vers la photo ultra zoomée "
             "(« À fournir » = photo attendue).",
    )


def jeux_de_bandes():
    inclus = [
        ["Jeu de bandes inclus", f"Jeu de bandes {j}", f"Bandes {j}es calibrées, système breveté", 0, None,
         "Actif", "Tous", None, None, "Un seul par groupe", None]
        for j in ("français", "américain", "pool")
    ]
    inclus[0][2] = "Bandes françaises calibrées (billes Ø 61 mm), système breveté"
    inclus[1][2] = "Bandes américaines calibrées (billes Ø 57 mm), système breveté"
    inclus[2][2] = "Bandes pool calibrées (billes Ø 50,8 mm), système breveté"
    second = [
        ["2e jeu de bandes", "2e jeu de bandes américain", "Second jeu de bandes interchangeables : américain",
         700, None, "Actif", "Tous", None, "Jeu de bandes américain", "Plusieurs possibles", None],
        ["2e jeu de bandes", "2e jeu de bandes pool", "Second jeu de bandes interchangeables : pool",
         700, None, "Actif", "Tous", None, "Jeu de bandes pool", "Plusieurs possibles", None],
        ["2e jeu de bandes", "2e jeu de bandes français", "Second jeu de bandes interchangeables : français",
         700, None, "Actif", "Tous", None, "Jeu de bandes français", "Plusieurs possibles", None],
    ]
    return inclus + second


def tapis_inclus():
    return [
        ["Tapis", "Tapis Simonis 760 (26 teintes)", "Drap Simonis 760, référence mondiale des compétitions", 0,
         None, "Actif", "Tous", None, None, "Un seul par groupe", "Teinte choisie dans l'onglet Coloris"],
        ["Tapis", "Tapis Strachan 777 (7 teintes)", "Drap Strachan 777, référence du pool anglais", 0,
         None, "Actif", "Tous", None, None, "Un seul par groupe", "Teinte choisie dans l'onglet Coloris"],
    ]


def onglet_reference(wb, ref):
    f = Feuille(
        wb, "Référence", "Référence Premium · Billard Plaisance",
        "Cellules blanches : modifiables. Lignes crème : vides, prêtes pour un nouvel élément. "
        "Ne renommez pas les titres ■ ni les en-têtes.", LARGEURS_GAMME, onglet="3D4248",
    )
    bloc_gamme(f, [
        ["Nom affiché", "Référence Premium", "Nom de la gamme sur le devis"],
        ["Marque", "Billard Plaisance", "Billard Plaisance ou Billard Lafuge (logo et échéancier)"],
        ["Accroche", "Le meilleur rapport qualité-prix", "Une phrase sous le nom de la gamme"],
        ["Délai de fabrication", "2 à 3 semaines", "Hors organisation de la livraison"],
        ["Atelier affiché sur le devis", None, "Laisser vide pour la Référence : aucune mention d'origine"],
        ["Kit accessoires inclus", "Oui", "Oui : le bloc « Kit accessoires offert » s'affiche"],
        ["Valeur du kit accessoires", 330, "Valeur affichée à côté de « offert »"],
        ["Contenu du kit accessoires",
         "16 billes (US Ø 57 mm ou Pool Ø 50,8 mm), 1 boîte de craies, 4 queues de 120 cm, 1 triangle, 1 brosse, 1 porte-queue",
         "Imprimé tel quel"],
        ["Statut", "Actif", "Masqué : la gamme disparaît de l'outil"],
    ])
    modeles = [
        [m["modele"], m["version"], m["finition"], m["prix_ttc"],
         "Masqué" if m["modele"] == "Panama" else "Actif", m["photo_detouree"],
         m["photo_plateau_bois"], m["photo_plateau_verre"], "\n".join(m["photos_detail"]),
         "Bonne affaire, hors catalogue" if m["modele"] == "Panama" else None]
        for m in ref["modeles"]
    ]
    f.bloc("MODÈLES", ENTETES_MODELES, modeles, vides=8, formats={"Prix TTC": EURO},
           validations={"Statut": STATUTS, "Version": '"Pieds bois massif,Pieds métalliques"'},
           note="Photos : liens issus du site (détourées sur fond blanc).")
    opts = [
        ["Tapis", "Tapis standard (4 teintes)", "Drap rapide de très bonne qualité", 0, None, "Actif", "Tous",
         None, None, "Un seul par groupe", "Gris clair, Bleu royal, Rouge, Vert (onglet Coloris)"],
        ["Tapis", "Tapis Simonis 760 (26 teintes)", "Drap Simonis 760, référence mondiale des compétitions", 620,
         None, "Actif", "Tous", None, None, "Un seul par groupe", None],
        ["Tapis", "Tapis Strachan 777 (7 teintes)", "Drap Strachan 777, référence du pool anglais", 620, None,
         "Actif", "Tous", None, None, "Un seul par groupe", None],
        ["Jeu", "Billard américain", "Bandes américaines, billes Ø 57 mm", 0, None, "Actif", "Tous", None, None,
         "Un seul par groupe", None],
        ["Jeu", "Pool anglais", "Bandes pool, billes Ø 50,8 mm", 0, None, "Actif", "Tous", None, None,
         "Un seul par groupe", None],
        ["Billard français", "6 plugs pour jouer au billard français", "Ajout de 6 plugs aux bandes", 640, None,
         "Actif", "Tous", None, None, "Plusieurs possibles", None],
        ["Dessus de table", "Plateau 100 % bois en 2 parties", "Transforme le billard en table à manger", 330,
         None, "Actif", "Tous", None, None, "Un seul par groupe", None],
        ["Dessus de table", "Plateau 100 % verre Sécurit en 2 parties", "Verre de sécurité, en 2 parties", 1100,
         None, "Actif", "Tous", None, None, "Un seul par groupe", None],
        ["Couleur des pieds", "Pieds noirs", "Pieds métalliques laqués époxy, noir", 0, None, "Actif",
         "Pieds métalliques", None, None, "Un seul par groupe", None],
        ["Couleur des pieds", "Pieds blancs", "Pieds métalliques laqués époxy, blanc", 0, None, "Actif",
         "Pieds métalliques", None, None, "Un seul par groupe", None],
        ["Couleur des pieds", "Pieds gris anthracite", "Pieds métalliques laqués époxy, gris anthracite", 0, None,
         "Actif", "Pieds métalliques", None, None, "Un seul par groupe", None],
        ["Couleur des pieds", "Pieds couleur RAL au choix", "Pieds métalliques dans la couleur RAL de votre choix",
         0, None, "Actif", "Pieds métalliques", None, None, "Un seul par groupe",
         "Sans supplément : l'écart bois → métal (400 €) est déjà dans le prix du modèle pieds métalliques"],
        ["Rangement", "Rangement Octopack", "Rangement intégré des accessoires", None, None, "Masqué", "Tous", None,
         None, "Plusieurs possibles", "Pas possible sur la Référence"],
        ["Rangement", "Rangement des accessoires", "Queues, billes, boîte de craies et brosse rangées sous le billard",
         400, None, "Actif", "Tous", None, None, "Plusieurs possibles", None],
    ]
    bloc_options(f, opts)
    bloc_arguments(f, arguments_brouillons.lignes("Référence"))


def onglet_design(wb, dp):
    f = Feuille(
        wb, "Design", "Design · Billard Plaisance",
        "Cellules blanches : modifiables. Lignes crème : vides, prêtes pour un nouvel élément. "
        "Ne renommez pas les titres ■ ni les en-têtes.", LARGEURS_GAMME, onglet="B01C2E",
    )
    bloc_gamme(f, [
        ["Nom affiché", "Design", None],
        ["Marque", "Billard Plaisance", None],
        ["Accroche", "Le meilleur rapport qualité-prix en fabrication française, en laqué", None],
        ["Délai de fabrication", "4 à 6 semaines", "Hors organisation de la livraison"],
        ["Atelier affiché sur le devis", "Fabriqué dans nos ateliers de Plaisance-du-Gers", None],
        ["Kit accessoires inclus", "Non", None],
        ["Valeur du kit accessoires", None, None],
        ["Contenu du kit accessoires", None, None],
        ["Statut", "Actif", None],
    ])
    modeles = [
        [p["nom"].replace("Billard ", ""), gp.DESIGN_PIETEMENT, gp.DESIGN[p["nom"].replace("Billard ", "")],
         p["prix_ttc_site"], "Actif", next((g["full"] for g in p["galerie"] if g.get("detouree")), ""), None, None, None,
         gp.NOTE_VERIFIE]
        for p in dp if "/billard-design/" in p["url"]
    ]
    f.bloc("MODÈLES", ENTETES_MODELES, modeles, vides=8, formats={"Prix TTC": EURO},
           validations={"Statut": STATUTS})
    opts = tapis_inclus() + jeux_de_bandes() + [
        ["Finition", "Couleur RAL au choix", "Laque dans la couleur RAL de votre choix", 250, None, "Actif", "Tous",
         None, None, "Plusieurs possibles", None],
        ["Finition", "Vernis grand brillant et polissage du billard", "Vernis grand brillant, poli à la main", 540,
         None, "Actif", "Tous", None, None, "Plusieurs possibles", None],
        ["Finition", "Vernis grand brillant et polissage du dessus de table",
         "Plateau en vernis grand brillant, poli à la main", 270, None, "Actif", "Tous", "Plateau table bois laqué",
         None, "Plusieurs possibles", None],
        ["Rangement", "Rangement des accessoires", "Queues, billes, boîte de craies et brosse rangées sous le billard",
         400, None, "Actif", "Tous", None, None, "Plusieurs possibles", "Photo de réassurance à venir"],
        ["Allonge", "Allonge de plateau 45 cm", "Agrandit la table à manger de 45 cm", 500, None, "Actif", "Tous",
         "Plateau table bois laqué", None, "Plusieurs possibles",
         "Une seule finition laquée. Déjà incluse avec le plateau vitré"],
        ["Plateau table", "Plateau table bois laqué", "Plateau en 2 parties, laqué dans la finition du billard", 990,
         None, "Actif", "Tous", None, None, "Un seul par groupe", None],
        ["Plateau table", "Plateau 100 % verre Sécurit 8 mm", "Verre Sécurit 8 mm, motif décor à carré, en 2 parties",
         1100, None, "Actif", "Tous", None, None, "Un seul par groupe", "Sans allonge"],
        ["Plateau table", "Plateau vitré cadre bois", "Cadre bois et verre Sécurit 6 mm, en 2 parties, allonge 45 cm incluse",
         1600, None, "Actif", "Tous", None, None, "Un seul par groupe", "Allonge incluse"],
    ]
    bloc_options(f, opts)
    bloc_arguments(f, arguments_brouillons.lignes("Design"))


def onglet_prestige(wb, dp):
    f = Feuille(
        wb, "Prestige", "Prestige · Billard Plaisance",
        "Cellules blanches : modifiables. Lignes crème : vides, prêtes pour un nouvel élément. "
        "Ne renommez pas les titres ■ ni les en-têtes.", LARGEURS_GAMME, onglet="7A5A3A",
    )
    bloc_gamme(f, [
        ["Nom affiché", "Prestige", None],
        ["Marque", "Billard Plaisance", None],
        ["Accroche", "Le billard convertible le plus abouti, en bois massif", None],
        ["Délai de fabrication", "4 à 6 semaines", "Hors organisation de la livraison"],
        ["Atelier affiché sur le devis", "Fabriqué dans nos ateliers de Plaisance-du-Gers", None],
        ["Kit accessoires inclus", "Non", None],
        ["Valeur du kit accessoires", None, None],
        ["Contenu du kit accessoires", None, None],
        ["Statut", "Actif", None],
    ])
    modeles = [
        [p["nom"].replace("Billard ", ""), gp.PRESTIGE[p["nom"].replace("Billard ", "")][0],
         gp.PRESTIGE[p["nom"].replace("Billard ", "")][1], gp.PRESTIGE_PRIX[p["nom"].replace("Billard ", "")],
         "Actif", next((g["full"] for g in p["galerie"] if g.get("detouree")), ""), None, None,
         None, gp.NOTE_VERIFIE]
        for p in dp if "/billard-prestige-/" in p["url"]
    ]
    f.bloc("MODÈLES", ENTETES_MODELES, modeles, vides=8, formats={"Prix TTC": EURO},
           validations={"Statut": STATUTS})
    opts = tapis_inclus() + jeux_de_bandes() + [
        ["Plateau table", "Plateau table bois", "Plateau bois en 2 parties, dans la teinte du billard, allonge 45 cm incluse",
         990, None, "Actif", "Tous", None, None, "Un seul par groupe", "Allonge incluse"],
        ["Plateau table", "Plateau 100 % verre Sécurit 8 mm", "Verre Sécurit 8 mm, motif décor à carré, en 2 parties",
         1200, None, "Actif", "Tous", None, None, "Un seul par groupe", "Sans allonge"],
        ["Plateau table", "Plateau verre et cadre couleur de rappel",
         "Cadre bois dans la couleur du billard et verre Sécurit 6 mm, en 2 parties, allonge 45 cm incluse",
         1600, None, "Actif", "Tous", None, None, "Un seul par groupe", "Allonge incluse"],
        ["Décor", "Motif décor à carré", "4 carrés peints sur le plateau bois (ex. marron foncé, aluminium)", 300,
         None, "Actif", "Tous", "Plateau table bois", None, "Plusieurs possibles",
         "Ex. dessus Athènes : 4 carrés marron foncé ; dessus Helsinki : 4 carrés aluminium"],
        ["Pieds", "Pieds métalliques", "Pieds métalliques à la place des pieds en bois massif", None, None,
         "Bientôt", "Tous", None, None, "Un seul par groupe", "Disponible dans environ 3 mois, prix à définir"],
    ]
    bloc_options(f, opts)
    bloc_arguments(f, arguments_brouillons.lignes("Prestige"))


GRIS_IMPOSSIBLE, AMBRE = "9A9D9F", "F6E7C8"
CONVENTION = ("Case vide = pas encore chiffrée ; « — » = taille non proposée pour ce modèle ; « Sur demande » = prix "
              "saisi à la main dans l'outil ; « Impossible » ; « Inclus ».")


def styliser_prix(f, premiere, derniere, c0, c1, col_libelle):
    """Lecture rapide : « Impossible » et « — » en gris, « Sur demande » en italique, case à chiffrer en ambre."""
    plage = f"{get_column_letter(c0)}{premiere}:{get_column_letter(c1)}{derniere}"
    haut = f"{get_column_letter(c0)}{premiere}"
    lib = f"${get_column_letter(col_libelle)}{premiere}"
    f.ws.conditional_formatting.add(plage, FormulaRule(formula=[f'OR({haut}="Impossible",{haut}="—")'],
                                                       font=Font(color=GRIS_IMPOSSIBLE)))
    f.ws.conditional_formatting.add(plage, FormulaRule(formula=[f'{haut}="Sur demande"'],
                                                       font=Font(color=ANTHRACITE, italic=True)))
    f.ws.conditional_formatting.add(plage, FormulaRule(formula=[f'AND({lib}<>"",ISBLANK({haut}))'],
                                                       fill=PatternFill("solid", fgColor=AMBRE)))
    for r in range(premiere, derniere + 1):
        for c in range(c0, c1 + 1):
            f.ws.cell(r, c).alignment = Alignment(horizontal="right", vertical="top")


def onglets_lafuge(wb, ht=False):
    """Onglets « Lafuge mixte » et « Lafuge bandes françaises » (TTC) ou leurs équivalents HT revendeur.

    Les colonnes de prix sont au même endroit dans tous les blocs (D et suivantes) pour une lecture verticale.
    """
    conv = lt.ht if ht else (lambda v: v)
    for jeu, nom, titre in (("mixte", "Lafuge mixte", "Billard Lafuge · mixte"),
                            ("français", "Lafuge bandes françaises", "Billard Lafuge · bandes françaises")):
        tailles = lt.TAILLES[jeu]
        prix = [f"Prix {t}" for t in tailles]
        n = len(tailles)
        formats = {c: EURO for c in prix}
        consigne = (("CONFIDENTIEL : prix d'achat revendeur HT départ, à ne jamais transmettre à un client. "
                     if ht else "Prix de vente TTC public, par taille. ") + CONVENTION
                    + " Ne renommez pas les titres ■ ni les en-têtes.")
        f = Feuille(wb, nom + (" HT" if ht else ""), titre + (" — prix revendeur HT" if ht else ""), consigne,
                    [16, 46, 24] + [11] * n + [36, 30, 40, 18, 11, 46, 34], onglet="1E4F4A")
        f.ws.freeze_panes = "C3"
        fiches = lt.fiches_mixte() if jeu == "mixte" else lt.fiches_francais()
        if not ht:
            bloc_gamme(f, [
                ["Nom affiché", "Billard Lafuge", None],
                ["Marque", "Billard Lafuge", "Logo Lafuge, échéancier en 3 versements"],
                ["Jeu", "Billard mixte : pool, américain, anglais, snooker, russe" if jeu == "mixte"
                 else "Billard français à bandes fixes", None],
                ["Accroche", "Une pièce unique, fabriquée à la main par un seul ébéniste", None],
                ["Délai de fabrication", lt.GAMME["Délai de fabrication"], None],
                ["Atelier affiché sur le devis", "Fabriqué à la main dans notre atelier de Miribel-les-Échelles", None],
                ["Drap", lt.DRAP[jeu], None],
                ["Mention accessoires", lt.GAMME["Accessoires"], "Imprimée sur le devis"],
                ["Échéancier", lt.GAMME["Échéancier"], None],
                ["Kit accessoires inclus", "Non", None],
                ["Statut", "Actif", None],
            ])
        colonne_ardoise = 2 if jeu == "mixte" else 3
        f.bloc("TAILLES", ["Taille", "Dimensions hors tout (m)", "Surface de jeu (m)", "Ardoise italienne", "Statut"],
               [[t, *lt.DIMENSIONS[t][:2], lt.DIMENSIONS[t][colonne_ardoise], "Actif"] for t in tailles],
               validations={"Statut": STATUTS})
        lignes = [[m, fiche.nom, fiche.base, *[conv(v[t]) for t in tailles], "Oui" if fiche.table else "Non",
                   "Actif", None, None] for fiche in fiches for m, v in fiche.modeles.items()]
        p0, d0 = f.bloc("MODÈLES", ["Modèle", "Fiche", "Matière de base", *prix, "Version table", "Statut",
                                    "Photo détourée", "Note interne"], lignes, vides=4, formats=formats,
                        validations={"Statut": STATUTS, "Version table": OUI_NON},
                        note="Recherche rapide du prix d'un billard ; ses options sont dans le bloc de sa fiche, plus bas.")
        styliser_prix(f, p0, d0, 4, 3 + n, 1)
        entetes = ["Groupe", "Option", "Valable pour", *prix, "Conditions", "Nécessite", "Exclut", "Choix", "Statut",
                   "Détail imprimé sur le devis", "Note interne"]
        for fiche in fiches:
            lignes = [["Billard", m, m, *[conv(v[t]) for t in tailles], fiche.base, None, None, "Un seul par groupe",
                       "Actif", None, None] for m, v in fiche.modeles.items()]
            lignes += [[o.groupe, o.nom, o.valable_pour, *[conv(o.prix[t]) for t in tailles], o.conditions or None,
                        o.necessite or None, o.exclut or None, o.choix, "Actif", o.detail or None, o.note or None]
                       for o in fiche.options]
            p0, d0 = f.bloc(fiche.nom, entetes, lignes, vides=2, formats=formats,
                            validations={"Statut": STATUTS, "Choix": CHOIX})
            styliser_prix(f, p0, d0, 4, 3 + n, 2)
            for r in range(p0, p0 + len(fiche.modeles)):
                for c in range(1, len(entetes) + 1):
                    f.ws.cell(r, c).font = Font(name="DM Sans", size=10, bold=True, color=ENCRE)
        lignes = [[g, nom_p, "Tous", *[conv(v[t]) for t in tailles], cond, nec or None, None, choix, "Actif",
                   det or None, None] for g, nom_p, v, cond, det, nec, choix in lt.plateaux(jeu)]
        p0, d0 = f.bloc("PLATEAUX", entetes, lignes, vides=4, formats=formats,
                        validations={"Statut": STATUTS, "Choix": CHOIX},
                        note="Plateau au choix, indépendant de la finition du billard. Pas de plateau sur Compétition et Chambord.")
        styliser_prix(f, p0, d0, 4, 3 + n, 2)


def onglet_lafuge_contenus(wb):
    """Textes Lafuge : fiches techniques (imprimées sur le devis selon les options) et arguments, par jeu."""
    f = Feuille(wb, "Lafuge contenus", "Billard Lafuge · fiches techniques et arguments",
                "Fiche technique : la version imprimée suit les options (laque, bois massif). "
                "Ne renommez pas les titres ■ ni les en-têtes.", [10, 24, 16, 52, 44, 30, 14], onglet="1E4F4A")
    for jeu, suffixe in (("mixte", "MIXTE"), ("français", "BANDES FRANÇAISES")):
        fiches = lt.fiches_mixte() if jeu == "mixte" else lt.fiches_francais()
        lignes = [[i, fiche.nom, el[0], el[1], lt.option_bois(fiche, el), el[2] or None]
                  for i, (fiche, el) in enumerate(((fi, e) for fi in fiches for e in fi.technique), start=1)]
        f.bloc(f"FICHES TECHNIQUES · {suffixe}", ["Ordre", "Fiche", "Élément", "De base", "En option",
                                                   "Version laquée"], lignes, vides=4,
               note="De base : la matière indiquée sous le titre de la fiche. En option (bois massif) : cadre, pieds, "
                    "traverses et châssis passent en bois massif ; le métal (châssis acier, pieds acier) reste.")
        bloc_arguments_lafuge(f, suffixe, arguments_brouillons.lignes("Lafuge" if jeu == "mixte" else "Lafuge français"))


def bloc_arguments_lafuge(f, suffixe, lignes, vides=4):
    f.bloc(
        f"ARGUMENTS & PHOTOS · {suffixe}", ENTETES_ARGS, lignes, vides,
        validations={"Statut": STATUTS_ARG, "Proposé par défaut": OUI_NON},
        note="On coche 4 arguments au maximum par devis ; « Proposé par défaut = Oui » les pré-coche.",
    )


def classeur_revendeurs(sortie):
    """Classeur séparé et confidentiel des prix revendeur HT (Lafuge). Jamais lu par l'outil de devis."""
    wb = Workbook()
    wb.remove(wb.active)
    onglets_lafuge(wb, ht=True)
    f = Feuille(wb, "Accessoires Lafuge HT", "Accessoires Lafuge — prix revendeur HT",
                "CONFIDENTIEL : prix d'achat revendeur HT départ, à ne jamais transmettre à un client.",
                [26, 56, 44, 12, 12, 30], onglet="1E4F4A")
    f.bloc("ACCESSOIRES", ["Catégorie", "Article", "Détail", "Prix HT", "Statut", "Note interne"],
           [[c, a, d, lt.ht(p), "Actif", None] for c, a, d, p in lt.accessoires()], vides=6,
           formats={"Prix HT": EURO}, validations={"Statut": STATUTS})
    wb.active = 0
    wb.save(sortie)
    return wb.sheetnames


COLORIS = [
    ("Standard", "Gris clair", "A7ADB0"), ("Standard", "Bleu royal", "1F4E9C"), ("Standard", "Rouge", "B3202A"),
    ("Standard", "Vert", "2E7D3A"),
    ("Simonis 760", "Vert jaune", "7A9A1E"), ("Simonis 760", "Vert bleu", "0F7D6E"),
    ("Simonis 760", "Vert anglais", "1F5A3A"), ("Simonis 760", "Vert olive", "6B6B2A"),
    ("Simonis 760", "Vert pomme", "5BA33B"), ("Simonis 760", "Spruce", "1E4F4A"),
    ("Simonis 760", "Vert foncé", "1B4A2E"), ("Simonis 760", "Bleu pétrole", "1D5B6B"),
    ("Simonis 760", "Bleu royal", "224C9C"), ("Simonis 760", "Bleu marine", "1F2B4A"),
    ("Simonis 760", "Bleu tournoi", "1E6BB0"), ("Simonis 760", "Bleu électrique", "1F7DD1"),
    ("Simonis 760", "Bleu poudré", "7FA7C9"), ("Simonis 760", "Chocolat", "4A2E22"),
    ("Simonis 760", "Rouge", "B3202A"), ("Simonis 760", "Bordeaux (burgundy)", "6E1A2A"),
    ("Simonis 760", "Rouge vin", "7A1E33"), ("Simonis 760", "Fuchsia", "B0236E"),
    ("Simonis 760", "Violet", "5B2C7A"), ("Simonis 760", "Orange", "D9661F"),
    ("Simonis 760", "Camel", "B48A57"), ("Simonis 760", "Or", "C9A227"),
    ("Simonis 760", "Gris", "7D8285"), ("Simonis 760", "Gris requin", "5E6468"),
    ("Simonis 760", "Gris ardoise", "4A5157"), ("Simonis 760", "Noir", "1A1A1A"),
]
COLORIS += [("Strachan 777", t, gp.STRACHAN_HEX[t]) for t in gp.STRACHAN]


def onglet_coloris(wb):
    f = Feuille(wb, "Coloris", "Coloris des tapis",
                "Le code couleur sert à la pastille du devis (aperçu indicatif, à ajuster si besoin).",
                [16, 24, 14, 10, 12, 40], onglet="2E7D3A")
    p, d = f.bloc(
        "COLORIS", ["Drap", "Teinte", "Code couleur", "Aperçu", "Statut", "Note interne"],
        [[dr, t, f"#{h}", None, "Actif", None] for dr, t, h in COLORIS], vides=10,
        validations={"Drap": '"Standard,Simonis 760,Strachan 777"', "Statut": STATUTS},
        note="Standard = 4 teintes incluses sur la Référence uniquement.",
    )
    for i, (_, _, h) in enumerate(COLORIS):
        f.ws.cell(p + i, 4).fill = PatternFill("solid", fgColor=h)


def onglet_accessoires(wb):
    f = Feuille(wb, "Accessoires & mobilier", "Accessoires & mobilier",
                "Articles ajoutables à n'importe quel devis compatible.", [22, 40, 44, 12, 30, 12, 26, 30, 12],
                onglet="B48A57")
    lignes = [["Mobilier", "Banc laqué assorti", "Banc laqué : blanc, noir, gris clair, anthracite ou aluminium", 740,
               "Référence, Design, Prestige", "Actif", None, None, None]]
    lignes += [[c, a, d, prix, g, "Actif", None, None, ref] for c, a, d, prix, g, ref in gp.ACCESSOIRES]
    lignes += [[c, a, d, prix, "Lafuge", "Actif", None, None, None] for c, a, d, prix in lt.accessoires()]
    f.bloc(
        "ACCESSOIRES",
        ["Catégorie", "Article", "Détail imprimé sur le devis", "Prix TTC", "Gammes compatibles", "Statut", "Photo",
         "Note interne", "Réf."],
        lignes, vides=10, formats={"Prix TTC": EURO}, validations={"Statut": STATUTS},
        note="Une ligne par référence. Grille papier p. 11 (19/11).",
    )


def onglet_livraison(wb):
    f = Feuille(wb, "Livraison & montage", "Livraison & montage",
                "Une seule formule par devis. La valeur « si offert » s'affiche barrée à côté de « Offerte ».",
                [34, 50, 12, 14, 26, 12, 40], onglet="3D4248")
    f.bloc(
        "FORMULES",
        ["Formule", "Détail imprimé sur le devis", "Prix TTC", "Valeur si offert", "Gammes compatibles", "Statut",
         "Note interne"],
        [
            ["Livraison offerte", "Livraison au pied de la porte par messagerie, sur palette fabriquée sur mesure",
             0, 300, "Toutes", "Actif", None],
            ["Livraison et montage — rez-de-chaussée", "Livraison et montage complet par nos techniciens", 725, None,
             "Toutes", "Masqué", "Ancienne grille du site : à remplacer par la nouvelle grille"],
            ["Livraison et montage — sous-sol ou 1er étage", "Livraison et montage complet par nos techniciens", 875,
             None, "Toutes", "Masqué", "Ancienne grille du site : à remplacer par la nouvelle grille"],
            ["Livraison et montage — autre configuration", "Sur devis complémentaire", None, None, "Toutes", "Masqué",
             "Ancienne grille du site : à remplacer par la nouvelle grille"],
        ],
        vides=10, formats={"Prix TTC": EURO, "Valeur si offert": EURO}, validations={"Statut": STATUTS},
    )


def onglet_equipe(wb):
    f = Feuille(wb, "Équipe", "Équipe", "Personnes proposées dans « Devis réalisé par ».", [26, 64, 12],
                onglet="151515")
    f.bloc("ÉQUIPE", ["Nom", "Fonction imprimée sur le devis", "Statut"], [
        ["Philippe Fitan", "PDG de Billards de France (Billards Plaisance et Lafuge)", "Actif"],
        ["Stéphanie Guigon", "Secrétaire commerciale et achats Billards Lafuge", "Actif"],
        ["Xavier Fitan", "Directeur du développement & de la transformation digitale", "Actif"],
        ["Alain Bottacin", "Production / secrétariat", "Actif"],
    ], vides=4, validations={"Statut": STATUTS})


def onglet_revendeurs(wb):
    f = Feuille(wb, "Revendeurs", "Showrooms & revendeurs",
                "Points affichés sur la carte de France du devis, avec leur lettre.",
                [8, 36, 14, 24, 40, 12, 12, 12, 40], onglet="7A9A1E")
    f.bloc("POINTS DE VENTE", ["Lettre", "Nom", "Type", "Ville", "Adresse", "Latitude", "Longitude", "Statut",
                               "Note interne"], [
        ["A", "Showroom et atelier Billards de France", "Showroom", "Plaisance-du-Gers (32)",
         "Chemin de la Riberotte, 32160 Plaisance-du-Gers", 43.609446, 0.0542193, "Actif",
         "Environ 50 billards : quasiment tous les Plaisance et les Lafuge"],
        ["B", "Showroom et atelier Billard Lafuge", "Showroom", "Miribel-les-Échelles (38)", "38380 Miribel-les-Échelles",
         45.4306, 5.7139, "Actif", "Environ 30 billards. Coordonnées du village, à préciser"],
        ["C", "L'Ébéno", "Revendeur", "Région toulousaine", None, 43.6011249, 1.3011746, "Actif", "Adresse à compléter"],
        ["D", "L'Univers du Billard", "Revendeur", "Région nantaise", None, 47.1103146, -1.5435386, "Actif",
         "Adresse à compléter"],
    ], vides=6, validations={"Type": '"Showroom,Revendeur"', "Statut": STATUTS})


def onglet_parametres(wb):
    f = Feuille(wb, "Paramètres", "Paramètres", "Valeurs utilisées par tous les devis.", [44, 40, 60],
                onglet="151515")
    lignes = [
        ["Validité du devis (jours)", 30, "La date limite est imprimée sur le devis"],
        ["Acompte à la validation — Plaisance", 0.30, "Solde avant livraison"],
        ["Acompte à la validation — Lafuge", 0.30, None],
        ["Versement au lancement en production — Lafuge", 0.30, "Solde avant livraison"],
        ["Seuil Oney 3x / 4x (€)", 3000, "L'encadré Oney apparaît si le total TTC est inférieur ou égal"],
        ["Taux de TVA", 0.20, "Les prix sont saisis TTC"],
        ["Préfixe des références de devis", "BDF", "Exemple : BDF-2026-0001"],
        ["Email de validation client", "contact@billardsdefrance.fr", "Destinataire du bouton « Je valide mon devis »"],
        ["Téléphone « Appeler mon conseiller »", "05 62 69 30 20", None],
        ["Avis Google Plaisance — note", 4.7, None],
        ["Avis Google Plaisance — nombre d'avis", 47, None],
        ["Avis Google Lafuge — note", 4.8, None],
        ["Avis Google Lafuge — nombre d'avis", 21, None],
        ["Clients satisfaits", 25000, None],
        ["Garantie (années)", 2, None],
        ["Raison sociale", "FITAN et FILS SAS", None],
        ["Capital social", "406 875 €", None],
        ["SIRET", "997 739 107 00016", None],
        ["TVA intracommunautaire", "FR63997739107", None],
        ["RCS", "RCS Auch 997 739 107", "Confirmé le 17/11/2026"],
        ["Adresse du siège", "Chemin de la Riberotte, 32160 Plaisance-du-Gers", None],
        ["Site internet", "www.billardsdefrance.fr", None],
    ]
    p, _ = f.bloc("PARAMÈTRES", ["Paramètre", "Valeur", "Explication"], lignes)
    for i, (nom, _, _) in enumerate(lignes):
        c = f.ws.cell(p + i, 2)
        if "Acompte" in nom or "Versement" in nom or nom == "Taux de TVA":
            c.number_format = POURCENT
        if nom.startswith("Seuil"):
            c.number_format = EURO
        c.alignment = Alignment(horizontal="left")


def onglet_journal(wb):
    f = Feuille(wb, "Journal", "Journal des devis",
                "Rempli automatiquement par l'outil à chaque devis généré. Ne pas modifier.",
                [18, 14, 20, 16, 26, 20, 14, 26, 12, 12, 60], onglet="9A9D9F")
    f.bloc("DEVIS", ["Référence", "Date", "Réalisé par", "N° facturation", "Client", "Ville", "Gamme", "Modèle",
                     "Total TTC", "Remise", "Configuration complète"], [], vides=0)


def onglet_mode_emploi(wb):
    ws = wb.create_sheet("Mode d'emploi", 0)
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = ROUGE
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 110
    lignes = [
        ("titre", "Tarifs & contenus — mode d'emploi"),
        ("texte", "Ce fichier alimente l'outil de devis : prix, options, photos et textes. "
                  "Ce qui est modifié ici apparaît dans le prochain devis, sans rien toucher d'autre."),
        ("section", "Les 3 règles"),
        ("texte", "1. Ne renommez pas les titres qui commencent par ■ ni les en-têtes beiges : l'outil s'en sert pour lire le fichier."),
        ("texte", "2. Pour ajouter un modèle, une option ou un argument : remplissez une ligne crème vide du bon bloc, "
                  "ou insérez une ligne à l'intérieur du bloc. Ajouter des lignes ou des colonnes ne casse rien : il n'y a aucune formule."),
        ("texte", "3. Pour retirer un élément sans le perdre : passez son Statut à « Masqué »."),
        ("section", "Statut"),
        ("texte", "Actif : proposé dans l'outil.   Bientôt : prêt mais pas encore proposé (passez-le en Actif le jour J).   "
                  "Masqué : invisible dans l'outil.   À valider (arguments) : texte en attente de relecture."),
        ("section", "Options"),
        ("texte", "Groupe : les options d'un même groupe s'affichent ensemble (ex. Tapis, Plateau table)."),
        ("texte", "Choix : « Un seul par groupe » (ex. un seul tapis) ou « Plusieurs possibles » (ex. RAL + vernis brillant)."),
        ("texte", "Nécessite : nom exact d'une option ou d'un groupe requis (ex. le motif à carré nécessite « Plateau table bois »)."),
        ("texte", "Exclut : nom exact d'une option incompatible (ex. le 2e jeu américain exclut « Jeu de bandes américain »)."),
        ("texte", "Valable pour : « Tous », une version (ex. « Pieds métalliques ») ou des modèles séparés par des virgules."),
        ("texte", "Prix TTC en euros. Prix vide = sur devis. Valeur si offert : montant affiché barré à côté de « Offert »."),
        ("section", "Arguments & photos (réassurance)"),
        ("texte", "Dans l'outil, après le choix du produit, on coche au maximum 4 arguments selon le client. "
                  "« Proposé par défaut = Oui » les pré-coche (4 au maximum par gamme et par version)."),
        ("texte", "Valable pour : « Tous » pour toute la gamme, ou une version (ex. « Pieds métalliques »). "
                  "Photo : lien vers la photo ultra zoomée ; « À fournir » = photo attendue ; vide = argument en texte seul."),
        ("section", "Lafuge (onglets « Lafuge mixte » et « Lafuge bandes françaises »)"),
        ("texte", "Un bloc par fiche papier (ex. « ■ LOFT · ÉLÉGANCE ») : le prix du billard puis toutes ses options, "
                  "une colonne par taille. Le bloc MODÈLES sert à retrouver vite le prix d'un billard."),
        ("texte", "Cases de prix : nombre = prix ; « Inclus » ; « Impossible » ; « Sur demande » = prix saisi à la main "
                  "dans l'outil ; « — » = taille non proposée pour ce modèle ; case vide (surlignée) = pas encore chiffrée."),
        ("texte", "Les prix revendeur HT sont dans un classeur séparé et confidentiel, jamais lu par l'outil de devis."),
        ("section", "Photos"),
        ("texte", "Collez un lien : photo du site billardsdefrance.fr (clic droit sur l'image > copier l'adresse) "
                  "ou fichier Google Drive partagé en lecture."),
        ("section", "Nouvelle gamme"),
        ("texte", "Dupliquez l'onglet d'une gamme existante, renommez-le, puis adaptez les blocs."),
    ]
    for i, (kind, txt) in enumerate(lignes, start=2):
        c = ws.cell(i, 2, txt)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if kind == "titre":
            c.font = TITRE
            ws.row_dimensions[i].height = 36
        elif kind == "section":
            c.font = Font(name="DM Sans", size=12, bold=True, color=ROUGE)
            ws.row_dimensions[i].height = 26
        else:
            c.font = Font(name="DM Sans", size=11, color=ENCRE)
            ws.row_dimensions[i].height = 32 if len(txt) > 110 else 18


def main():
    donnees, sortie = Path(sys.argv[1]), Path(sys.argv[2])
    ref = json.loads((donnees / "reference.json").read_text(encoding="utf-8"))
    dp = json.loads((donnees / "design-prestige-site-brut.json").read_text(encoding="utf-8"))
    wb = Workbook()
    wb.remove(wb.active)
    onglet_reference(wb, ref)
    onglet_design(wb, dp)
    onglet_prestige(wb, dp)
    onglets_lafuge(wb)
    onglet_lafuge_contenus(wb)
    onglet_coloris(wb)
    onglet_accessoires(wb)
    onglet_livraison(wb)
    onglet_equipe(wb)
    onglet_revendeurs(wb)
    onglet_parametres(wb)
    onglet_journal(wb)
    onglet_mode_emploi(wb)
    wb.active = 0
    wb.save(sortie)
    print(f"Classeur écrit : {sortie} ({', '.join(wb.sheetnames)})")
    if len(sys.argv) > 3:
        print(f"Classeur revendeurs écrit : {sys.argv[3]} ({', '.join(classeur_revendeurs(Path(sys.argv[3])))})")


if __name__ == "__main__":
    main()
