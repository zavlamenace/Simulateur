"""Arguments de réassurance validés le 19/11/2026 (statut « À valider » jusqu'à relecture finale).

Une entrée : (Valable pour, Titre, Texte, photo prévue, proposé par défaut).
- « Valable pour » : « Tous » ou une version (« Pieds bois massif », « Pieds métalliques »).
- Photo prévue : la colonne Photo affiche « À fournir » en attendant la photo ultra zoomée.
- Proposé par défaut : pré-coché dans l'outil (4 au maximum par gamme et par version).
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
        ("Tous", "Le meilleur rapport qualité-prix du marché",
         "Ardoise monobloc, structure en bois massif et pack accessoires inclus.", False, True),
        ("Tous", "Ardoise monobloc de 19 mm",
         "Une pierre naturelle d'un seul tenant : elle ne gonfle pas et ne se déforme pas avec l'humidité, "
         "contrairement au MDF. La bille roule droit, durablement.", True, True),
        ("Tous", "Pack accessoires offert",
         "16 billes, 4 queues, triangle, craies, brosse et porte-queue inclus (valeur 330 €).", True, True),
        ("Pieds bois massif", "Pieds bois massif et Formica",
         "Le Formica, le matériau des plans de travail de cuisine : il résiste aux chocs, aux rayures et aux taches, "
         "là où le papier décor courant s'abîme.", True, True),
        ("Pieds métalliques", "Pieds métalliques de 5 mm",
         "Acier de 5 mm d'épaisseur, laqué époxy : une rigidité à toute épreuve.", True, True),
        CHASSIS + (True, False),
        BOITES + (True, False),
        ("Tous", "Vérins de réglage", "Une planéité parfaite, même sur un sol irrégulier.", True, False),
        ("Tous", "Bandes en caoutchouc toilé", "Un rebond vif et régulier.", True, False),
        ("Tous", "Billard et table à manger", "Avec le plateau en 2 parties, une table pour 8 à 10 personnes.",
         False, False),
    ],
    "Design": [
        ("Tous", "Le meilleur rapport qualité-prix en fabrication française",
         "Un billard laqué, fabriqué à la main dans nos ateliers du Gers.", False, True),
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
        ("Tous", "Le billard convertible le plus fonctionnel du marché",
         "Rangements intégrés, réception centralisée des billes, allonge incluse.", False, True),
        ("Tous", "12 couverts, allonge incluse", "Avec le plateau bois, l'allonge de 45 cm est fournie.", False, True),
        ("Tous", "Châssis Woodstone",
         "Un bois haute densité aux fibres serrées : il absorbe le poids de l'ardoise sans fléchir et ne travaille "
         "ni avec l'humidité ni avec la température.", True, True),
        ("Tous", "Réception centralisée et insonorisée",
         "Goulottes capitonnées en 3 épaisseurs, un tiroir abattant de chaque côté.", True, True),
        ("Tous", "Système de rangement Octopack",
         "Un système intégré sous le billard pour ranger queues, bandes, billes et craies.", True, False),
        ("Tous", "Rangement des plateaux intégré", "Pendant la partie, les plateaux se rangent sous le billard.",
         True, False),
        BANDES_INTERCHANGEABLES + (True, False),
        ("Tous", "Ardoise italienne monobloc de 19 mm",
         "Une pierre naturelle d'un seul tenant, sur longerons métalliques : elle ne se déforme pas avec "
         "l'humidité, contrairement au MDF.", True, False),
        DRAP + (True, False),
        BANDES_FRANCAISES + (True, False),
        ("Tous", "Pieds en bois massif", "Chêne, hêtre ou tauari selon le modèle, teintés et vernis à la main.",
         True, False),
        ("Tous", "Fabriqué dans le Gers",
         "Bois massif teinté et verni à la main dans nos ateliers de Plaisance-du-Gers.", False, False),
    ],
    "Lafuge": [
        ("Tous", "Le billard le plus personnalisable",
         "Essence, teinte, laque, taille, finitions, liserés : chaque détail est à votre choix.", False, True),
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
         "Essence, teinte, laque, taille, finitions, liserés : chaque détail est à votre choix.", False, True),
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
