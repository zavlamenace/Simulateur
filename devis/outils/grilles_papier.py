"""Données transcrites des grilles tarifaires papier (validées le 18/11/2026).

Sources : connaissances/sources/grille-design-p5.jpg, grille-prestige-p8.jpg, grille-prestige-p9.jpg.
Les noms de modèles suivent l'orthographe du site (« New-York », « Pekin ») pour rester
cohérents avec le bloc MODÈLES et la colonne « Valable pour » des arguments.
"""

DESIGN_PIETEMENT = "Pieds carrés hêtre 120 × 120"
DESIGN = {
    "New-York": "Moderne, laqué blanc, vernis mat",
    "Washington": "Moderne, laqué gris anthracite, vernis mat",
    "Miami": "Moderne, laqué noir, vernis mat",
    "Boston": "Moderne, laqué gris clair, vernis mat",
}

# modèle : (piètement, style et finition)
PRESTIGE = {
    "Douvres": ("Pieds tournés hêtre Ø 100", "Rustique, chêne n°1"),
    "Cardiff": ("Pieds carrés tauari 100 × 100", "Campagnard, chêne n°1"),
    "Rome": ("Pieds tournés chêne Ø 100", "Louis XIV, chêne n°1"),
    "Venise": ("Pieds carrés chêne 100 × 100", "Campagnard, chêne n°1"),
    "Rotterdam blanchi": ("Pieds tournés chêne Ø 100", "Moderne, blanchi n°19"),
    "Rotterdam Wengé": ("Pieds tournés chêne Ø 100", "Moderne, wengé n°17"),
    "Athènes": ("Pieds carrés chêne 100 × 100", "Moderne, blanc n°21"),
    "Florence": ("Pieds carrés chêne 100 × 100", "Campagnard, vieilli ciré n°7"),
    "Sydney": ("Pieds carrés chêne 100 × 100", "Moderne, naturel mat n°23"),
    "Helsinki blanchi": ("Pieds carrés chêne 100 × 100", "Moderne, blanchi n°19 + rechampi wengé"),
    "Helsinki Wengé": ("Pieds carrés chêne 100 × 100", "Moderne, wengé n°17 + rechampi aluminium"),
    "Pekin": ("Pieds galbés chêne 130 × 100", "Moderne, naturel mat n°23 + rechampi noir"),
    "Paris": ("Pieds gainés de cuir 100 × 100", "Moderne, cuir noir + inserts chêne naturel n°23"),
}

# Prix TTC des modèles Prestige : identiques au site (Helsinki blanchi : 4 600 €, prix du site, décision du 18/11).
PRESTIGE_PRIX = {nom: 4600 for nom in PRESTIGE} | {"Pekin": 5400, "Paris": 8800}

NOTE_VERIFIE = "Vérifié sur la grille papier (18/11)"

STRACHAN = ["Vert", "Bleu", "Rouge", "Gris", "Bordeaux", "Cherry", "Violet"]
STRACHAN_HEX = {
    "Vert": "1F6B3A", "Bleu": "1F4E9C", "Rouge": "B3202A", "Gris": "7D8285",
    "Bordeaux": "6E1A2A", "Cherry": "8E1B2F", "Violet": "5B2C7A",
}

# Accessoires & mobilier (grille p. 11, validée le 19/11) : (catégorie, article, détail, prix TTC, gammes, réf.)
TOUTES = "Référence, Design, Prestige, Lafuge"
ACCESSOIRES = [
    ("Packs", "Jeu d'accessoires 7 éléments", "4 queues de 120 cm, 1 boîte de craies, 1 porte-queue, 1 brosse", 250, TOUTES, "0193400"),
    ("Packs", "Jeu de 16 billes US + triangle", "16 billes US Ø 57 mm, 1 triangle, 1 règle de jeu", 80, TOUTES, "0191570"),
    ("Packs", "Jeu de 16 billes pool + triangle", "16 billes pool Ø 50,8 mm, 1 triangle, 1 règle de jeu", 80, TOUTES, "0191508"),
    ("Packs", "Jeu de 3 billes françaises", "3 billes françaises Ø 61,5 mm, règle de jeu", 35, TOUTES, "0190500"),
    ("Billes", "Jeu de 16 billes US", "16 billes US Ø 57 mm", 60, TOUTES, "0190700"),
    ("Billes", "Jeu de 16 billes pool", "16 billes pool Ø 50,8 mm", 60, TOUTES, "0191580"),
    ("Triangles", "Triangle pour billes Ø 57 mm", "Triangle noir", 20, TOUTES, "0190662"),
    ("Triangles", "Triangle pour billes Ø 50,8 mm", "Triangle noir", 20, TOUTES, "0190655"),
    ("Craies", "Boîte de 12 craies bleues", "12 craies", 8, TOUTES, "0190200"),
    ("Craies", "Boîte de 12 craies rouges", "12 craies", 8, TOUTES, "0190202"),
    ("Craies", "Boîte de 12 craies jaunes", "12 craies", 8, TOUTES, "0190203"),
    ("Craies", "Boîte de 12 craies vertes", "12 craies", 8, TOUTES, "0190201"),
    ("Queues", "Queue classique 100 cm", "Queue de billard classique", 50, TOUTES, "0190101"),
    ("Queues", "Queue classique 120 cm", "Queue de billard classique", 50, TOUTES, "0190100"),
    ("Queues", "Queue classique 140 cm", "Queue de billard classique", 50, TOUTES, "0190140"),
    ("Queues", "Queue de luxe américaine 140 cm", "Queue de luxe pour le billard américain", 95, TOUTES, "0191100"),
    ("Queues", "Queue de luxe pool 140 cm", "Queue de luxe en frêne pour le pool", 50, TOUTES, "0191101"),
    ("Queues", "Queue de luxe française 140 cm", "Queue de luxe pour le billard français", 70, TOUTES, "0191102"),
    ("Queues", "Queue en fibre de verre 120 cm", "Queue en fibre de verre", 60, TOUTES, "0191420"),
    ("Queues", "Queue en fibre de verre 140 cm", "Queue en fibre de verre", 65, TOUTES, "0191400"),
    ("Porte-queues", "Porte-queue simple noir", "Porte-queue mural", 20, TOUTES, "0190801"),
    ("Porte-queues", "Porte-queues avec horloge", "Finition chêne, L 70 × H 87 × P 8,2 cm", 189, TOUTES, "0190850"),
    ("Entretien", "Brosse", "Brosse à tapis", 22, TOUTES, "0194000"),
    ("Entretien", "Clé 6 pans", "Clé de réglage", 20, TOUTES, "0191200"),
    ("Entretien", "Règle de jeux", "Règles des jeux de billard", 20, TOUTES, "0191002"),
    ("Protection & rangement", "Protection PVC des dessus", "Protection PVC des plateaux, billard 2,10 m", 80, TOUTES, "0192050"),
    ("Protection & rangement", "Équerre de rangement des dessus et de l'allonge", "Range les plateaux et l'allonge à côté du billard", 150, TOUTES, "0192060"),
    ("Pieds", "Rehausse de pieds carrés", "Rehausse de 30 ou 50 mm", 200, "Design, Prestige", "0192070"),
]
