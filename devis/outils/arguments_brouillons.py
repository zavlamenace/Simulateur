"""Brouillons d'arguments de réassurance (statut « À valider »), par gamme.

Chaque entrée : (Valable pour, Titre, Texte). « Tous » = argument de gamme ;
sinon nom exact d'un modèle (bloc MODÈLES) ou d'une version (« Pieds métalliques »).
Les photos ultra zoomées seront ajoutées quand l'équipe les aura fournies.
Règles : jamais d'origine ni « italienne » pour la Référence (voir CLAUDE.md).
"""

FORMICA = (
    "Le Formica est l'un des revêtements les plus durables : il résiste aux chocs, aux rayures et aux taches, "
    "là où un simple papier décor s'use vite."
)

ARGUMENTS = {
    "Référence": [
        ("Tous", "Ardoise monobloc de 19 mm",
         "D'une seule pièce, elle offre une surface de jeu parfaitement plane et une grande solidité dans le temps."),
        ("Tous", "Structure en bois massif",
         "Cadre et pieds en bois massif, châssis renforcé de métal. Les vérins sous chaque pied assurent une mise "
         "à niveau parfaite, même sur un sol irrégulier."),
        ("Tous", "Bandes en caoutchouc toilé", "Un rebond vif et régulier, partie après partie."),
        ("Tous", "Prêt à jouer dès la livraison",
         "Kit offert : 16 billes, 4 queues de 120 cm, triangle, craies, brosse et porte-queue."),
        ("Tous", "Billard et table à manger",
         "Avec son plateau en 2 parties, il devient en quelques secondes une table pour 8 à 10 personnes."),
        ("Santiago", "Formica noir brillant", f"{FORMICA} Son noir brillant profond donne au billard une vraie présence."),
        ("Rio", "Formica blanc brillant", f"{FORMICA} Son blanc brillant illumine la pièce et l'agrandit visuellement."),
        ("Caracas", "Formica teck marron", f"{FORMICA} Le teck apporte la chaleur du bois, sans son entretien."),
        ("Bogota", "Formica chêne gris anthracite",
         f"{FORMICA} Un chêne grisé contemporain, qui s'accorde avec les intérieurs actuels."),
        ("Mendoza", "Formica chêne naturel", f"{FORMICA} Un chêne clair et naturel, lumineux et intemporel."),
        ("Pieds métalliques", "Pieds métalliques réglables",
         "Laqués époxy, ils dessinent une ligne contemporaine et se règlent pour une planéité parfaite."),
    ],
    "Design": [
        ("Tous", "Fabriqué dans le Gers", "Fabriqué et laqué à la main dans nos ateliers de Plaisance-du-Gers."),
        ("Tous", "Deux billards en un",
         "Notre système breveté de bandes interchangeables : un vrai billard français et un vrai pool, "
         "sans compromis sur le rebond."),
        ("Tous", "Drap de compétition inclus",
         "26 teintes Simonis 760 ou 7 teintes Strachan 777, les références mondiales, sans supplément."),
        ("Tous", "Ardoise italienne de 19 mm", "Rectifiée pour une planéité parfaite."),
        ("Tous", "Pieds en hêtre massif", "Pieds carrés de 120 mm en hêtre massif : une assise robuste et stable."),
        ("Tous", "Votre couleur",
         "Laque dans la couleur RAL de votre choix ; vernis grand brillant poli à la main en option."),
        ("Boston", "Laqué gris clair, vernis mat", "Un gris clair doux, laqué à la main puis protégé par un vernis mat."),
        ("Washington", "Laqué gris anthracite, vernis mat",
         "Un anthracite profond et élégant, laqué à la main puis protégé par un vernis mat."),
        ("New-York", "Laqué blanc, vernis mat", "Un blanc lumineux, laqué à la main puis protégé par un vernis mat."),
        ("Miami", "Laqué noir, vernis mat", "Un noir intense, laqué à la main puis protégé par un vernis mat."),
    ],
    "Prestige": [
        ("Tous", "Fabriqué dans le Gers",
         "Bois massif teinté et verni à la main dans nos ateliers de Plaisance-du-Gers."),
        ("Tous", "Réception centralisée et silencieuse",
         "Goulottes capitonnées en 3 épaisseurs : les billes roulent sans bruit jusqu'à un tiroir abattant, "
         "de chaque côté du billard."),
        ("Tous", "Tout se range",
         "Porte-queues, rangement des bandes et des accessoires intégrés (Octopack), support du plateau sous le billard."),
        ("Tous", "Deux billards en un",
         "Système breveté de bandes interchangeables : un vrai billard français et un vrai pool, "
         "sans compromis sur le rebond."),
        ("Tous", "Jusqu'à 12 couverts", "Avec le plateau bois, l'allonge de 45 cm est incluse."),
        ("Tous", "Châssis Woodstone",
         "Un bois haute densité aux fibres serrées : il absorbe le poids de l'ardoise sans fléchir et ne travaille "
         "ni avec l'humidité ni avec la température. Votre surface de jeu reste parfaitement plane, année après année."),
        ("Paris", "Cuir noir et chêne naturel",
         "Pieds gainés de cuir, inserts en chêne naturel n°23 : une pièce de caractère, au style moderne."),
        ("Sydney", "Chêne naturel mat",
         "Chêne massif teinte n°23 en finition mate, sur pieds carrés en chêne de 100 mm. Un style moderne et épuré."),
        ("Venise", "Chêne n°1, style campagnard",
         "Chêne massif teinte n°1, pieds carrés en chêne de 100 mm : la chaleur d'un style campagnard."),
        ("Athènes", "Chêne blanc n°21",
         "Chêne massif teinte blanc n°21, sur pieds carrés en chêne de 100 mm. Un style moderne et lumineux."),
        ("Pekin", "Chêne naturel et rechampi noir",
         "Chêne naturel mat n°23 rehaussé d'un rechampi noir, sur pieds galbés en chêne : un modèle signature."),
        ("Helsinki Wengé", "Wengé n°17, rechampi aluminium",
         "Chêne massif teinté wengé, rehaussé d'un rechampi aluminium, sur pieds carrés en chêne."),
        ("Helsinki blanchi", "Blanchi n°19, rechampi wengé",
         "Chêne massif blanchi, rehaussé d'un rechampi wengé, sur pieds carrés en chêne."),
        ("Rome", "Style Louis XIV",
         "Chêne massif teinte n°1, pieds tournés en chêne de 100 mm : l'élégance d'un style Louis XIV."),
        ("Florence", "Chêne vieilli ciré",
         "Chêne massif vieilli et ciré (n°7), pieds carrés en chêne : le charme d'un style campagnard authentique."),
        ("Rotterdam blanchi", "Blanchi n°19, pieds tournés",
         "Chêne massif blanchi, pieds tournés en chêne de 100 mm. Un style moderne et clair."),
        ("Rotterdam Wengé", "Wengé n°17, pieds tournés",
         "Chêne massif teinté wengé, pieds tournés en chêne de 100 mm. Un style moderne et profond."),
        ("Cardiff", "Chêne n°1, pieds en tauari",
         "Chêne massif teinte n°1, pieds carrés en tauari de 100 mm : un style campagnard robuste."),
        ("Douvres", "Style rustique",
         "Chêne massif teinte n°1, pieds tournés en hêtre de 100 mm : le charme d'un style rustique."),
    ],
    "Lafuge": [
        ("Tous", "Une pièce unique",
         "Conçue avec vous et fabriquée à la main par un seul ébéniste, du début à la fin."),
        ("Tous", "Essences nobles",
         "Chêne, érable, noyer, mélèze, kotibé ; laque dans toute couleur RAL, patine, incrustations."),
        ("Tous", "Ardoise italienne rectifiée", "De 19 à 50 mm selon la taille."),
        ("Tous", "Ils nous ont choisis",
         "Yacht Club de Monaco, Sheraton Paris, villas prestigieuses de la Côte d'Azur et de la côte atlantique."),
        ("Tous", "Deux jeux, un seul billard",
         "Le système breveté de bandes interchangeables est offert pour les projets multi-jeux."),
    ],
}


def lignes(gamme):
    """Lignes du bloc ARGUMENTS & PHOTOS : Ordre, Valable pour, Titre, Texte, Photo, Statut."""
    return [[i, v, t, x, None, "À valider"] for i, (v, t, x) in enumerate(ARGUMENTS[gamme], start=1)]
