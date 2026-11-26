# Billards de France — dépôt interne

Ce dépôt contient deux projets de Billards de France (FITAN et FILS SAS) :

1. **Configurateur « Quelle taille de billard pour ma pièce »** (`configurateur-billard.html`, `README.md`). Il est livré et ne sert pas de référence de charte.
2. **Outil interne de devis** (en cours). Le plan validé est dans `connaissances/outil-devis-plan.md`. Code de la page : `devis/appscript/` (installation : `INSTALLATION.md`) ; banc d'essai et tests : `devis/banc/` (`npm test`).

**Le dépôt est privé et doit le rester.** Il contient des informations internes : origine de fabrication, grilles tarifaires, échanges commerciaux.

## Mémoire du projet : à lire avant toute tâche
Le dossier `connaissances/` fait foi sur l'entreprise. Les informations transmises en conversation y sont consignées.

| Fichier | Contenu |
|---|---|
| `connaissances/entreprise.md` | Histoire, chiffres, ateliers, showrooms, revendeurs, mentions légales |
| `connaissances/gammes/reference.md`, `design.md`, `prestige.md`, `lafuge.md` | Une fiche par gamme |
| `connaissances/conditions.md` | Paiement, échéancier, livraison, montage, garantie, validité, délais |
| `connaissances/arguments.md` | Arguments de réassurance : sélection de 4 arguments au maximum par devis, règles de rédaction, liste validée |
| `connaissances/accessoires.md` | Accessoires et options annexes (références, prix), caractéristiques techniques du 2,10 m |
| `connaissances/coloris.md` | Listes officielles des teintes de tapis (Standard, Simonis 760, Strachan 777) |
| `connaissances/charte.md` | Charte graphique du site (fait foi pour le PDF) |
| `connaissances/equipe.md` | Personnes qui font les devis |
| `connaissances/storytelling.md` | Idée de bloc histoire et réassurance par gamme (à développer après le Sheet tarifaire) |
| `connaissances/a-verifier.md` | Points ouverts, contradictions entre sources, chantier Lafuge et tarification |
| `connaissances/sources/` | Documents bruts fournis : tableau comparatif, PDF « Différences selon les gammes », grilles tarifaires papier, logo. Le PDF contient des mentions internes à ne jamais reprendre côté client (« Sous-traitant », « 0 SAV ») |

Si une information nouvelle contredit ces fichiers, mettre le fichier à jour dans le même commit que le travail concerné.

## Règles permanentes pour tout contenu client (PDF, emails, textes)
- **Gamme Référence Premium** :
  - ne jamais mentionner d'origine de fabrication ni de « fabrication française », ni de badge atelier ;
  - ardoise : écrire « ardoise de 19 mm », jamais « italienne ».
- Design et Prestige sont fabriqués à Plaisance-du-Gers ; Lafuge à Miribel-les-Échelles.
- **Références clients** (Yacht Club de Monaco, Sheraton Paris, villas prestigieuses de la Côte d'Azur et de la côte atlantique) : uniquement sur les devis Lafuge.
- **Ne jamais écrire** :
  - « 0 SAV en 10 ans » ;
  - la promesse de rappel personnel de Philippe Fitan ;
  - PayPlug ;
  - le droit de rétractation ou son exclusion ;
  - quoi que ce soit qui puisse rendre le client frileux.
- **Pas d'encadré visio** pour l'instant (peut revenir plus tard sur demande).
- **Kit accessoires** : mis en avant uniquement sur la Référence (inclus). Pour les autres gammes, c'est un argument oral, absent du PDF.
- **Logos** : produit Plaisance = logo Billards de France seul. Produit Lafuge = logo BdF + logo Lafuge, avec « Billard Lafuge, maison du groupe Billards de France ».
- **Design** : épuré, va à l'essentiel, pas d'« AI slop » :
  - pas de dégradé, d'ombre décorative, d'icône gadget ni d'emoji ;
  - rouge réservé à l'action de validation ;
  - les photos portent le message.
- **Le client se place au centre** : parler de son projet, pas de nos outils.

## Google Sheet « BdF – Tarifs & contenus » (fait foi pour les prix)
- **Lien** : https://docs.google.com/spreadsheets/d/1_MZBcXsz-DqXfk_hN1X1WY5_9wfMXTx9I52tOmSEooY/edit (propriétaire : le Gmail de Xavier Fitan).
- **Lecture** :
  - les blocs commencent par une cellule « ■ TITRE » en colonne A ;
  - la ligne suivante porte les en-têtes ;
  - les colonnes se lisent par leur nom, jamais par leur position (prototype : `devis/outils/lire_sheet.py`).
- **Écriture** :
  - toujours **relire l'onglet en ligne avant d'écrire** ;
  - n'écrire que des cellules ciblées ;
  - **ne jamais écraser une valeur modifiée par l'équipe** : en cas de doute, demander ;
  - ne jamais régénérer ni réimporter le classeur entier. `devis/outils/construire_sheet.py` n'est qu'une trace de la structure d'origine.
- **Arguments & photos** : colonne « Valable pour » = « Tous » (argument de gamme) ou un nom de modèle / de version (argument personnalisé, par exemple la finition Formica d'un modèle Référence). Au moins 3 à 4 arguments par gamme, chacun avec une photo ultra zoomée.

## Classeur « BdF – Tarifs revendeurs HT (confidentiel) »
- **Lien** : https://docs.google.com/spreadsheets/d/1b2Q7TEO6G6YFLZ75z_Wvvss-LggABT79Qy-uZqfOvWo/edit (propriétaire seul, non partagé).
- Prix d'achat revendeur HT départ (Lafuge) = prix TTC public ÷ 2.
- **Jamais lu par l'outil de devis, jamais transmis à un client.**

## Conventions
- Langue : français.
- Prix : TTC, clientèle de particuliers uniquement.
- Branche de développement : `claude/billiard-quote-tool-1wrwy3`.
