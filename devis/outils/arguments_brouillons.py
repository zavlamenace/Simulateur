"""Arguments de réassurance validés le 19/11/2026 (statut « À valider » jusqu'à relecture finale).

Une entrée : (Valable pour, Titre, Texte, photo prévue, proposé par défaut).
- « Valable pour » : « Tous » ou une version (« Pieds bois massif », « Pieds métalliques »).
- Photo prévue : la colonne Photo affiche « À fournir » en attendant la photo ultra zoomée.
- Proposé par défaut : point fort pré-coché dans l'outil (3 au maximum par gamme et par version, 27/11).
  La phrase d'accroche de la gamme se règle dans le bloc GAMME (paramètre « Accroche ») ; la ligne de
  positionnement reste ici comme argument au choix, non pré-coché.
Règles de rédaction : connaissances/arguments.md.
"""

PHOTO_A_FOURNIR = "À fournir"

DRAP = ("Tous", "Drap Simonis 760 ou Strachan 777 inclus",
        "Les draps des grandes compétitions internationales, en 26 couleurs, sans supplément.")
BANDES_INTERCHANGEABLES = ("Tous", "Bandes interchangeables brevetées",
                           "Plusieurs jeux sur un même billard : français, américain ou pool, à vous de choisir.")
BANDES_FRANCAISES = ("Tous", "Bandes en caoutchouc français", "Un rebond précis, calibré pour chaque jeu.")
CHASSIS = ("Tous", "Châssis bois massif renforcé", "Bois massif et renforts métalliques pour une stabilité maximale.")
BOITES = ("Tous", "6 boîtes insonorisées", "Les billes tombent sans bruit.")

ARGUMENTS = {
    "Référence": [
        # Titre et texte de l'ardoise modifiés par l'équipe dans le Sheet (relu le 27/11).
        ("Tous", "Le meilleur rapport qualité-prix du marché en 2,10m",
         "Ardoise monobloc, structure en bois massif et pack accessoires inclus.", False, False),
        ("Tous", "Ardoise monobloc de 19 mm",
         "Une pierre naturelle d'un seul tenant : elle ne gonfle pas et ne se déforme pas avec l'humidité, "
         "contrairement au MDF ou aggloméré. ", True, True),
        ("Tous", "Pack accessoires inclus, d'une valeur de 300 €",
         "16 billes, 4 queues, triangle, craies, brosse et porte-queue.", True, True),
        ("Pieds bois massif", "Pieds bois massif et Formica",
         "Le Formica, le matériau des plans de travail de cuisine : il résiste aux chocs, aux rayures et aux taches, "
         "là où le papier décor courant s'abîme.", True, True),
        ("Pieds métalliques", "Pieds métalliques de 5 mm",
         "Acier de 5 mm d'épaisseur, laqué époxy : une rigidité à toute épreuve.", True, True),
        CHASSIS + (True, False),
        BOITES + (True, False),
        ("Tous", "Vérins de réglage", "Une planéité parfaite, même sur un sol irrégulier.", True, False),
        ("Tous", "Bandes en caoutchouc toilé", "Un rebond vif et régulier.", True, False),
        ("Tous", "Billard convertible en table", "Avec le plateau en 2 parties, une table pour 8 à 10 personnes.",
         False, False),
    ],
    "Design": [
        ("Tous", "Le billard convertible en table, laqué et fabriqué à la main dans notre atelier du Gers",
         "Laque mate, satinée ou brillante, dans la couleur RAL de votre choix.", False, False),
        DRAP + (True, True),
        ("Tous", "Ardoise italienne monobloc de 19 mm",
         "Une pierre naturelle d'un seul tenant, dans un schiste italien réputé pour sa densité : elle ne se déforme "
         "pas avec l'humidité, contrairement au MDF.", True, True),
        BANDES_INTERCHANGEABLES + (True, True),
        BANDES_FRANCAISES + (True, False),
        CHASSIS + (True, False),
        ("Tous", "Pieds en hêtre massif", "Pieds carrés de 120 mm.", True, False),
        ("Tous", "Finition laquée à la main", "Mate, satinée ou brillante.", True, False),
        BOITES + (True, False),
        ("Tous", "Votre couleur", "Laque dans la couleur RAL de votre choix.", False, False),
    ],
    "Prestige": [
        ("Tous", "Le billard convertible en table le plus fonctionnel du marché",
         "Rangement intégré des accessoires et des plateaux, réception des billes centralisée et insonorisée, "
         "allonge incluse pour recevoir jusqu'à 12 convives.", False, False),
        ("Tous", "Bandes interchangeables brevetées",
         "Plusieurs jeux sur un même billard : vous passez d'un jeu à l'autre en changeant de bandes.", True, True),
        ("Tous", "Rangement intégré de tous les accessoires",
         "Le système Octopack range sous le billard les queues, les billes, les bandes, les craies et les plateaux.",
         True, True),
        ("Tous", "Réception centralisée et insonorisée",
         "Goulottes capitonnées en 3 épaisseurs, un tiroir abattant de chaque côté.", True, True),
        ("Tous", "12 couverts, allonge incluse",
         "Avec le plateau bois comme avec le plateau vitré, l'allonge de 45 cm est fournie.", False, False),
        ("Tous", "Châssis Woodstone",
         "Un bois haute densité aux fibres serrées : il absorbe le poids de l'ardoise sans fléchir et ne travaille "
         "ni avec l'humidité ni avec la température.", True, False),
        ("Tous", "Rangement des plateaux intégré", "Pendant la partie, les plateaux se rangent sous le billard.",
         True, False),
        ("Tous", "Ardoise italienne monobloc de 19 mm",
         "Une pierre naturelle d'un seul tenant, sur longerons métalliques : elle ne se déforme pas avec "
         "l'humidité, contrairement au MDF.", True, False),
        DRAP + (True, False),
        BANDES_FRANCAISES + (True, False),
        ("Tous", "Pieds en bois massif", "Chêne, hêtre ou tauari selon le modèle, teintés et vernis à la main.",
         True, False),
        ("Tous", "Fabriqué à la main dans le Gers",
         "Bois massif teinté et verni à la main dans notre atelier de Plaisance-du-Gers (Sud-Ouest).", False, False),
    ],
    "Lafuge": [
        ("Tous", "Le billard le plus personnalisable",
         "Essence, teinte, laque, taille, finitions, liserés : chaque détail est à votre choix.", False, False),
        ("Tous", "Une pièce unique, faite à la main",
         "Fabriquée à l'unité par un seul ébéniste, du début à la fin, à Miribel-les-Échelles.", False, True),
        ("Tous", "Essences nobles massives", "Érable, chêne, mélèze ou noyer massifs.", True, True),
        ("Tous", "Ils nous ont choisis",
         "Yacht Club de Monaco, Sheraton Paris, villas prestigieuses de la Côte d'Azur et de la côte atlantique.",
         False, True),
        ("Tous", "Ardoise italienne jusqu'à 45 mm",
         "Une pierre naturelle épaisse, qui garde sa planéité pendant des décennies.", True, False),
        BANDES_INTERCHANGEABLES + (True, False),
        ("Tous", "Toutes les dimensions", "Du 7 pieds au snooker 12 pieds, jusqu'au billard russe.", False, False),
    ],
    "Lafuge français": [
        ("Tous", "Le billard le plus personnalisable",
         "Essence, teinte, laque, taille, finitions, liserés : chaque détail est à votre choix.", False, False),
        ("Tous", "Une pièce unique, faite à la main",
         "Fabriquée à l'unité par un seul ébéniste, du début à la fin, à Miribel-les-Échelles.", False, True),
        ("Tous", "Essences nobles massives", "Érable, chêne, mélèze ou noyer massifs.", True, True),
        ("Tous", "Ils nous ont choisis",
         "Yacht Club de Monaco, Sheraton Paris, villas prestigieuses de la Côte d'Azur et de la côte atlantique.",
         False, True),
        ("Tous", "Ardoise italienne jusqu'à 50 mm",
         "Une pierre naturelle épaisse, qui garde sa planéité pendant des décennies.", True, False),
        ("Tous", "Bandes A37 toilées incluses dès 2,60 m",
         "Le caoutchouc A37 toilé, la référence haut de gamme du billard français.", True, False),
        ("Tous", "Chauffage de l'ardoise", "Proposé dès 2,40 m, pour un drap sec et une bille qui roule régulièrement.",
         False, False),
        ("Tous", "Toutes les dimensions", "De 2,30 m jusqu'au billard de match de 3,10 m.", False, False),
    ],
}


def lignes(gamme):
    """Lignes du bloc : Ordre, Valable pour, Titre, Texte, Photo, Statut, Proposé par défaut."""
    return [
        [i, v, t, x, PHOTO_A_FOURNIR if photo else "", "À valider", "Oui" if defaut else "Non"]
        for i, (v, t, x, photo, defaut) in enumerate(ARGUMENTS[gamme], start=1)
    ]


# Arguments liés aux choix (bloc « ARGUMENTS DES CHOIX » de « Lafuge contenus »), brouillons du 26/11.
# Imprimés sous la ligne de l'option seulement quand l'équipe passe leur statut à « Actif ».
FR_26 = "Origine confirmée par la direction (26/11)"
SIMONIS = "Drap Iwan Simonis : la manufacture belge tisse des draps depuis 1680 et habille les grands championnats."
BANDES_FR = "Bandes en caoutchouc fabriqué en France, calibrées pour ce jeu."
LAQUE_TXT = "Laqué à la main dans notre cabine de finition, dans la couleur RAL de votre choix."
CHOIX_LAFUGE = [
    ["Érable sycomore massif", "Érable sycomore massif français : un bois clair, dense et homogène, recherché des ébénistes et des luthiers.",
     FR_26 + " ; Futura-Sciences, fiche CIRAD", "À valider"],
    ["Chêne massif", "Chêne massif français : un bois dense et durable, au veinage marqué, qui se patine avec le temps.",
     FR_26 + " ; IGN : les chênes, 44 % du volume des feuillus français", "À valider"],
    ["Noyer massif", "Noyer massif français : le bois des pièces d'exception, sombre et profond.", FR_26, "À valider"],
    ["Érable massif", "Érable massif français : un bois clair, dense et homogène.", FR_26, "À valider"],
    ["Mélèze massif", "Mélèze massif : un bois de montagne au veinage chaleureux.", "Origine non précisée", "À valider"],
    ["Simonis 760", SIMONIS, "iwansimonis.com (sources du fabricant)", "À valider"],
    ["Simonis 330", SIMONIS, "iwansimonis.com (sources du fabricant)", "À valider"],
    ["Strachan 777", "Drap Strachan : la maison anglaise dont les draps équipent le championnat du monde de snooker depuis 1980.",
     "WSP Textiles, Intergame (sources du fabricant)", "À valider"],
    ["Bandes initiales américaines", BANDES_FR, "Confirmé par la direction (26/11)", "À valider"],
    ["Bandes initiales anglaises", BANDES_FR, "Confirmé par la direction (26/11)", "À valider"],
    ["Bandes initiales françaises", BANDES_FR, "Confirmé par la direction (26/11)", "À valider"],
    ["2e jeu de bandes interchangeables",
     "Grâce au système breveté de bandes interchangeables, inclus, vous changez de jeu en quelques minutes, sans outil.",
     "Brevet déposé en 2000 (billardsdefrance.fr, Brevets et innovations)", "À valider"],
    ["Bandes A37 toilées", "Bandes A37 toilées : un caoutchouc de qualité compétition, pour un rebond vif et constant.",
     "Artemis A37 (fabriqué en Allemagne) ; le détail de l'option dans les fiches est prioritaire", "À valider"],
    ["Chauffage de l'ardoise",
     "L'ardoise chauffée garde le drap parfaitement sec : la bille roule plus vite et plus régulièrement.", "À confirmer",
     "À valider"],
    ["Laque", LAQUE_TXT, "billardsdefrance.fr (cabine de finition dédiée à la laque)", "À valider"],
    ["Laque du cadre", LAQUE_TXT, "billardsdefrance.fr", "À valider"],
    ["Plateau simple, érable ou chêne, toutes teintes", "En une minute, votre billard devient une table à manger.",
     "Affirmation de la direction (26/11)", "À valider"],
]



# Arguments des choix des gammes Plaisance (bloc « ARGUMENTS DES CHOIX » de chaque onglet), brouillons du 27/11.
# Imprimés sous la ligne de l'option, après le « Détail imprimé sur le devis », quand le statut passe à « Actif ».
# Référence : aucune mention d'origine, jamais « italienne ».
DRAP_SIMONIS = "Drap Iwan Simonis : la manufacture belge tisse des draps depuis 1680 et habille les grands championnats."
DRAP_STRACHAN = ("Drap Strachan : la maison anglaise dont les draps équipent le championnat du monde de snooker "
                 "depuis 1980.")
SRC_FAB = "Sources du fabricant (iwansimonis.com, WSP Textiles)"
BANDES_FR_PL = "Bandes en caoutchouc fabriqué en France, calibrées pour ce jeu."
DEUXIEME_JEU = "Système breveté : changez de bandes, vous changez de jeu, sur le même billard."
RANGEMENT = "Queues, billes, craies et brosse ont leur place sous le billard."
VERRE = "Verre de sécurité trempé : résistant aux chocs et facile à entretenir."
TABLE = "Posez le plateau : votre billard devient une table à manger pour 8 à 10 personnes."
ALLONGE_12 = "l'allonge de 45 cm est incluse pour recevoir jusqu'à 12 convives."
EPOXY = "Laque époxy : une finition dure, qui résiste aux chocs."
NOS = "Nos fiches et grilles"


def _choix(*lignes):
    return [[c, t, s, "À valider"] for c, t, s in lignes]


CHOIX_PLAISANCE = {
    "Référence": _choix(
        ("Tapis standard (4 teintes)", "Un drap rapide et résistant, dans l'une des quatre teintes de la gamme.", NOS),
        ("Tapis Simonis 760 (26 teintes)", DRAP_SIMONIS, SRC_FAB),
        ("Tapis Strachan 777 (7 teintes)", DRAP_STRACHAN, SRC_FAB),
        ("Billard américain", "Le jeu le plus répandu, avec des bandes calibrées pour ses billes de 57 mm.", NOS),
        ("Pool anglais", "Le jeu des pubs anglais, avec des bandes calibrées pour ses billes de 50,8 mm.", NOS),
        ("6 plugs pour jouer au billard français",
         "Six plugs referment les poches : vous jouez aussi au billard français sur le même billard.", NOS),
        ("Plateau 100 % bois en 2 parties", TABLE, NOS),
        ("Plateau 100 % verre Sécurit en 2 parties", VERRE, NOS),
        ("Pieds noirs", EPOXY, NOS),
        ("Pieds blancs", EPOXY, NOS),
        ("Pieds gris anthracite", EPOXY, NOS),
        ("Pieds couleur RAL au choix", "Les pieds dans la couleur de votre intérieur, parmi tout le nuancier RAL.", NOS),
        ("Rangement des accessoires", RANGEMENT, NOS),
    ),
    "Design": _choix(
        ("Tapis Simonis 760 (26 teintes)", DRAP_SIMONIS, SRC_FAB),
        ("Tapis Strachan 777 (7 teintes)", DRAP_STRACHAN, SRC_FAB),
        ("Jeu de bandes français", BANDES_FR_PL, NOS),
        ("Jeu de bandes américain", BANDES_FR_PL, NOS),
        ("Jeu de bandes pool", BANDES_FR_PL, NOS),
        ("2e jeu de bandes américain", DEUXIEME_JEU, NOS),
        ("2e jeu de bandes pool", DEUXIEME_JEU, NOS),
        ("2e jeu de bandes français", DEUXIEME_JEU, NOS),
        ("Couleur RAL au choix", "Laqué à la main dans notre atelier du Gers, dans la couleur RAL de votre choix.", NOS),
        ("Vernis grand brillant et polissage du billard", "Vernis grand brillant, poli à la main pour un éclat profond.",
         NOS),
        ("Vernis grand brillant et polissage du dessus de table", "Le plateau assorti au billard, dans le même éclat.",
         NOS),
        ("Rangement des accessoires", RANGEMENT, NOS),
        ("Allonge de plateau 45 cm", "Avec l'allonge, la table reçoit jusqu'à 12 convives.", NOS),
        ("Plateau table bois laqué", TABLE, NOS),
        ("Plateau 100 % verre Sécurit 8 mm", VERRE, NOS),
        ("Plateau vitré cadre bois", "Cadre bois et verre de sécurité ; " + ALLONGE_12, NOS),
    ),
    "Prestige": _choix(
        ("Tapis Simonis 760 (26 teintes)", DRAP_SIMONIS, SRC_FAB),
        ("Tapis Strachan 777 (7 teintes)", DRAP_STRACHAN, SRC_FAB),
        ("Jeu de bandes français", BANDES_FR_PL, NOS),
        ("Jeu de bandes américain", BANDES_FR_PL, NOS),
        ("Jeu de bandes pool", BANDES_FR_PL, NOS),
        ("2e jeu de bandes américain", DEUXIEME_JEU, NOS),
        ("2e jeu de bandes pool", DEUXIEME_JEU, NOS),
        ("2e jeu de bandes français", DEUXIEME_JEU, NOS),
        ("Plateau table bois", "Dans la teinte du billard ; " + ALLONGE_12, NOS),
        ("Plateau 100 % verre Sécurit 8 mm", VERRE, NOS),
        ("Plateau verre et cadre couleur de rappel", "Le cadre reprend la couleur du billard ; " + ALLONGE_12, NOS),
        ("Motif décor à carré", "Quatre carrés peints sur le plateau, pour une table au dessin plus graphique.", NOS),
        ("Pieds métalliques", "Des pieds métalliques, pour une ligne plus contemporaine.", NOS),
    ),
}
