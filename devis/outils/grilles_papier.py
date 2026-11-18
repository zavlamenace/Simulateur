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
