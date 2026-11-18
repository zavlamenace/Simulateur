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
        ("Tous", "Votre couleur",
         "Laque dans la couleur RAL de votre choix ; vernis brillant poli à la main en option."),
        ("Boston", "Laque gris clair satinée", "Un gris clair doux (RAL 7036), satiné, appliqué à la main."),
        ("Washington", "Laque gris anthracite", "Un anthracite profond et élégant, appliqué à la main."),
        ("New-York", "Laque blanc satiné", "Un blanc satiné lumineux, appliqué à la main."),
        ("Miami", "Laque noir satiné", "Un noir satiné intense, appliqué à la main."),
    ],
    "Prestige": [
        ("Tous", "Fabriqué dans le Gers",
         "Bois massif teinté et verni à la main dans nos ateliers de Plaisance-du-Gers."),
        ("Tous", "Silencieux",
         "Billes amorties par un capitonnage en 3 épaisseurs, récupérées dans un tiroir de chaque côté."),
        ("Tous", "Tout se range", "Rangement Octopack et support du plateau intégrés."),
        ("Tous", "Deux billards en un", "Système breveté de bandes interchangeables."),
        ("Tous", "Jusqu'à 12 couverts", "Allonge de plateau incluse."),
        ("Tous", "Châssis Woodstone", "Fibres entrecroisées et renforts métalliques : une stabilité durable."),
        ("Paris", "Cuir et chêne naturel mat", "Le cuir et le chêne naturel mat, vernis à la main."),
        ("Sydney", "Chêne naturel mat", "Le chêne massif dans sa teinte naturelle, en finition mate."),
        ("Venise", "Chêne teinté n°1", "Chêne massif teinté n°1 et verni à la main."),
        ("Athènes", "Chêne blanc verni", "Un vernis chêne blanc qui laisse apparaître le veinage du bois."),
        ("Pekin", "Chêne naturel et rechampi noir", "Chêne naturel mat rehaussé d'un rechampi noir."),
        ("Helsinki Wengé", "Teinte wengé n°17", "Chêne massif teinté wengé, profond et contemporain."),
        ("Helsinki blanchi", "Chêne blanchi n°19", "Chêne massif blanchi, clair et lumineux."),
        ("Rome", "Chêne teinté n°1", "Chêne massif teinté n°1 et verni à la main."),
        ("Florence", "Chêne vieilli ciré", "Un chêne vieilli et ciré, au charme authentique."),
        ("Rotterdam blanchi", "Chêne blanchi n°19", "Chêne massif blanchi, clair et lumineux."),
        ("Rotterdam Wengé", "Teinte wengé n°17", "Chêne massif teinté wengé, profond et contemporain."),
        ("Cardiff", "Chêne n°1", "Chêne massif teinte n°1, verni à la main."),
        ("Douvres", "Chêne n°1", "Chêne massif teinte n°1, verni à la main."),
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
