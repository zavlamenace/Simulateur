"""Tarifs Lafuge au 01/01/2027 : billard mixte (pool, américain, anglais, snooker, russe) et billard français à bandes fixes.

Source : les 4 documents Word de connaissances/sources/lafuge-2027/ (vente TTC et revendeur HT, pool et français),
corrigés avec l'utilisateur les 20 et 25/11/2026. Chaque correction est listée dans CORRECTIONS et commentée.
Le contrôle croisé avec les documents est dans devis/tests/test_lafuge.py.

Convention des cases (prix TTC) :
  nombre        prix de l'option ou du billard à cette taille
  « Inclus »    compris dans le prix, sans supplément
  « Impossible » option impossible à cette taille
  « Sur demande » le vendeur saisit le prix à la main dans l'outil
  « — »         le modèle n'existe pas dans cette taille
  vide (None)   pas encore chiffré : à compléter dans le Sheet
Prix revendeur HT = prix TTC ÷ 2 (règle confirmée le 20/11).
"""
from dataclasses import dataclass, field

IMP, SD, INC, NP = "Impossible", "Sur demande", "Inclus", "—"

TAILLES = {
    "mixte": ["2,10 m", "2,30 m", "2,40 m", "2,60 m", "2,80 m", "10 pieds", "12 pieds"],
    "français": ["2,30 m", "2,40 m", "2,60 m", "2,80 m", "3,10 m"],
}
GRANDS = ("10 pieds", "12 pieds")

# Taille : (dimensions hors tout, surface de jeu, ardoise mixte, ardoise français), en mètres et mm.
DIMENSIONS = {
    "2,10 m": ("2,10 × 1,20", "1,80 × 0,90", "19 mm", None),
    "2,30 m": ("2,30 × 1,30", "2,00 × 1,00", "19 mm", "19 mm"),
    "2,40 m": ("2,44 × 1,37", "2,14 × 1,07", "30 mm", "30 mm"),
    "2,60 m": ("2,64 × 1,47", "2,34 × 1,17", "30 mm", "40 mm"),
    "2,80 m": ("2,84 × 1,57", "2,54 × 1,27", "30 mm", "50 mm"),
    "3,10 m": ("3,14 × 1,72", "2,84 × 1,42", None, "50 mm"),
    "10 pieds": ("3,22 × 1,74", "2,95 × 1,475", "38 mm", None),
    "12 pieds": ("3,83 × 2,04", "3,57 × 1,78", "45 mm", None),
}


@dataclass
class Option:
    groupe: str
    nom: str
    prix: dict                      # taille → valeur (voir convention)
    valable_pour: str = "Tous"      # « Tous » ou nom de modèle(s) de la fiche
    conditions: str = ""            # en clair, pour la lecture
    necessite: str = ""             # noms d'options, séparés par « ; »
    exclut: str = ""
    choix: str = "Plusieurs possibles"
    detail: str = ""                # imprimé sur le devis
    note: str = ""                  # interne
    doc: str = ""                   # clé dans les documents (contrôle croisé) ; vide = ligne ajoutée


@dataclass
class Fiche:
    nom: str                        # titre du bloc, comme la page papier
    jeu: str                        # « mixte » ou « français »
    modeles: dict                   # modèle → {taille: prix}
    base: str                       # ligne sous le titre, en clair
    table: bool = True              # existe en version table (plateau possible)
    options: list = field(default_factory=list)
    technique: list = field(default_factory=list)   # (élément, version de base, version laquée, version bois massif)


# --- Aides de saisie -------------------------------------------------------------------------------------------

def tailles_de(fiche_tailles, jeu):
    return [t for t in TAILLES[jeu] if t in fiche_tailles]


def colonnes(jeu, tailles, valeurs, grands=SD):
    """Répartit les colonnes du document sur les tailles du modèle.

    Mixte : colonnes du document = [2,10–2,30, 2,40, 2,60, 2,80] (une seule valeur = toutes tailles).
    Français : [2,30, 2,40, 2,60, 2,80, 3,10].
    Les tailles absentes du modèle reçoivent « — » ; le 10 et le 12 pieds reçoivent `grands` (valeur ou paire).
    """
    out = {}
    if jeu == "mixte":
        ordre = ["2,30 m", "2,40 m", "2,60 m", "2,80 m"]
        for i, t in enumerate(ordre):
            out[t] = valeurs[i] if i < len(valeurs) else (valeurs[0] if len(valeurs) == 1 else None)
        out["2,10 m"] = out["2,30 m"]
        g = grands if isinstance(grands, tuple) else (grands, grands)
        out["10 pieds"], out["12 pieds"] = g
    else:
        for i, t in enumerate(TAILLES["français"]):
            out[t] = valeurs[i] if i < len(valeurs) else (valeurs[0] if len(valeurs) == 1 else None)
    return {t: (out[t] if t in tailles else NP) for t in TAILLES[jeu]}


def prix_modele(jeu, valeurs):
    """valeurs : dict taille → prix pour les tailles proposées ; « — » ailleurs."""
    return {t: valeurs.get(t, NP) for t in TAILLES[jeu]}


def partout(jeu, tailles, valeur, grands=SD):
    return colonnes(jeu, tailles, [valeur], grands)


# --- Noms d'options communs (servent aussi dans Nécessite / Exclut) --------------------------------------------

CHENE, MELEZE, NOYER = "Chêne massif", "Mélèze massif", "Noyer massif"
PARCHEMIN, BROSSEE, BICOLORE = ("Finition parchemin, patine antiquaire ou cérusée", "Finition brossée",
                                "Finition bicolore vernie")
TEINTE_INCLUSE, TEINTE_SPECIALE = "Teinte incluse", "Teinte spéciale"
LAQUE, LISERE, LISERE_ALU = "Laque", "Liseré de couleur", "Liseré aluminium ou bois gainé du drap"
REPERES, JEU2, A37 = "Repères de bandes en nacre", "2e jeu de bandes interchangeables", "Bandes A37 toilées"
CUIR, SOFIC = "Entrées de poche en cuir noir", "Cuir de couleur (gamme SOFIC)"
# 26/11 : cuir noir ou cuir de couleur SOFIC, l'un ou l'autre (plus de « Nécessite »).
POCHES_CUIR = "Entrées de poche en cuir"
CADRE_DEM, PIET_DEM = "Cadre démontable", "Piètement démontable"
ELASTHANNE = "Boîtes élasthanne"
CADRE_SNOOKER, SIX_PIEDS, RETOUR, PLOTS, CHAUFFAGE = ("Cadre snooker", "Option 6 pieds", "Retour centralisé des billes",
                                                       "Plots Altuglas", "Chauffage de l'ardoise")

TXT_DEMONTABLE = "Pour une pièce d'accès difficile : le billard se démonte pour passer."
TXT_CADRE_SNOOKER = ("Le cadre est découpé à l'endroit des poches pour laisser apparentes les poches en cuir, "
                     "comme sur les snookers d'autrefois.")
TXT_PLOTS = "Plots transparents à la place des plots inox : le billard semble en lévitation."
TXT_A37 = "Bandes en caoutchouc A37 toilé, la référence haut de gamme du billard français."
TXT_ELASTHANNE = "Jupe du cadre affinée de 20 mm."


def essences(f, tailles, chene, meleze=None, noyer=None, chene_nom=CHENE, meleze_nom=MELEZE, base_chene=False,
             grands=SD, meleze_pour="Tous", doc_prefixe=""):
    """Groupe Essence. `base_chene` : la base est déjà du chêne (placage) ; sinon les finitions exigent le chêne."""
    jeu = f.jeu
    excl = LAQUE
    opts = [Option("Essence", chene_nom, colonnes(jeu, tailles, chene, grands), exclut=excl,
                   choix="Un seul par groupe", conditions="Impossible avec la laque", doc=CHENE)]
    if meleze is not None:
        valeur = colonnes(jeu, tailles, meleze, SD) if meleze != IMP else colonnes(jeu, tailles, [IMP], IMP)
        opts.append(Option("Essence", meleze_nom, valeur, valable_pour=meleze_pour, exclut=excl,
                           choix="Un seul par groupe",
                           conditions="Impossible avec la laque" + (f" ; {meleze_pour} uniquement"
                                                                    if meleze_pour != "Tous" else ""),
                           doc=MELEZE if meleze != IMP else ""))
    if noyer is not None:
        valeur = colonnes(jeu, tailles, noyer, SD) if noyer != SD else colonnes(jeu, tailles, [SD], SD)
        opts.append(Option("Essence", NOYER, valeur, exclut=excl, choix="Un seul par groupe",
                           conditions="Impossible avec la laque", doc=NOYER if noyer != SD else ""))
    return opts


def finitions(f, tailles, parchemin, brossee, bicolore, base_chene, grands=SD, chene_nom=CHENE):
    jeu = f.jeu
    cond = "Sur chêne uniquement" if base_chene else f"Nécessite « {chene_nom} » (sur chêne uniquement)"
    nec = "" if base_chene else chene_nom
    excl = f"{LAQUE} ; {MELEZE} ; {NOYER}"
    opts = [
        Option("Finition", PARCHEMIN, colonnes(jeu, tailles, parchemin, grands), necessite=nec, exclut=excl,
               conditions=cond, doc=PARCHEMIN),
        Option("Finition", BROSSEE, colonnes(jeu, tailles, brossee, grands), necessite=nec, exclut=excl,
               conditions=cond, doc=BROSSEE),
    ]
    if bicolore == IMP:
        opts.append(Option("Finition", BICOLORE, colonnes(jeu, tailles, [IMP], IMP)))
    else:
        opts.append(Option("Finition", BICOLORE, colonnes(jeu, tailles, bicolore, grands), exclut=LAQUE,
                           conditions="Deux teintes sur le billard ; impossible avec la laque", doc=BICOLORE))
    return opts


PLACAGE_ERABLE = "Placage érable"
# 26/11 : les modèles en MDF plaqué chêne se font aussi, sans supplément, en placage érable. Les modèles en érable
# massif d'origine ne se font pas en placage érable.
MODELES_PLACAGE = {"SOHO", "ARCADE", "TROCADÉRO", "MONT BLANC", "CITY · ÉOS", "EIFFEL · ALPHA", "BEAUBOURG"}


def placage(f, tailles):
    # Exclut les essences massives, la laque et les finitions réservées au chêne.
    exclut = " ; ".join(o.nom for o in f.options if o.groupe in ("Essence", "Laque") or o.nom in (PARCHEMIN, BROSSEE))
    return Option("Placage", PLACAGE_ERABLE, colonnes(f.jeu, tailles, [0], 0), exclut=exclut,
                  conditions="Au lieu du placage chêne, sans supplément ; impossible avec une essence massive, la laque ou une finition sur chêne",
                  note="Ajouté le 26/11")


def ajouter_placage(f, tailles):
    """Insère « Placage érable » juste avant le groupe Essence."""
    i = next(k for k, o in enumerate(f.options) if o.groupe == "Essence")
    f.options.insert(i, placage(f, tailles))


def retouches_26_11(fiches):
    """Retouches du 26/11 sur les fiches construites : placage érable, brossée du Trocadéro.

    27/11 : le Soho n'existe pas en érable massif (ajout du 26/11 retiré)."""
    for f in fiches:
        tailles = [t for t, v in next(iter(f.modeles.values())).items() if v not in (NP, IMP)]
        if f.nom in MODELES_PLACAGE:
            ajouter_placage(f, tailles)
        if f.nom == "TROCADÉRO":
            brossee_sur_meleze(f)
        # 26/11 : « Exclut » et « Nécessite » ne citent que des options de la fiche (contrôle des règles du Sheet).
        noms = {o.nom for o in f.options} | {o.groupe for o in f.options} | {p[1] for p in plateaux(f.jeu)}
        for o in f.options:
            o.exclut = " ; ".join(x.strip() for x in o.exclut.split(";") if x.strip() in noms)
            o.necessite = " ; ".join(x.strip() for x in o.necessite.split(";") if x.strip() in noms)
    return fiches


def brossee_sur_meleze(f):
    """26/11 : sur le Trocadéro, la finition brossée est aussi proposée avec le mélèze massif."""
    for o in f.options:
        if o.nom == BROSSEE:
            o.exclut = " ; ".join(x.strip() for x in o.exclut.split(";") if x.strip() != MELEZE)
            o.conditions = "Sur chêne ou mélèze"


def teinte(f, tailles, speciale=True):
    jeu = f.jeu
    return [
        Option("Teinte", TEINTE_INCLUSE, colonnes(jeu, tailles, [INC], INC), choix="Un seul par groupe"),
        Option("Teinte", TEINTE_SPECIALE, colonnes(jeu, tailles, [600 if speciale else IMP], 600 if speciale else IMP),
               choix="Un seul par groupe", exclut=LAQUE if speciale else "",
               conditions="Teinte hors nuancier ; impossible avec la laque" if speciale else ""),
    ]


def laque(f, tailles, valeurs, grands=SD, nom=LAQUE, conditions="", doc=LAQUE):
    jeu = f.jeu
    excl = f"{CHENE} ; {MELEZE} ; {NOYER} ; {REPERES} ; {BICOLORE} ; {TEINTE_SPECIALE} ; {PARCHEMIN} ; {BROSSEE}"
    cond = "Seul le liseré de couleur reste possible" + (f" ; {conditions}" if conditions else "")
    return Option("Laque", nom, colonnes(jeu, tailles, valeurs, grands), exclut=excl, conditions=cond, doc=doc)


def communs(f, tailles, liseré=True, repères=True, cuir=True, sofic=True, cadre=410, pietement=410,
            jeu2=None, elasthanne=0, grands=SD, a37=True, chauffage=None, liseré_doc=True, cadre_doc=True,
            pietement_doc=True):
    """Options présentes sur (presque) tous les billards, dans l'ordre des fiches papier."""
    jeu, opts = f.jeu, []
    if liseré is not None:
        opts.append(Option("Liseré", LISERE, colonnes(jeu, tailles, [400 if liseré else IMP], grands if liseré else IMP),
                           conditions="Le seul décor possible avec la laque", doc=LISERE if liseré_doc else "",
                           note="" if liseré_doc else "Ajouté le 25/11 : liseré de couleur sur tous les billards sauf Harmonie"))
    if repères:
        opts.append(Option("Repères", REPERES, colonnes(jeu, tailles, [400], grands), exclut=LAQUE,
                           conditions="Impossible avec la laque", doc=REPERES))
    if jeu == "mixte":
        if jeu2 is not None:
            opts.append(Option("Bandes", JEU2, colonnes(jeu, tailles, jeu2, IMP),
                               conditions="Jeu d'un autre type que les bandes initiales ; impossible en 10 et 12 pieds",
                               doc=JEU2))
        if cuir is not None:
            opts.append(Option(POCHES_CUIR, CUIR, colonnes(jeu, tailles, [cuir if cuir != INC else INC],
                                                           grands if cuir != INC else INC),
                               choix="Un seul par groupe", doc=CUIR if cuir not in (INC,) else ""))
        if sofic:
            opts.append(Option(POCHES_CUIR, SOFIC, colonnes(jeu, tailles, [990], grands),
                               choix="Un seul par groupe",
                               conditions="Cuir noir ou cuir de couleur : l'un ou l'autre", doc=SOFIC))
        # 26/11 : sans supplément, à toutes les tailles ; impossible sur City, Éos, Eiffel, Alpha, Beaubourg,
        # Compétition et Harmonie.
        opts.append(Option("Poches", ELASTHANNE, colonnes(jeu, tailles, [elasthanne], elasthanne),
                           detail=TXT_ELASTHANNE,
                           note="Sans supplément (26/11)" if elasthanne != IMP else "Impossible sur ce modèle"))
    else:
        if a37:
            v = {"2,30 m": 750, "2,40 m": 750, "2,60 m": INC, "2,80 m": INC, "3,10 m": INC}
            opts.append(Option("Bandes", A37, {t: (v[t] if t in tailles else NP) for t in TAILLES[jeu]},
                               conditions="Option jusqu'à 2,40 m, incluse au-delà", detail=TXT_A37,
                               doc=A37 if a37 == "doc" else "",
                               note="" if a37 == "doc" else "Ajouté le 25/11 : A37 sur tous les billards français"))
        if chauffage is not None:
            opts.append(Option("Bandes", CHAUFFAGE, colonnes(jeu, tailles, chauffage),
                               conditions="À partir de 2,40 m", doc=CHAUFFAGE))
    opts.append(Option("Démontage", CADRE_DEM, colonnes(jeu, tailles, [cadre], grands if cadre not in (IMP, INC) else cadre),
                       detail=TXT_DEMONTABLE, doc=CADRE_DEM if cadre_doc and isinstance(cadre, int) else "",
                       note="" if cadre_doc else "Ajouté le 25/11"))
    opts.append(Option("Démontage", PIET_DEM,
                       colonnes(jeu, tailles, [pietement], grands if pietement not in (IMP, INC, None) else pietement),
                       detail=TXT_DEMONTABLE if pietement not in (IMP,) else "",
                       doc=PIET_DEM if pietement_doc and isinstance(pietement, int) else "",
                       note=("Ajouté le 25/11" if not pietement_doc and isinstance(pietement, int) else
                             "Pas encore chiffré" if pietement is None else
                             "Piètement toujours démontable" if pietement == INC else "")))
    return opts


BANDES_INIT = "Bandes initiales (une incluse)"
# Libellés du 27/11 (jamais « Bandes de snooker » ni « Bandes de billard russe »).
JEU_SNOOKER, JEU_RUSSE = "Jeu snooker", "Jeu pyramide russe"


def jeux_mixte(f, tailles, grands_formats):
    """Bandes initiales : une seule au choix, comprise dans le prix ; le 2e jeu de bandes est une option."""
    opts = []
    cond = "Une seule au choix, incluse dans le prix ; le 2e jeu de bandes est en option (dès 860 €)"
    for nom in ("Bandes initiales américaines", "Bandes initiales anglaises", "Bandes initiales françaises"):
        opts.append(Option(BANDES_INIT, nom, colonnes("mixte", tailles, [INC], IMP), choix="Un seul par groupe",
                           conditions=cond))
    if grands_formats:
        for nom in (JEU_SNOOKER, JEU_RUSSE):
            opts.append(Option(BANDES_INIT, nom, colonnes("mixte", tailles, [IMP], INC), choix="Un seul par groupe",
                               conditions="10 et 12 pieds : le client choisit son jeu, snooker ou pyramide russe, "
                                          "inclus, au même prix"))
    return opts


def renommer_laque(f, nom="Laque du cadre"):
    """Beaubourg : seule la laque du cadre existe ; les renvois à « Laque » pointent vers elle."""
    for o in f.options:
        for champ in ("necessite", "exclut"):
            refs = [r.strip() for r in getattr(o, champ).split(";") if r.strip()]
            setattr(o, champ, " ; ".join(nom if r == LAQUE else r for r in refs))
    return f


def option_bois(fiche, element):
    """Colonne « En option » d'une fiche technique : les essences massives proposées sur la fiche."""
    nom, base, laquee, massif = element
    if not massif and not laquee:
        return None
    if massif == base and any(m in base.lower() for m in ("acier", "métallique")) and "bois" not in base.lower():
        return "Inchangé (acier)"
    if massif != "Bois massif de l'essence choisie":
        return "Identique" if massif == base else massif
    chiffrees, demande = [], []
    for o in fiche.options:
        if o.groupe != "Essence":
            continue
        valeurs = set(o.prix.values()) - {NP, IMP}
        essence = o.nom.replace("Cadre en ", "")
        if any(isinstance(v, (int, float)) for v in valeurs):
            chiffrees.append(essence)
        elif SD in valeurs:
            demande.append(essence)
    ordre = {CHENE: 0, MELEZE: 1, NOYER: 2}
    chiffrees.sort(key=lambda e: ordre.get(e, 9))
    if not chiffrees and not demande:
        return None
    texte = " ou ".join([chiffrees[0][0].upper() + chiffrees[0][1:]] + [e.lower() for e in chiffrees[1:]]) if chiffrees else ""
    if demande:
        texte += (" ; " if texte else "") + " ou ".join(e.lower().replace(" massif", "") for e in demande) + " sur demande"
    return texte[0].upper() + texte[1:]


# --- Fiches techniques ---------------------------------------------------------------------------------------

def tech_massif(base, laquee, massif=None):
    return (base, laquee, massif if massif is not None else "Bois massif de l'essence choisie")


ACIER_60_60 = "Double barre en acier de section 60 × 60 mm, épaisseur 5 mm"
ACIER_60_40 = "Double barre en acier de section 60 × 40 mm, épaisseur 3 mm"


# --- Billard mixte (document « Billards Lafuge pool et US », TTC) --------------------------------------------

def fiches_mixte():
    J = "mixte"
    out = []

    T = ["2,10 m", "2,30 m", "2,40 m", "2,60 m"]
    f = Fiche("LOFT · ÉLÉGANCE", J, {}, "Érable sycomore massif")
    prix = {"2,10 m": 5600, "2,30 m": 6300, "2,40 m": 7800, "2,60 m": 8300}
    f.modeles = {"Loft": prix_modele(J, prix), "Élégance": prix_modele(J, prix)}
    f.options = (jeux_mixte(f, T, False)
                 + essences(f, T, [700, 820, 940], [700, 820, 940], SD)
                 + finitions(f, T, [700, 820, 940], [700, 820, 940], [300, 400, 500], base_chene=False)
                 + teinte(f, T) + [laque(f, T, [1600, 1700, 1800])]
                 + communs(f, T, jeu2=[860, 920, 990], cuir=480))
    f.technique = [("Mention", "Billard 100 % bois massif", "", ""),
                   ("Cadre", *tech_massif("Érable sycomore massif", "MDF")),
                   ("Pieds", *tech_massif("Érable sycomore massif", "MDF")),
                   ("Traverses", *tech_massif("Érable sycomore massif", "Érable massif"))]
    out.append(f)

    f = Fiche("SOHO", J, {}, "MDF plaqué chêne")
    f.modeles = {"Soho": prix_modele(J, {"2,10 m": 5400, "2,30 m": 6100, "2,40 m": 7600, "2,60 m": 8100})}
    f.options = (jeux_mixte(f, T, False)
                 + essences(f, T, [1320, 1440, 1560], [1320, 1440, 1560], None, base_chene=True)
                 + finitions(f, T, [700, 810, 920], [700, 810, 920], [300, 400, 500], base_chene=True)
                 + teinte(f, T) + [laque(f, T, [1600, 1700, 1800]),
                                   Option("Liseré", LISERE_ALU, colonnes(J, T, [900, 900, 900]), doc=LISERE_ALU,
                                          conditions="Liseré aluminium, ou bois gainé du drap du billard (rappel de couleur)")]
                 + communs(f, T, jeu2=[860, 920, 990], cuir=480))
    f.technique = [("Cadre", *tech_massif("MDF plaqué chêne", "MDF")),
                   ("Pieds", *tech_massif("MDF plaqué chêne", "MDF")),
                   ("Traverses", *tech_massif("Chêne massif", "Érable massif"))]
    out.append(f)

    T2 = ["2,10 m", "2,30 m"]
    f = Fiche("CITY · ÉOS", J, {}, "MDF plaqué chêne")
    f.modeles = {"City": prix_modele(J, {"2,10 m": 5200, "2,30 m": 5900}),
                 "Éos": prix_modele(J, {"2,10 m": 5040, "2,30 m": 5740})}
    f.options = (jeux_mixte(f, T2, False)
                 + essences(f, T2, [1320], [1320], None, base_chene=True)
                 + finitions(f, T2, [700], [700], [300], base_chene=True)
                 + teinte(f, T2) + [laque(f, T2, [1500]),
                                    Option("Liseré", LISERE_ALU, colonnes(J, T2, [650]), doc=LISERE_ALU,
                                           conditions="Liseré aluminium, ou bois gainé du drap du billard (rappel de couleur)")]
                 + communs(f, T2, jeu2=[860], cuir=480, elasthanne=IMP, cadre_doc=False, pietement=IMP))
    f.technique = [("Châssis", ACIER_60_60, ACIER_60_60, ACIER_60_60),
                   ("Cadre", *tech_massif("MDF plaqué chêne", "MDF")),
                   ("Pieds", *tech_massif("MDF plaqué chêne, 120 × 120 mm", "MDF")),
                   ("Traverses", *tech_massif("Multiplis 40 mm plaqué chêne (plus résistant que le bois massif)",
                                              "Érable massif")),
                   ("Forme des pieds (City)", "Biseautés", "Biseautés", "Biseautés")]
    out.append(f)

    f = Fiche("EIFFEL · ALPHA", J, {}, "MDF plaqué chêne, pieds en acier")
    prix = {"2,10 m": 5780, "2,30 m": 6480}
    f.modeles = {"Eiffel": prix_modele(J, prix), "Alpha": prix_modele(J, prix)}
    f.options = (jeux_mixte(f, T2, False)
                 + essences(f, T2, [1000], [1000], [4000], base_chene=True)
                 + finitions(f, T2, [630], [630], [300], base_chene=True)
                 + teinte(f, T2) + [laque(f, T2, [1100]),
                                    Option("Liseré", LISERE_ALU, colonnes(J, T2, [650]), doc=LISERE_ALU,
                                           conditions="Liseré aluminium, ou bois gainé du drap du billard (rappel de couleur)")]
                 + communs(f, T2, jeu2=[860], cuir=480, elasthanne=IMP, cadre_doc=False, pietement=IMP))
    acier = "Acier laqué au RAL choisi par le client"
    f.technique = [("Châssis", ACIER_60_60, ACIER_60_60, ACIER_60_60),
                   ("Cadre", *tech_massif("MDF plaqué chêne", "MDF")),
                   ("Pieds", acier, acier, acier),
                   ("Traverses", *tech_massif("Multiplis 40 mm plaqué chêne (plus résistant que le bois massif)",
                                              "Érable massif"))]
    out.append(f)

    f = Fiche("BEAUBOURG", J, {}, "MDF plaqué chêne ou érable, pieds et traverses en acier finition mat fine texture")
    f.modeles = {"Beaubourg": prix_modele(J, {"2,10 m": 5990, "2,30 m": 6690})}
    f.options = (jeux_mixte(f, T2, False)
                 + [Option("Essence", "Cadre en mélèze massif", colonnes(J, T2, [740]), exclut="Laque du cadre",
                           choix="Un seul par groupe", doc=MELEZE),
                    Option("Essence", "Cadre en chêne massif", colonnes(J, T2, [740]), exclut="Laque du cadre",
                           choix="Un seul par groupe", doc=CHENE),
                    Option("Finition", BROSSEE, colonnes(J, T2, [410]), exclut="Laque du cadre ; Cadre en mélèze massif",
                           conditions="Sur chêne uniquement", doc=BROSSEE),
                    Option("Finition", PARCHEMIN, colonnes(J, T2, [410]), exclut="Laque du cadre ; Cadre en mélèze massif",
                           conditions="Sur chêne uniquement", doc=PARCHEMIN),
                    Option("Finition", BICOLORE, colonnes(J, T2, [IMP], IMP), note="Déjà bicolore (bois et métal)")]
                 + teinte(f, T2)
                 + [Option("Laque", "Laque du cadre", colonnes(J, T2, [740]),
                           exclut=f"Cadre en mélèze massif ; Cadre en chêne massif ; {REPERES} ; {TEINTE_SPECIALE} ; "
                                  f"{PARCHEMIN} ; {BROSSEE}",
                           conditions="Seul le liseré de couleur reste possible", doc=LAQUE)]
                 + communs(f, T2, jeu2=[860], cuir=480, elasthanne=IMP, cadre_doc=False, pietement=IMP,
                           liseré_doc=False))
    renommer_laque(f)
    f.technique = [("Châssis", ACIER_60_60, ACIER_60_60, ACIER_60_60),
                   ("Cadre", *tech_massif("MDF plaqué chêne", "MDF")),  # 26/11 : érable = option « Placage érable »
                   ("Pieds", acier, acier, acier),
                   ("Traverses", "Multiplis 40 mm habillé d'une équerre en acier laqué",
                    "Multiplis 40 mm habillé d'une équerre en acier laqué",
                    "Multiplis 40 mm habillé d'une équerre en acier laqué")]
    out.append(f)

    TG = ["2,10 m", "2,30 m", "2,40 m", "2,60 m", "2,80 m", "10 pieds", "12 pieds"]
    chassis_upn = {"2,10 m": ACIER_60_40, "2,30 m": ACIER_60_40, "2,40 m": "Acier UPN de 80 mm",
                   "2,60 m": "Acier UPN de 100 mm",
                   "2,80 m": "Acier UPN de 80 mm avec 6 pieds, de 100 mm avec 4 pieds"}
    chassis_txt = " ; ".join(f"{t} : {v}" for t, v in chassis_upn.items())

    def grands(f, tailles, six_pieds=None, retour=None):
        """Options propres aux modèles qui existent en snooker et en russe."""
        o = [Option("Modèle", CADRE_SNOOKER, colonnes(J, tailles, [1000], (1000, 1000)), detail=TXT_CADRE_SNOOKER,
                    conditions="Modèles snooker et russe, toutes tailles", doc="")]
        if six_pieds:
            o.append(Option("Modèle", SIX_PIEDS, {t: six_pieds.get(t, IMP if t in tailles else NP)
                                                   for t in TAILLES[J]}, doc=SIX_PIEDS if six_pieds.get("doc") else "",
                            note=six_pieds.get("note", "")))
        if retour:
            o.append(Option("Modèle", RETOUR, colonnes(J, tailles, retour, IMP), doc=RETOUR,
                            conditions="Compétition et Chambord uniquement"))
        return o

    f = Fiche("ARCADE", J, {}, "MDF plaqué chêne, plots inox")
    f.modeles = {"Arcade": prix_modele(J, {"2,10 m": 6300, "2,30 m": 7000, "2,40 m": 9000, "2,60 m": 10000,
                                           "2,80 m": 12000, "10 pieds": 19000, "12 pieds": 21000})}
    f.options = (jeux_mixte(f, TG, True)
                 + essences(f, TG, [1820, 1940, 2060, 2180], [1820, 1940, 2060, 2180], None, base_chene=True,
                            grands=(2650, 2980))
                 + finitions(f, TG, [900, 950, 1000, 1050], [900, 950, 1000, 1050], [300, 400, 500, 600],
                             base_chene=True)
                 + teinte(f, TG) + [laque(f, TG, [1700, 1800, 1900, 2000], grands=(2540, 2760)),
                                    Option("Liseré", LISERE_ALU, colonnes(J, TG, [880, 900, 920, 940]), doc=LISERE_ALU,
                                           conditions="Liseré aluminium, ou bois gainé du drap du billard (rappel de couleur)"),
                                    Option("Modèle", PLOTS, colonnes(J, TG, [470, 470, 470, 470]), detail=TXT_PLOTS,
                                           doc=PLOTS)]
                 + communs(f, TG, jeu2=[860, 920, 990, 1060], cuir=480, pietement=IMP)
                 + grands(f, TG, six_pieds={"2,80 m": 1370, "note": "Confirmé le 25/11 (fiche technique)"}))
    f.technique = [("Châssis", chassis_txt, chassis_txt, chassis_txt),
                   ("Cadre", *tech_massif("MDF plaqué chêne", "MDF")),
                   ("Pieds", *tech_massif("MDF plaqué chêne", "MDF")),
                   ("Poutre", *tech_massif("MDF plaqué chêne", "MDF")),
                   ("Piètement", "2,80 m : 2 arches ; 10 pieds : 3 arches ; 12 pieds : 4 arches",
                    "2,80 m : 2 arches ; 10 pieds : 3 arches ; 12 pieds : 4 arches",
                    "2,80 m : 2 arches ; 10 pieds : 3 arches ; 12 pieds : 4 arches")]
    out.append(f)

    f = Fiche("TROCADÉRO", J, {}, "MDF plaqué chêne, pieds métalliques")
    f.modeles = {"Trocadéro": prix_modele(J, {"2,10 m": 6800, "2,30 m": 7500})}
    f.options = (jeux_mixte(f, T2, False)
                 + essences(f, T2, [1220], [1220], None, base_chene=True)
                 + finitions(f, T2, [760], [760], [300], base_chene=True)
                 + teinte(f, T2) + [laque(f, T2, [1100]),
                                    Option("Liseré", LISERE_ALU, colonnes(J, T2, [880]), doc=LISERE_ALU,
                                           conditions="Liseré aluminium, ou bois gainé du drap du billard (rappel de couleur)")]
                 + communs(f, T2, jeu2=[860], cuir=480, pietement=IMP))
    f.technique = [("Châssis", ACIER_60_40, ACIER_60_40, ACIER_60_40),
                   ("Cadre", *tech_massif("MDF plaqué chêne", "MDF")),
                   ("Pieds", "Métalliques laqués mat structuré", "Métalliques laqués mat structuré",
                    "Métalliques laqués mat structuré"),
                   ("Traverse", *tech_massif("Bois massif verni", "Bois massif laqué"))]
    out.append(f)

    f = Fiche("MONT BLANC", J, {}, "MDF plaqué chêne, pieds en bois massif")
    f.modeles = {"Mont Blanc": prix_modele(J, {"2,10 m": 6650, "2,30 m": 7350, "2,40 m": 9350, "2,60 m": 10350,
                                               "2,80 m": 12350, "10 pieds": 20400, "12 pieds": 22400})}
    f.options = (jeux_mixte(f, TG, True)
                 + essences(f, TG, [1220, 1440, 1660, 1880], [1220, 1440, 1660, 1880], None, base_chene=True,
                            grands=(2650, 2980))
                 + finitions(f, TG, [900, 950, 1000, 1050], [900, 950, 1000, 1050], [300, 400, 500, 600],
                             base_chene=True)
                 + teinte(f, TG) + [laque(f, TG, [2100, 2200, 2300, 2400], grands=(2540, 2760)),
                                    Option("Liseré", LISERE_ALU, colonnes(J, TG, [880, 900, 920, 940]), doc=LISERE_ALU,
                                           conditions="Liseré aluminium, ou bois gainé du drap du billard (rappel de couleur)")]
                 + communs(f, TG, jeu2=[860, 920, 990, 1060], cuir=480, pietement=IMP)
                 + grands(f, TG, six_pieds={"2,80 m": 1370, "note": "Confirmé le 25/11 (fiche technique)"}))
    f.technique = [("Châssis", chassis_txt, chassis_txt, chassis_txt),
                   ("Cadre", *tech_massif("MDF plaqué chêne", "MDF")),
                   ("Pieds", *tech_massif("Bois massif, verni ou laqué", "Bois massif laqué")),
                   ("Poutre", *tech_massif("Bois massif, verni ou laqué", "Bois massif laqué")),
                   ("Piètement", "2,80 m : 2 piètements ; 10 pieds : 3 piètements ; 12 pieds : 4 piètements",
                    "2,80 m : 2 piètements ; 10 pieds : 3 piètements ; 12 pieds : 4 piètements",
                    "2,80 m : 2 piètements ; 10 pieds : 3 piètements ; 12 pieds : 4 piètements")]
    out.append(f)

    f = Fiche("COMPÉTITION", J, {}, "Érable sycomore massif", table=False)
    f.modeles = {"Compétition": prix_modele(J, {"2,10 m": 7500, "2,30 m": 7500, "2,40 m": 9000, "2,60 m": 9500,
                                                "2,80 m": 11500, "10 pieds": 18000, "12 pieds": 20000})}
    f.options = (jeux_mixte(f, TG, True)
                 # Correction 25/11 : finitions 2,60 et 2,80 m alignées sur le français (1 280 / 1 380 €).
                 + essences(f, TG, [1200, 1350, 1500, 1650], [1200, 1350, 1500, 1650], SD, grands=(2000, 2300))
                 + finitions(f, TG, [1000, 1120, 1280, 1380], [1000, 1120, 1280, 1380], [300, 400, 500, 600],
                             base_chene=False)
                 + teinte(f, TG) + [laque(f, TG, [2100, 2200, 2300, 2400], grands=(2540, 2760))]
                 + communs(f, TG, jeu2=[860, 920, 990, 1060], cuir=480, pietement=INC, elasthanne=IMP)
                 + grands(f, TG, six_pieds={"2,60 m": 1370, "2,80 m": INC, "doc": True},
                          retour=[1220, 1320, 1420, 1520]))
    f.technique = [("Mention", "Billard 100 % bois massif", "", ""),
                   ("Cadre", *tech_massif("Érable sycomore massif", "MDF")),
                   ("Pieds", *tech_massif("Érable sycomore massif", "Érable massif")),
                   ("Traverses", *tech_massif("Érable sycomore massif", "Érable massif")),
                   ("Piètement", "2,80 m : 6 pieds", "2,80 m : 6 pieds", "2,80 m : 6 pieds")]
    out.append(f)

    f = Fiche("RUSTIC · CASTEL", J, {}, "Érable sycomore massif")
    prix = {"2,10 m": 6550, "2,30 m": 7250, "2,40 m": 8750, "2,60 m": 9250}
    f.modeles = {"Rustic": prix_modele(J, prix), "Castel": prix_modele(J, prix)}
    f.options = (jeux_mixte(f, T, False)
                 + essences(f, T, [900, 1000, 1100], [900, 1000, 1100], SD, meleze_pour="Rustic")
                 + finitions(f, T, [900, 1000, 1100], [900, 1000, 1100], [300, 400, 500], base_chene=False)
                 + teinte(f, T) + [laque(f, T, [1800, 1900, 2000], conditions="sur érable sycomore uniquement")]
                 + communs(f, T, jeu2=[860, 920, 990], cuir=480, liseré_doc=False))
    f.technique = [("Mention", "Billard 100 % bois massif", "", ""),
                   ("Cadre", *tech_massif("Érable sycomore massif", "Érable massif laqué")),
                   ("Pieds", *tech_massif("Érable sycomore massif", "Érable massif laqué")),
                   ("Traverses", *tech_massif("Érable sycomore massif", "Érable massif laqué"))]
    out.append(f)

    f = Fiche("LOUIS-PHILIPPE · MANOIR", J, {}, "Érable sycomore massif")
    f.modeles = {"Louis-Philippe": prix_modele(J, prix), "Manoir": prix_modele(J, prix)}
    f.options = (jeux_mixte(f, T, False)
                 + essences(f, T, [900, 1000, 1100], IMP, SD)
                 + finitions(f, T, [900, 1000, 1100], [900, 1000, 1100], [300, 400, 500], base_chene=False)
                 + teinte(f, T) + [laque(f, T, [1800, 1900, 2000], conditions="sur érable sycomore uniquement")]
                 + communs(f, T, jeu2=[860, 920, 990], cuir=480))
    f.technique = [("Mention", "Billard 100 % bois massif", "", ""),
                   ("Cadre", *tech_massif("Érable sycomore massif", "Érable massif laqué")),
                   ("Pieds", *tech_massif("Érable sycomore massif", "Érable massif laqué")),
                   ("Traverses", *tech_massif("Érable sycomore massif", "Érable massif laqué"))]
    out.append(f)

    for nom, prix, princ, inserts in (("HARMONIE NOYER", {"2,10 m": 9900, "2,30 m": 10600}, "Noyer", "d'érable"),
                                      ("HARMONIE ÉRABLE", {"2,10 m": 7590, "2,30 m": 8290}, "Érable", "de noyer")):
        f = Fiche(nom, J, {}, f"{princ} massif, incrustations {inserts} massif, poches en cuir noir")
        f.modeles = {nom.title().replace("Érable", "Érable"): prix_modele(J, prix)}
        f.options = (jeux_mixte(f, T2, False)
                     + [Option("Finition", BICOLORE, colonnes(J, T2, [IMP], IMP)),
                        Option("Teinte", TEINTE_INCLUSE, colonnes(J, T2, [INC], INC), choix="Un seul par groupe"),
                        Option("Teinte", TEINTE_SPECIALE, colonnes(J, T2, [IMP], IMP), choix="Un seul par groupe"),
                        Option("Laque", LAQUE, colonnes(J, T2, [IMP], IMP), note="Les Harmonie ne sont jamais laquées")]
                     + communs(f, T2, liseré=None, jeu2=[860], cuir=INC, elasthanne=IMP))
        f.technique = [("Mention", "Billard 100 % bois massif", "", ""),
                       ("Cadre", f"{princ} massif", "", ""), ("Pieds", f"{princ} massif", "", ""),
                       ("Traverses", f"{princ} massif", "", ""), ("Décor", f"Incrustations {inserts} massif", "", "")]
        out.append(f)

    f = Fiche("CHAMBORD", J, {}, "Érable sycomore massif", table=False)
    f.modeles = {"Chambord": prix_modele(J, {"2,10 m": 8700, "2,30 m": 8700, "2,40 m": 10700, "2,60 m": 11700,
                                             "2,80 m": 13700, "10 pieds": 21000, "12 pieds": 24000})}
    f.options = (jeux_mixte(f, TG, True)
                 # Correction 25/11 : chêne 2,40–2,80 m aligné sur le français (1 440 / 1 660 / 1 870 €).
                 + essences(f, TG, [1220, 1440, 1660, 1870], IMP, [4400, 4800, 5200, 5600], grands=(2000, 2300))
                 + finitions(f, TG, [1000, 1120, 1240, 1360], [1000, 1120, 1240, 1360], [300, 400, 500, 600],
                             base_chene=False)
                 + teinte(f, TG) + [laque(f, TG, [2100, 2200, 2300, 2400], grands=(2540, 2760),
                                          conditions="sur érable uniquement")]
                 + communs(f, TG, jeu2=[860, 920, 990, 1060], cuir=480, pietement=INC)
                 + grands(f, TG, six_pieds={"2,60 m": 1800, "2,80 m": INC, "doc": True},
                          retour=[1220, 1320, 1420, 1520]))
    f.technique = [("Mention", "Billard 100 % bois massif", "", ""),
                   ("Cadre", *tech_massif("Érable sycomore massif", "Érable massif laqué")),
                   ("Pieds", *tech_massif("Érable sycomore massif", "Érable massif laqué")),
                   ("Traverses", *tech_massif("Érable sycomore massif", "Érable massif laqué")),
                   ("Piètement", "2,80 m : 6 pieds", "2,80 m : 6 pieds", "2,80 m : 6 pieds")]
    out.append(f)
    return retouches_26_11(out)


# --- Billard français à bandes fixes (document « Billards français Lafuge », TTC) -----------------------------

def fiches_francais():
    J = "français"
    out = []
    T23, T234 = ["2,30 m"], ["2,30 m", "2,40 m"]
    T5 = ["2,30 m", "2,40 m", "2,60 m", "2,80 m", "3,10 m"]

    f = Fiche("LOFT · ÉLÉGANCE", J, {}, "Érable sycomore massif")
    # Correction 25/11 : HT 2,30 m = 3 115 € (document HT : 3 160 €).
    prix = {"2,30 m": 6230, "2,40 m": 7770}
    f.modeles = {"Loft": prix_modele(J, prix), "Élégance": prix_modele(J, prix)}
    # Correction 25/11 : essences et finitions 2,40 m à 820 € (document : 810 €), comme le pool.
    f.options = (essences(f, T234, [700, 820], [700, 820], SD)
                 + finitions(f, T234, [700, 820], [700, 820], [300, 400], base_chene=False)
                 + teinte(f, T234) + [laque(f, T234, [1600, 1700])]
                 + communs(f, T234, a37="doc", chauffage=[IMP, 1800]))
    f.technique = [("Mention", "Billard 100 % bois massif", "", ""),
                   ("Châssis", "Bois, renforcé en 2,40 m", "Bois, renforcé en 2,40 m", "Bois massif, renforcé en 2,40 m"),
                   ("Cadre", *tech_massif("Érable sycomore massif", "MDF")),
                   ("Pieds", *tech_massif("Érable sycomore massif", "MDF")),
                   ("Traverses", *tech_massif("Érable sycomore massif", "Érable massif"))]
    out.append(f)

    f = Fiche("SOHO", J, {}, "MDF plaqué chêne")
    f.modeles = {"Soho": prix_modele(J, {"2,30 m": 6130, "2,40 m": 7670})}
    f.options = (essences(f, T234, [1330, 1440], [1330, 1440], None, base_chene=True)
                 + finitions(f, T234, [700, 810], [700, 810], [300, 400], base_chene=True)
                 + teinte(f, T234) + [laque(f, T234, [1600, 1700]),
                                      Option("Liseré", LISERE_ALU, colonnes(J, T234, [900, 900]), doc=LISERE_ALU,
                                             conditions="Liseré aluminium, ou bois gainé du drap du billard (rappel de couleur)")]
                 + communs(f, T234, a37="doc", chauffage=[IMP, 1800]))
    f.technique = [("Châssis", "Bois", "Bois", "Bois massif"),
                   ("Cadre", *tech_massif("MDF plaqué chêne", "MDF")),
                   ("Pieds", *tech_massif("MDF plaqué chêne", "MDF")),
                   ("Traverses", *tech_massif("Chêne massif", "Érable massif"))]
    out.append(f)

    T4 = ["2,30 m", "2,40 m", "2,60 m", "2,80 m", "3,10 m"]
    f = Fiche("ARCADE", J, {}, "MDF plaqué chêne, plots inox")
    f.modeles = {"Arcade": prix_modele(J, {"2,30 m": 7000, "2,40 m": 10500, "2,60 m": 11700, "2,80 m": 16700,
                                           "3,10 m": SD})}
    f.options = (essences(f, T4, [1820, 1940, 2060, 2180, SD], [1820, 1940, 2060, 2180, SD], None, base_chene=True)
                 + finitions(f, T4, [900, 950, 1000, 1050, SD], [900, 950, 1000, 1050, SD], [300, 400, 500, 600, SD],
                             base_chene=True)
                 + teinte(f, T4) + [laque(f, T4, [1700, 1800, 1900, 2000, SD]),
                                    Option("Liseré", LISERE_ALU, colonnes(J, T4, [880, 900, 920, 940, SD]),
                                           doc=LISERE_ALU,
                                           conditions="Liseré aluminium, ou bois gainé du drap du billard (rappel de couleur)"),
                                    Option("Modèle", PLOTS, colonnes(J, T4, [470, 470, 470, 470, SD]), detail=TXT_PLOTS,
                                           doc=PLOTS)]
                 + communs(f, T4, a37="doc", chauffage=[IMP, 1800, 1900, 2000, SD], pietement=IMP))
    for o in f.options:
        if o.nom in (LISERE, REPERES, CADRE_DEM):
            o.prix["3,10 m"] = SD
    chassis = ("2,30 m : " + ACIER_60_40 + " ; 2,40 m : acier UPN de 80 mm ; 2,60 m : acier UPN de 100 mm ; "
               "2,80 m : acier UPN de 100 mm, 4 pieds ; 3,10 m : acier UPN de 80 mm, 6 pieds")
    f.technique = [("Châssis", chassis, chassis, chassis),
                   ("Cadre", *tech_massif("MDF plaqué chêne", "MDF")),
                   ("Pieds", *tech_massif("MDF plaqué chêne", "MDF")),
                   ("Poutre", *tech_massif("MDF plaqué chêne", "MDF")),
                   ("Piètement", "2,60 m : 2 arches ; 2,80 m : 3 arches", "2,60 m : 2 arches ; 2,80 m : 3 arches",
                    "2,60 m : 2 arches ; 2,80 m : 3 arches")]
    out.append(f)

    f = Fiche("TROCADÉRO", J, {}, "MDF plaqué chêne, pieds métalliques")
    f.modeles = {"Trocadéro": prix_modele(J, {"2,30 m": 7500})}
    f.options = (essences(f, T23, [1220], [1220], None, base_chene=True)
                 + finitions(f, T23, [760], [760], [300], base_chene=True)
                 + teinte(f, T23) + [laque(f, T23, [1100]),
                                     Option("Liseré", LISERE_ALU, colonnes(J, T23, [880]), doc=LISERE_ALU,
                                            conditions="Liseré aluminium, ou bois gainé du drap du billard (rappel de couleur)")]
                 + communs(f, T23, a37=True, pietement=IMP))
    f.technique = [("Châssis", ACIER_60_40, ACIER_60_40, ACIER_60_40),
                   ("Cadre", *tech_massif("MDF plaqué chêne", "MDF")),
                   ("Pieds", "Métalliques laqués mat structuré", "Métalliques laqués mat structuré",
                    "Métalliques laqués mat structuré"),
                   ("Traverse", *tech_massif("Bois massif verni", "Bois massif laqué"))]
    out.append(f)

    f = Fiche("MONT BLANC", J, {}, "MDF plaqué chêne, pieds en bois massif")
    f.modeles = {"Mont Blanc": prix_modele(J, {"2,30 m": 7400, "2,40 m": 10900, "2,60 m": 12100, "2,80 m": 17100,
                                               "3,10 m": SD})}
    # Mont Blanc 2,80 m : options laissées vides, l'utilisateur les saisira (25/11). 3,10 m : « nous consulter ».
    v = lambda a, b, c: [a, b, c, None, SD]  # noqa: E731
    f.options = (essences(f, T4, v(1220, 1440, 1660), v(1220, 1440, 1660), None, base_chene=True)
                 # Correction 25/11 : HT parchemin et brossée = 450 / 475 / 500 € (document HT : 450 / 470 / 490 €).
                 + finitions(f, T4, v(900, 950, 1000), v(900, 950, 1000), v(300, 400, 500), base_chene=True)
                 + teinte(f, T4) + [laque(f, T4, v(2100, 2200, 2300)),
                                    # Correction 25/11 : 880 / 920 / 960 € (document TTC : 880 / 880 / 880 €).
                                    Option("Liseré", LISERE_ALU, colonnes(J, T4, v(880, 920, 960)), doc=LISERE_ALU,
                                           conditions="Liseré aluminium, ou bois gainé du drap du billard (rappel de couleur)")]
                 + communs(f, T4, a37="doc", chauffage=[IMP, 1800, 1900, None, SD], pietement=IMP))
    for o in f.options:
        if o.nom in (LISERE, REPERES, CADRE_DEM):
            o.prix["2,80 m"], o.prix["3,10 m"] = None, SD
    chassis = ("2,30 m : " + ACIER_60_40 + " ; 2,40 m : acier UPN de 80 mm ; 2,60 m : acier UPN de 100 mm ; "
               "2,80 et 3,10 m : acier UPN de 80 mm, 6 pieds")
    f.technique = [("Châssis", chassis, chassis, chassis),
                   ("Cadre", *tech_massif("MDF plaqué chêne", "MDF")),
                   ("Pieds", *tech_massif("Bois massif, verni ou laqué", "Bois massif laqué")),
                   ("Traverses", *tech_massif("Bois massif, verni ou laqué", "Bois massif laqué")),
                   ("Piètement", "2,60 m : 2 piètements ; 2,80 m : 3 piètements",
                    "2,60 m : 2 piètements ; 2,80 m : 3 piètements", "2,60 m : 2 piètements ; 2,80 m : 3 piètements")]
    out.append(f)

    f = Fiche("CITY · ÉOS", J, {}, "MDF plaqué chêne")
    f.modeles = {"City": prix_modele(J, {"2,30 m": 5900}), "Éos": prix_modele(J, {"2,30 m": 5800})}
    f.options = (essences(f, T23, [1320], [1320], None, base_chene=True)
                 + finitions(f, T23, [700], [700], [300], base_chene=True)
                 + teinte(f, T23) + [laque(f, T23, [1500]),
                                     Option("Liseré", LISERE_ALU, colonnes(J, T23, [650]), doc=LISERE_ALU,
                                            conditions="Liseré aluminium, ou bois gainé du drap du billard (rappel de couleur)")]
                 + communs(f, T23, a37=True, cadre_doc=False, pietement=IMP))
    f.technique = [("Châssis", ACIER_60_60, ACIER_60_60, ACIER_60_60),
                   ("Cadre", *tech_massif("MDF plaqué chêne", "MDF")),
                   ("Pieds", *tech_massif("MDF plaqué chêne, 120 × 120 mm", "MDF")),
                   ("Traverses", *tech_massif("Multiplis 40 mm plaqué chêne (plus résistant que le bois massif)",
                                              "Érable massif")),
                   ("Forme des pieds (City)", "Biseautés", "Biseautés", "Biseautés")]
    out.append(f)

    f = Fiche("EIFFEL · ALPHA", J, {}, "MDF plaqué chêne, pieds en acier")
    f.modeles = {"Eiffel": prix_modele(J, {"2,30 m": 6500}), "Alpha": prix_modele(J, {"2,30 m": 6500})}
    f.options = (essences(f, T23, [1000], [1000], [4000], base_chene=True)
                 + finitions(f, T23, [620], [620], [300], base_chene=True)
                 + teinte(f, T23) + [laque(f, T23, [1100]),
                                     Option("Liseré", LISERE_ALU, colonnes(J, T23, [660]), doc=LISERE_ALU,
                                            conditions="Liseré aluminium, ou bois gainé du drap du billard (rappel de couleur)")]
                 + communs(f, T23, a37=True, cadre_doc=False, pietement=IMP))
    acier = "Acier laqué au RAL choisi par le client"
    f.technique = [("Châssis", ACIER_60_60, ACIER_60_60, ACIER_60_60),
                   ("Cadre", *tech_massif("MDF plaqué chêne", "MDF")),
                   ("Pieds", acier, acier, acier),
                   ("Traverses", *tech_massif("Multiplis 40 mm plaqué chêne (plus résistant que le bois massif)",
                                              "Érable massif"))]
    out.append(f)

    f = Fiche("BEAUBOURG", J, {}, "MDF plaqué chêne ou érable, pieds et traverses en acier finition mat fine texture")
    f.modeles = {"Beaubourg": prix_modele(J, {"2,30 m": 6670})}
    f.options = ([Option("Essence", "Cadre en mélèze massif", colonnes(J, T23, [740]), exclut="Laque du cadre",
                         choix="Un seul par groupe", doc=MELEZE),
                  Option("Essence", "Cadre en chêne massif", colonnes(J, T23, [740]), exclut="Laque du cadre",
                         choix="Un seul par groupe", doc=CHENE),
                  Option("Finition", BROSSEE, colonnes(J, T23, [410]), exclut="Laque du cadre ; Cadre en mélèze massif",
                         conditions="Sur chêne uniquement", doc=BROSSEE),
                  Option("Finition", PARCHEMIN, colonnes(J, T23, [410]),
                         exclut="Laque du cadre ; Cadre en mélèze massif", conditions="Sur chêne uniquement",
                         doc=PARCHEMIN),
                  Option("Finition", BICOLORE, colonnes(J, T23, [IMP], IMP), note="Déjà bicolore (bois et métal)")]
                 + teinte(f, T23)
                 + [Option("Laque", "Laque du cadre", colonnes(J, T23, [740]),
                           exclut=f"Cadre en mélèze massif ; Cadre en chêne massif ; {REPERES} ; {TEINTE_SPECIALE} ; "
                                  f"{PARCHEMIN} ; {BROSSEE}",
                           conditions="Seul le liseré de couleur reste possible", doc=LAQUE)]
                 + communs(f, T23, a37=True, cadre_doc=False, pietement=IMP, liseré_doc=False))
    renommer_laque(f)
    # Correction 25/11 : fiche technique reprise du pool (le document français copiait celle de City).
    f.technique = [("Châssis", ACIER_60_60, ACIER_60_60, ACIER_60_60),
                   ("Cadre", *tech_massif("MDF plaqué chêne", "MDF")),  # 26/11 : érable = option « Placage érable »
                   ("Pieds", acier, acier, acier),
                   ("Traverses", "Multiplis 40 mm habillé d'une équerre en acier laqué",
                    "Multiplis 40 mm habillé d'une équerre en acier laqué",
                    "Multiplis 40 mm habillé d'une équerre en acier laqué")]
    out.append(f)

    f = Fiche("COMPÉTITION", J, {}, "Érable sycomore massif", table=False)
    f.modeles = {"Compétition": prix_modele(J, {"2,30 m": 7500, "2,40 m": 10000, "2,60 m": 11000, "2,80 m": 14500,
                                                "3,10 m": 16500})}
    # Corrections 25/11 : mélèze et chêne alignés sur le pool (1 200 / 1 350 / 1 500 / 1 650 €), 3,10 m inchangé.
    f.options = (essences(f, T5, [1200, 1350, 1500, 1650, 1860], [1200, 1350, 1500, 1650, 1860], SD)
                 + finitions(f, T5, [1000, 1120, 1280, 1380, 1500], [1000, 1120, 1280, 1380, 1500],
                             [300, 400, 500, 600, 700], base_chene=False)
                 + teinte(f, T5) + [laque(f, T5, [2100, 2200, 2300, 2400, 2500])]
                 + communs(f, T5, a37="doc", chauffage=[IMP, 1800, 1900, 2000, 2100], pietement=INC)
                 + [Option("Modèle", SIX_PIEDS, {"2,30 m": IMP, "2,40 m": IMP, "2,60 m": 1370, "2,80 m": INC,
                                                 "3,10 m": INC}, doc=SIX_PIEDS)])
    chassis = ("2,30 m : bois massif ; 2,40 m : bois massif renforcé ; 2,60 m : acier UPN de 100 mm ; "
               "2,80 et 3,10 m : acier UPN de 80 mm, 6 pieds")
    f.technique = [("Mention", "Billard 100 % bois massif", "", ""),
                   ("Châssis", chassis, chassis, chassis),
                   ("Cadre", *tech_massif("Érable sycomore massif", "MDF")),
                   ("Pieds", *tech_massif("Érable sycomore massif", "Érable massif")),
                   ("Traverses", *tech_massif("Érable sycomore massif", "Érable massif")),
                   ("Dimensions", "2,80 m : demi-match ; 3,10 m : match", "2,80 m : demi-match ; 3,10 m : match",
                    "2,80 m : demi-match ; 3,10 m : match")]
    out.append(f)

    f = Fiche("RUSTIC · CASTEL", J, {}, "Érable sycomore massif")
    prix = {"2,30 m": 7270, "2,40 m": 8820}
    f.modeles = {"Rustic": prix_modele(J, prix), "Castel": prix_modele(J, prix)}
    # Correction 25/11 : 2,30 m à 900 € (document : 880 €), comme le pool. Piètement démontable ajouté (+410 €).
    f.options = (essences(f, T234, [900, 1000], [900, 1000], SD, meleze_pour="Rustic")
                 + finitions(f, T234, [900, 1000], [900, 1000], [300, 400], base_chene=False)
                 + teinte(f, T234) + [laque(f, T234, [1800, 1900], conditions="sur érable sycomore uniquement")]
                 + communs(f, T234, a37="doc", chauffage=[IMP, 1800], liseré_doc=False, pietement_doc=False))
    f.technique = [("Mention", "Billard 100 % bois massif", "", ""),
                   ("Châssis", "Bois massif, renforcé en 2,40 m", "Bois massif, renforcé en 2,40 m",
                    "Bois massif, renforcé en 2,40 m"),
                   ("Cadre", *tech_massif("Érable sycomore massif", "Érable massif laqué")),
                   ("Pieds", *tech_massif("Érable sycomore massif", "Érable massif laqué")),
                   ("Traverses", *tech_massif("Érable sycomore massif", "Érable massif laqué"))]
    out.append(f)

    f = Fiche("LOUIS-PHILIPPE · MANOIR", J, {}, "Érable sycomore massif")
    f.modeles = {"Louis-Philippe": prix_modele(J, prix), "Manoir": prix_modele(J, prix)}
    # Corrections 25/11 : 2,30 m à 900 € (document : 880 €) ; brossée 2,40 m à 1 000 € (document : 950 €).
    f.options = (essences(f, T234, [900, 1000], IMP, SD)
                 + finitions(f, T234, [900, 1000], [900, 1000], [300, 400], base_chene=False)
                 + teinte(f, T234) + [laque(f, T234, [1800, 1900], conditions="sur érable sycomore uniquement")]
                 + communs(f, T234, a37="doc", chauffage=[IMP, 1800]))
    f.technique = [("Mention", "Billard 100 % bois massif", "", ""),
                   ("Châssis", "Bois massif, renforcé en 2,40 m", "Bois massif, renforcé en 2,40 m",
                    "Bois massif, renforcé en 2,40 m"),
                   ("Cadre", *tech_massif("Érable sycomore massif", "Érable massif laqué")),
                   ("Pieds", *tech_massif("Érable sycomore massif", "Érable massif laqué")),
                   ("Traverses", *tech_massif("Érable sycomore massif", "Érable massif laqué"))]
    out.append(f)

    for nom, prix, princ, inserts in (("HARMONIE NOYER", {"2,30 m": 10600}, "Noyer", "d'érable"),
                                      ("HARMONIE ÉRABLE", {"2,30 m": 8250}, "Érable", "de noyer")):
        f = Fiche(nom, J, {}, f"{princ} massif, incrustations {inserts} massif")
        f.modeles = {nom.title(): prix_modele(J, prix)}
        f.options = ([Option("Finition", BICOLORE, colonnes(J, T23, [IMP], IMP)),
                      Option("Teinte", TEINTE_INCLUSE, colonnes(J, T23, [INC], INC), choix="Un seul par groupe"),
                      Option("Teinte", TEINTE_SPECIALE, colonnes(J, T23, [IMP], IMP), choix="Un seul par groupe"),
                      Option("Laque", LAQUE, colonnes(J, T23, [IMP], IMP), note="Les Harmonie ne sont jamais laquées")]
                     # Piètement démontable ajouté comme le pool (point interprété n° 3, validé le 25/11).
                     + communs(f, T23, liseré=None, a37=True, pietement_doc=False))
        f.technique = [("Mention", "Billard 100 % bois massif", "", ""),
                       ("Châssis", ACIER_60_60, "", ""),
                       ("Cadre", f"{princ} massif", "", ""), ("Pieds", f"{princ} massif", "", ""),
                       ("Traverses", f"{princ} massif", "", ""), ("Décor", f"Incrustations {inserts} massif", "", "")]
        out.append(f)

    f = Fiche("CHAMBORD", J, {}, "Érable sycomore massif", table=False)
    f.modeles = {"Chambord": prix_modele(J, {"2,30 m": 8800, "2,40 m": 11300, "2,60 m": 12300, "2,80 m": 15800,
                                             "3,10 m": 17800})}
    # Corrections 25/11 : finitions 2,40–2,80 m alignées sur le pool (1 120 / 1 240 / 1 360 €) ;
    # noyer 2,60 et 2,80 m à 5 200 / 5 600 € (document : 5 160 / 5 550 €).
    f.options = (essences(f, T5, [1220, 1440, 1660, 1870, 2080], IMP, [4400, 4800, 5200, 5600, 5920])
                 + finitions(f, T5, [1000, 1120, 1240, 1360, 1430], [1000, 1120, 1240, 1360, 1430],
                             [300, 400, 500, 600, 700], base_chene=False)
                 + teinte(f, T5) + [laque(f, T5, [2100, 2200, 2300, 2400, 2500], conditions="sur érable uniquement")]
                 + communs(f, T5, a37="doc", chauffage=[IMP, 1800, 1900, 2000, 2100], pietement=INC)
                 # Mention « si châssis bois donc démontable » retirée : les châssis bois et UPN sont démontables.
                 + [Option("Modèle", SIX_PIEDS, {"2,30 m": IMP, "2,40 m": IMP, "2,60 m": 1800, "2,80 m": INC,
                                                 "3,10 m": INC}, doc=SIX_PIEDS)])
    chassis = ("2,30 m : bois massif ; 2,40 m : bois massif renforcé ; 2,60 m : acier UPN de 100 mm ; "
               "2,80 et 3,10 m : acier UPN de 80 mm, 6 pieds")
    f.technique = [("Mention", "Billard 100 % bois massif", "", ""),
                   ("Châssis", chassis, chassis, chassis),
                   ("Cadre", *tech_massif("Érable sycomore massif", "Érable massif laqué")),
                   ("Pieds", *tech_massif("Érable sycomore massif", "Érable massif laqué")),
                   ("Traverses", *tech_massif("Érable sycomore massif", "Érable massif laqué")),
                   ("Dimensions", "2,80 m : demi-match ; 3,10 m : match", "2,80 m : demi-match ; 3,10 m : match",
                    "2,80 m : demi-match ; 3,10 m : match")]
    out.append(f)
    return retouches_26_11(out)


# --- Plateaux (identiques pour les deux jeux) -------------------------------------------------------------------

def plateaux(jeu):
    """Lignes : (groupe, plateau, prix par taille, conditions). 10 et 12 pieds, 3,10 m : sur demande."""
    t = TAILLES[jeu]

    def grille(v210_230, v240=IMP, v260=IMP, v280=IMP, grand=SD):
        d = {"2,10 m": v210_230, "2,30 m": v210_230, "2,40 m": v240, "2,60 m": v260, "2,80 m": v280,
             "3,10 m": grand, "10 pieds": grand, "12 pieds": grand}
        return {k: d[k] for k in t}

    encastre = "Creusé à l'endroit des poches, il s'emboîte dans le cadre et ne fait plus qu'un avec le billard."
    un, plus = "Un seul par groupe", "Plusieurs possibles"
    petites = "2,10 et 2,30 m uniquement" if jeu == "mixte" else "2,30 m uniquement"
    sup = "S'ajoute au prix d'un plateau encastré"
    enc = ("Plateau encastré, chêne ou érable ; Plateau encastré, finition parchemin, patine antiquaire, brossée ou "
           "cérusée ; Plateau encastré laqué ; Plateau encastré mélèze ; Plateau encastré noyer plaqué")
    # (groupe, plateau, prix par taille, conditions, détail imprimé, nécessite (l'un de), choix)
    return [
        ("Plateau", "Plateau simple, érable ou chêne, toutes teintes", grille(990, grand=IMP),
         "En 2 parties ; " + petites, "", "", un),
        ("Plateau", "Plateau encastré, chêne ou érable", grille(1190, 1600, 1770, 1960), "En 3 parties dès 2,40 m",
         encastre, "", un),
        ("Plateau", "Plateau encastré, finition parchemin, patine antiquaire, brossée ou cérusée",
         grille(1620, 2140, 2320, 2700), "En 3 parties dès 2,40 m", encastre, "", un),
        ("Plateau", "Plateau encastré laqué", grille(1720, 2250, 2420, 2810), "En 3 parties dès 2,40 m", encastre, "", un),
        ("Plateau", "Plateau encastré mélèze", grille(1900, 2300, 2500, 2900), "En 3 parties dès 2,40 m", encastre, "",
         un),
        ("Plateau", "Plateau encastré noyer plaqué", grille(2540, grand=IMP), petites[0].upper() + petites[1:], encastre, "",
         un),
        ("Plateau", "Dessus 100 % verre", {**grille(1160, grand=IMP), **({"2,30 m": 1260} if "2,30 m" in t else {})},
         "Non encastré" + (" ; 2,10 m : 1 160 €, 2,30 m : 1 260 €" if jeu == "mixte" else ""), "", "", un),
        ("Parties", "Plateau en 3 parties", grille(420, INC, INC, INC), "De série dès 2,40 m", "", "", plus),
        ("Supplément verre", "Verre Sécurit 8 mm transparent et bois", grille(1400, grand=IMP), sup, "", enc, un),
        ("Supplément verre", "Verre Sécurit 8 mm dépoli et bois", grille(1600, grand=IMP), sup, "", enc, un),
        ("Supplément verre", "Verre Sécurit 8 mm décor à carrés et bois", grille(2050, grand=IMP), sup, "", enc, un),
        ("Supplément verre", "Imitation céramique et bois (finition chêne)", grille(1200, grand=IMP), sup, "", enc, un),
        ("Rallonge", "Rallonge 50 cm, médium brut", grille(320, grand=IMP), "Jamais incluse ; avec tous les plateaux", "",
         "", un),
        ("Rallonge", "Rallonge 50 cm teintée", grille(470, grand=IMP), "Jamais incluse ; avec tous les plateaux", "", "",
         un),
        ("Rallonge", "Rallonge 50 cm laquée", grille(620, grand=IMP), "Jamais incluse ; avec tous les plateaux", "", "",
         un),
        ("Teinte", "Dessus en teinte spéciale", grille(250, 250, 250, 250), "Teinte hors nuancier", "", "", plus),
    ]


# --- Accessoires Lafuge (onglet Accessoires & mobilier) ---------------------------------------------------------

def accessoires():
    """(catégorie, article, détail, prix TTC)."""
    a = []
    for places, chene, noble, laq in ((4, 350, 560, 460), (6, 370, 620, 480), (8, 500, 700, 660)):
        a += [("Porte-queues Lafuge", f"Porte-queues Design {places} places, chêne ou mélèze", "Bois, finition chêne ou mélèze", chene),
              ("Porte-queues Lafuge", f"Porte-queues Design {places} places, noyer ou érable", "Bois, finition noyer ou érable", noble),
              ("Porte-queues Lafuge", f"Porte-queues Design {places} places laqué", "Laqué noir, blanc ou gris RAL 9006", laq)]
    a += [("Porte-queues Lafuge", "Option porte-queues Design : autre RAL", "Laque dans un autre RAL", 100),
          ("Porte-queues Lafuge", "Option porte-queues Design : aluminium", "Aluminium laqué mat fine texture", 160),
          ("Porte-queues Lafuge", "Porte-queues panoplie moderne 6 places, érable, chêne ou mélèze", "6 places", 1560),
          ("Porte-queues Lafuge", "Porte-queues panoplie moderne 6 places laqué", "6 places", 2150),
          ("Porte-queues Lafuge", "Porte-queues panoplie moderne 6 places noyer", "6 places", 3150),
          ("Porte-queues Lafuge", "Option panoplie : 8 places", "8 places au lieu de 6", 400)]
    for pos, vernis, laq, harm in ((4, 250, 360, 450), (6, 270, 380, 470), (8, 290, 400, 490)):
        a += [("Porte-queues Lafuge", f"Porte-queues standard {pos} positions verni", "Érable, mélèze ou chêne verni", vernis),
              ("Porte-queues Lafuge", f"Porte-queues standard {pos} positions laqué", "Laqué", laq),
              ("Porte-queues Lafuge", f"Porte-queues standard {pos} positions Harmonie", "Noyer et érable", harm)]
    a += [("Boulier Lafuge", "Boulier moderne chêne ou mélèze", "Chêne ou mélèze", 560),
          ("Boulier Lafuge", "Boulier moderne laqué", "Laqué", 710)]
    for long, prix, option in (("1,00 m", 750, 230), ("1,40 m", 850, 310), ("1,80 m", 1000, 390),
                               ("2,00 m", 1100, 440), ("2,20 m", 1200, 480)):
        a += [("Bancs Lafuge", f"Banc {long} chêne naturel", "Chêne naturel", prix),
              ("Bancs Lafuge", f"Banc {long} Harmonie", "Noyer et érable (prix du chêne × 2)", prix * 2),
              ("Bancs Lafuge", f"Option banc {long} : simili cuir ou liseré", "Simili cuir, ou liseré peint ou tissu", option)]
    a += [("Bancs Lafuge", "Option banc : laqué", "Banc laqué (non cumulable avec les pieds Eiffel)", 550),
          ("Bancs Lafuge", "Option banc : pieds métalliques Eiffel", "Chêne naturel et pieds Eiffel (non cumulable avec la laque)", 200),
          ("Rangement des plateaux", "Rangement des 2 plateaux en U, MDF brut et mousse noire", "Billards 2,10 et 2,30 m", 170),
          ("Rangement des plateaux", "Rangement des 2 plateaux en U, MDF teinté verni", "Billards 2,10 et 2,30 m", 270),
          ("Rangement des plateaux", "Rangement des 2 plateaux en U, MDF teinte blanche ou noire vernie", "Billards 2,10 et 2,30 m", 440),
          ("Rangement des plateaux", "Rangement des 2 plateaux en U, MDF laqué", "Billards 2,10 et 2,30 m", 600)]
    return a


def ht(valeur):
    """Prix revendeur HT = TTC ÷ 2 ; les cases non numériques restent telles quelles."""
    if isinstance(valeur, (int, float)):
        return valeur / 2 if valeur % 2 else valeur // 2
    return valeur


GAMME = {
    "Délai de fabrication": "8 semaines minimum, hors organisation de la livraison",
    "Accessoires": "Billard vendu hors accessoires",
    "Échéancier": "30 % à la commande, 30 % au lancement en fabrication, solde avant livraison",
}
DRAP = {"mixte": "Simonis 760 ou Strachan 777 inclus", "français": "Simonis 330 inclus"}

# Corrections des documents validées les 20 et 25/11 : (jeu, fiche, option, document, valeur des documents, valeur retenue).
# Valeurs = colonnes du document (mixte : 2,10–2,30 / 2,40 / 2,60 / 2,80 ; français : 2,30 / 2,40 / 2,60 / 2,80 / 3,10).
CORRECTIONS_TTC = [
    ("mixte", "COMPÉTITION", PARCHEMIN, [1000, 1120, 1240, 1360], [1000, 1120, 1280, 1380]),
    ("mixte", "COMPÉTITION", BROSSEE, [1000, 1120, 1240, 1360], [1000, 1120, 1280, 1380]),
    ("mixte", "CHAMBORD", CHENE, [1220, 1420, 1620, 1820], [1220, 1440, 1660, 1870]),
    ("français", "LOFT · ÉLÉGANCE", MELEZE, [700, 810], [700, 820]),
    ("français", "LOFT · ÉLÉGANCE", CHENE, [700, 810], [700, 820]),
    ("français", "LOFT · ÉLÉGANCE", PARCHEMIN, [700, 810], [700, 820]),
    ("français", "LOFT · ÉLÉGANCE", BROSSEE, [700, 810], [700, 820]),
    ("français", "MONT BLANC", LISERE_ALU, [880, 880, 880], [880, 920, 960]),
    ("français", "COMPÉTITION", MELEZE, [1150, 1320, 1490, 1660, 1860], [1200, 1350, 1500, 1650, 1860]),
    ("français", "COMPÉTITION", CHENE, [1150, 1320, 1490, 1660, 1860], [1200, 1350, 1500, 1650, 1860]),
    ("français", "RUSTIC · CASTEL", MELEZE, [880, 1000], [900, 1000]),
    ("français", "RUSTIC · CASTEL", CHENE, [880, 1000], [900, 1000]),
    ("français", "RUSTIC · CASTEL", PARCHEMIN, [880, 1000], [900, 1000]),
    ("français", "RUSTIC · CASTEL", BROSSEE, [880, 1000], [900, 1000]),
    ("français", "LOUIS-PHILIPPE · MANOIR", CHENE, [880, 1000], [900, 1000]),
    ("français", "LOUIS-PHILIPPE · MANOIR", PARCHEMIN, [880, 1000], [900, 1000]),
    ("français", "LOUIS-PHILIPPE · MANOIR", BROSSEE, [880, 950], [900, 1000]),
    ("français", "CHAMBORD", PARCHEMIN, [1000, 1100, 1200, 1350, 1430], [1000, 1120, 1240, 1360, 1430]),
    ("français", "CHAMBORD", BROSSEE, [1000, 1100, 1200, 1350, 1430], [1000, 1120, 1240, 1360, 1430]),
    ("français", "CHAMBORD", NOYER, [4400, 4800, 5160, 5550, 5920], [4400, 4800, 5200, 5600, 5920]),
]
# Écarts des documents HT (valeur HT des documents ≠ TTC retenu ÷ 2) acceptés : (jeu, fiche, option ou taille, HT document).
CORRECTIONS_HT = [
    ("français", "LOFT · ÉLÉGANCE", "prix 2,30 m", [3160]),
    ("français", "LOFT · ÉLÉGANCE", A37, [350]),
    ("français", "MONT BLANC", A37, [350]),
    ("français", "MONT BLANC", PARCHEMIN, [450, 470, 490]),
    ("français", "MONT BLANC", BROSSEE, [450, 470, 490]),
    ("mixte", "PLATEAUX", "Plateau encastré mélèze 2,40 m", [1300]),
]
