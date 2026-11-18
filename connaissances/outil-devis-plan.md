# Outil de devis Billards de France — plan avant production (v4)

## Contexte
Aujourd'hui, chaque devis billard se monte à la main alors que la combinatoire est forte (gamme × modèle × options × coloris). On veut :
- un tableau de tarifs simple à tenir ;
- une page web de saisie rapide ;
- un PDF épuré et premium aux couleurs du site, qui pousse le client à valider.

Objectif : améliorer la transformation entre la demande de devis et la commande.

**Approuver ce plan ne lance que la phase A** : base de connaissances et Google Sheet. Le PDF et la page de saisie ne seront construits qu'après validation du Sheet.

## Architecture retenue
- **Google Sheet « BdF – Tarifs & contenus »** : il fait foi. Tous les chiffres y sont et restent modifiables : prix, valeurs des offerts, pourcentages d'échéancier, seuil Oney, validité, grille de montage. Il appartient à votre Gmail. Les autres éditeurs (Philippe, Stéphanie…) s'y connectent avec un compte Google créé sur leur email pro, sans avoir besoin de Gmail.
- **Page de devis** : une application web Apps Script liée au Sheet.
  - Elle s'ouvre dans Chrome **sans aucun compte Google**, avec un **mot de passe commun**.
  - Elle tourne sous votre compte mais avec seulement deux autorisations, affichées par Google à l'installation : « ce tableur uniquement » et « télécharger des images depuis billardsdefrance.fr et Google Drive ».
  - Elle n'a **aucun accès à votre Gmail ni au reste de votre Drive**. L'outil n'envoie aucun email.
- **PDF** : construit par le code (pdfmake). Un clic le télécharge, sans fenêtre d'impression. Le texte est vectoriel, les polices EB Garamond et DM Sans sont intégrées, les liens sont cliquables.
- **Après « Générer le devis »** :
  - le PDF se télécharge ;
  - le devis est inscrit au Journal du Sheet ;
  - trois boutons sont proposés :
    - « Envoyer à contact@ » ouvre votre messagerie avec un email déjà rédigé contenant le récapitulatif. Il reste à joindre le PDF ;
    - « Copier le récap CRM » ;
    - « Copier l'email client ».

## Sécurité
- **Mot de passe commun** :
  - au moins 12 caractères, stocké haché et salé dans les propriétés du script, jamais dans le code ni dans le Sheet ;
  - on le change depuis le Sheet (menu « Outil devis › Changer le mot de passe »), réservé aux éditeurs ;
  - session de 8 h ;
  - blocage de 15 min après 10 échecs ;
  - chaque appel au serveur vérifie la session.
- **Sans mot de passe, on ne voit rien** : la page n'affiche que l'écran de connexion. Aucun prix ni contenu n'est envoyé avant authentification.
- **Données** : le Sheet n'est partagé qu'avec les éditeurs ; Journal et Paramètres sont protégés en écriture ; les saisies sont échappées.
- **Validation en deux étapes** recommandée sur votre Gmail, propriétaire de l'ensemble.

## Décisions validées
- **« Devis réalisé par »** (choix obligatoire, nom et fonction imprimés, sans photo) :

  | Personne | Fonction |
  |---|---|
  | Philippe Fitan | PDG de Billards de France (Billards Plaisance et Lafuge) |
  | Stéphanie Guigon | Secrétaire commerciale et achats Billards Lafuge |
  | Xavier Fitan | Directeur du développement & de la transformation digitale |
  | Alain Bottacin | Production / secrétariat |

- **Référence du devis** : automatique (BDF-2026-0001…). Le n° du logiciel de facturation est facultatif.
- **Échéancier** :

  | Marque | 1er versement | 2e versement | Solde |
  |---|---|---|---|
  | Plaisance | 30 % à la validation | — | avant livraison |
  | Lafuge | 30 % à la validation | 30 % au lancement en production | avant livraison |

  Encadré Oney 3x/4x seulement si le total est inférieur ou égal à 3 000 €.
- **Validation par le client depuis le PDF** :
  - bouton « Je valide mon devis » : il ouvre un email vers contact@ avec la référence, la configuration, le total, l'acompte, la demande de lien de paiement et un espace « Mes commentaires » ;
  - bouton « Appeler mon conseiller » (05 62 69 30 20) ;
  - encadré « Bon pour accord ».
- **Remise** en € ou en % : prix barré et ligne de remise. **Masquée s'il n'y a pas de remise.**
- **Livraison** : offerte au pied de la porte par messagerie (valeur 300 €). La grille livraison + montage change : vous me l'envoyez sur papier, elle ira dans le Sheet.
- **Validité** : 30 jours, avec la date affichée.
- **Logos** : Billards de France seul pour Plaisance. Pour Lafuge, BdF + Lafuge avec la mention « maison du groupe Billards de France ».
- **Avis Google** : Billards Plaisance 4,7/5 (47 avis), Billards Lafuge 4,8/5 (21 avis). On affiche ceux de la marque du produit.
- **Origine et matériaux** :
  - Référence : aucune mention d'origine. L'ardoise est décrite comme « ardoise de 19 mm, grande solidité », sans dire « italienne » ;
  - Design et Prestige : atelier de Plaisance-du-Gers ;
  - Lafuge : atelier de Miribel-les-Échelles.
- **Références clients, uniquement sur Lafuge** : Yacht Club de Monaco, Sheraton Paris, villas prestigieuses de la Côte d'Azur et de la côte atlantique.
- **Absents du PDF** : encadré visio, « 0 SAV en 10 ans », rappel de Philippe Fitan, lettre. Le message personnel va dans l'email.
- **Contenu** : un bloc court « Votre projet » de 3 à 5 lignes.
- **Faits validés** :
  - Plaisance créée en 1985 ;
  - Prestige : 1 tiroir de chaque côté ;
  - le showroom de Plaisance-du-Gers expose quasiment tous les Plaisance et les Lafuge ;
  - Paris est fermé.
- **Délais de fabrication** : Référence 2–3 sem., Design 4–6, Prestige 4–6, Lafuge 8 sem. minimum, hors organisation de la livraison.
- **Charte** (relevée sur le site) :
  - typographies : EB Garamond 700 pour les titres, DM Sans pour le texte ;
  - couleurs :

    | Rôle | Couleur |
    |---|---|
    | Encre | `#151515` |
    | Rouge | `#b01c2e` |
    | Crème | `#f6f3ee` |
    | Sable | `#efe9e3` et `#d9cfbf` |
    | Anthracite | `#3d4248` |

  - Règles « pas d'AI slop » : pas de dégradé, d'ombre, d'icône décorative ni d'emoji. Rouge réservé à la validation. Les photos portent le message.

## Catalogue connu à ce jour
**Coloris** (onglet commun) :
- standard Référence, sans marque, très bonne qualité : Gris clair, Bleu royal, Rouge, Vert ;
- Simonis 760, 26 teintes : Vert jaune, Vert bleu, Vert anglais, Vert olive, Vert pomme, Spruce, Vert foncé, Bleu pétrole, Bleu royal, Bleu marine, Bleu tournoi, Bleu électrique, Bleu poudré, Chocolat, Rouge, Bordeaux (burgundy), Rouge vin, Fuchsia, Violet, Orange, Camel, Or, Gris, Gris requin, Gris ardoise, Noir ;
- Strachan 777, 7 teintes : Bordeaux, Rouge, Vert olive, Bleu royal, Violet, Gris, Noir.

**Référence** (pré-remplie depuis le site) :

| Élément | Choix et prix |
|---|---|
| Tapis | 4 teintes standard incluses ; Simonis et Strachan en option à +620 € |
| Jeu | Américain ou Pool |
| Plugs français | +640 € |
| Dessus de table | bois en 2 parties +330 € ; verre Sécurit en 2 parties +1 100 € |
| Pieds | version pieds métalliques (couleur des pieds) |
| Kit accessoires | offert (valeur à donner) |

**Design** (4 modèles laqués : blanc, gris anthracite, noir, gris clair) :

| Option | Prix |
|---|---|
| Tapis (33 teintes) | inclus |
| Un jeu de bandes au choix | inclus |
| 2e jeu de bandes | américain +600 €, pool +700 €, français +700 € (différent du premier) |
| RAL au choix | +250 € |
| Vernis brillant et polissage du billard | +540 € |
| Vernis brillant et polissage du dessus de table | +270 € |
| Rangement des accessoires et des bandes | +400 € (photo à venir) |
| Allonge de plateau 45 cm | +500 € |
| Banc laqué assorti | +740 € (onglet commun Accessoires & mobilier, valable pour Référence, Design et Prestige) |

**Prestige** :

| Option | Prix |
|---|---|
| Tapis, un jeu de bandes, allonge, Octopack | inclus |
| 2e jeu de bandes | mêmes prix que Design |
| Pieds métalliques en remplacement du bois massif | statut « Bientôt », prix à définir |
| Plateau table bois | 990 € |
| Motif décor à carré | +300 €, uniquement avec le plateau bois |
| Plateau 100 % verre Sécurit 8 mm | 1 200 € |
| Plateau verre avec cadre couleur de rappel | 1 600 € |

**Lafuge, accessoires, livraison + montage** : d'après vos photos de grilles papier, à venir.

## Le Google Sheet
**Règle de lecture** : « on comprend sans formation ».
- **Onglets** :
  - Mode d'emploi ;
  - Référence · Design · Prestige · Lafuge ;
  - Coloris ;
  - Accessoires ;
  - Livraison & montage ;
  - Équipe ;
  - Revendeurs ;
  - Paramètres ;
  - Journal (rempli par l'outil, en lecture seule).
- **Chaque onglet de gamme** a 3 blocs titrés, empilés, chacun avec des lignes vides réservées :
  - **■ MODÈLES** : nom, finition et description, prix TTC, photo détourée, photos, statut, note interne. Pour Lafuge, une colonne de prix par taille.
  - **■ OPTIONS** : groupe (liste), nom affiché, détail imprimé, prix TTC, valeur si offert, statut (Actif / Bientôt / Masqué), valable pour (modèles), **nécessite** (une autre option, par exemple le motif à carré qui nécessite le plateau bois), **exclut** (par exemple 2e jeu ≠ jeu inclus), choix unique ou multiple.
  - **■ ARGUMENTS & PHOTOS** : titre, texte, photo de détail, ordre d'affichage.
- **Robustesse** :
  - l'outil lit les blocs par leurs titres et les colonnes par leurs en-têtes, jamais par position ;
  - insérer une ligne ou une colonne, ou ajouter un modèle ou une option dans les lignes vides, ne casse rien ;
  - pas de formules fragiles : les rares calculs utilisent des références de colonnes entières ;
  - listes déroulantes, format €, en-têtes figés, couleur par onglet ;
  - nouvelle gamme = dupliquer un onglet.
- **Photos** : un lien vers billardsdefrance.fr ou vers un dossier Drive « Photos devis » partagé en lecture.
- **Création** : directement dans votre Drive via le connecteur Google Sheets. À défaut, un fichier .xlsx mis en forme, avec ses listes déroulantes, à importer dans Drive.

## Phases
**A — Données (lancée si vous approuvez)**
1. `CLAUDE.md` et `connaissances/` dans le repo (entreprise, gammes, conditions, charte, équipe, règles), commit et push.
2. Extraction du site pour la Référence : modèles, prix, options chiffrées, photos détourées et de détail. Le reste des gammes sert de référence.
3. Structure du Sheet, avec la Référence pré-remplie et les options Design et Prestige ci-dessus.
4. **Design et Prestige d'abord**, à partir de vos photos de grilles papier. Je vous pose des questions avant de remplir.
5. Puis Lafuge, Accessoires et Livraison & montage, à partir de leurs photos.
6. Atelier « réassurance » gamme par gamme : je rédige les arguments et je choisis les photos de détail, vous validez.
7. **Point de validation : vous relisez le Sheet.**

**B — Maquette du PDF** sur 2 devis exemples. **Point de validation du design.**

**C — Page de saisie, mot de passe, génération du PDF, journal, textes.**

**D — Installation** (guide pas à pas), puis recette sur 5 devis réels.

## Réponses reçues (v4.1)
- **Design** :
  - 4 390 € pour les 4 modèles ;
  - couleurs et plateaux : d'après vos photos.
- **Prestige** : modèles, prix et finitions d'après vos photos.
- **Banc laqué +740 €** : le même banc pour Référence, Design et Prestige. Il va dans l'onglet commun **Accessoires & mobilier**, avec une colonne « gammes compatibles ».
- **Valeur du kit accessoires Référence** : 330 €.
- **Revendeurs** pour la carte :
  - **L'Ébéno**, région toulousaine (43.6011, 1.3012) ;
  - **L'Univers du Billard**, région nantaise (47.1103, -1.5435).

  Adresse exacte à relever en phase A. La carte affiche aussi les 2 showrooms : Plaisance-du-Gers et Miribel-les-Échelles.
- **Mentions légales** :
  - FITAN et FILS SAS, capital social 406 875 € ;
  - SIRET 997 739 107 00016 ;
  - TVA FR63997739107 ;
  - Chemin de la Riberotte, 32160 Plaisance-du-Gers.
- **Photos** : vous les envoyez dans la conversation.
  - Je les recadre, les optimise, les renomme et les range dans le repo (`devis/photos/`).
  - Je les dépose ensuite dans un dossier Drive « Photos devis », partagé en lecture et référencé dans le Sheet. Je passe par le connecteur Drive, ou à défaut je vous donne un zip à glisser dans Drive.
  - Les photos de grilles tarifaires servent seulement à la saisie dans le Sheet, elles ne sont pas publiées.

## Avancement de la phase A (17/11)
**Fait** :
- **Base de connaissances** : `CLAUDE.md` et `connaissances/` sont commités et poussés (commit f91d124).
- **Extraction du site** :
  - Référence : 12 modèles (6 bois + 6 métal, Panama compris), prix, options chiffrées, photos détourées (billard ouvert, plateau bois, plateau verre) et gros plans ;
  - Design : 4 modèles. Correspondance relevée sur le site : Boston gris clair, Washington gris anthracite, New-York blanc, Miami noir ;
  - Prestige : 13 modèles et prix du site.
- **Classeur généré** (`devis/outils/construire_sheet.py`), lu par `devis/outils/lire_sheet.py`. Les 4 tests de `devis/tests/test_sheet.py` passent : structure, prix Référence identiques au site, règles métier Référence, insertion de ligne et de colonne sans effet.
- **Google Sheet créé dans le Drive** : « BdF – Tarifs & contenus », https://docs.google.com/spreadsheets/d/1_MZBcXsz-DqXfk_hN1X1WY5_9wfMXTx9I52tOmSEooY/edit. Les listes déroulantes et les en-têtes figés ont été conservés à la conversion.

**À faire en premier en sortant du mode plan** : commiter et pousser `devis/` (outils, données extraites, tests, .xlsx). C'est du travail non sauvegardé.

**Règle à partir de maintenant** : le Google Sheet en ligne fait foi. Les mises à jour se font directement dedans, via le connecteur Google Sheets et cellule par cellule. On ne régénère plus le classeur, ce qui écraserait les modifications faites à la main. Le générateur reste dans le dépôt comme trace de la structure.

**Prochaines étapes** :
1. Recevoir les photos des grilles **Design et Prestige**, poser les questions de compréhension, puis remplir les onglets.
2. Faire de même avec les grilles Lafuge, Accessoires et Livraison & montage.
3. Atelier réassurance : photos de détail et textes des blocs « Arguments & photos », aujourd'hui « À valider ».
4. Partager le Sheet avec les éditeurs (comptes Google sur leur email pro).

## Réponses du 17/11 et production à lancer
**Réponses** :
- **Photos Référence** : validées.
- **Panama** : bonne affaire, hors catalogue. Ses 2 lignes passent en « Masqué ».
- **Octopack** : inclus sur Prestige. Pour la Référence, la ligne reste masquée.
- **Pieds en couleur RAL** (Référence) : prix pas encore fixé, statut « Bientôt ».
- **Pieds PMMA** : la ligne est supprimée, on ne les fait plus.
- **RCS Auch 997 739 107** : confirmé.

**Réassurance personnalisée par billard** :
- Le bloc « ARGUMENTS & PHOTOS » de chaque onglet de gamme reçoit une colonne **« Valable pour »** :
  - « Tous » pour un argument de gamme ;
  - un nom de modèle ou de finition pour un argument personnalisé. Exemple : « Finition Formica chêne naturel » pour Mendoza, « Formica teck marron » pour Caracas.
- Chaque argument a sa **photo ultra zoomée** (lien) et son ordre.
- Il faut **au moins 3 à 4 arguments par gamme**, plus les arguments propres à chaque modèle ou finition.
- Le PDF prend les arguments « Tous » de la gamme, puis ceux du modèle choisi.

**Comment la page web lira le Sheet sans formule** :
1. Elle ouvre l'onglet de la gamme, par exemple « Prestige ».
2. Elle cherche la ligne qui commence par « ■ OPTIONS ».
3. La ligne suivante donne les noms des colonnes. L'outil y repère la colonne qui s'appelle « Prix TTC », où qu'elle se trouve.
4. Il lit chaque ligne jusqu'au prochain « ■ » et retient celle dont la colonne « Option » vaut « Plateau table bois ».

Si une colonne est insérée, « Prix TTC » change de place mais garde son nom, donc on la retrouve. C'est déjà codé et testé dans `devis/outils/lire_sheet.py`. Le futur lecteur de la page web applique les mêmes règles.

**Ne jamais écraser vos modifications dans le Sheet** :
- Avant chaque écriture, je relis l'onglet en ligne.
- J'écris uniquement les cellules visées, jamais un bloc entier.
- Si une cellule que je veux changer a été modifiée par vous depuis ma dernière lecture, je ne l'écrase pas et je vous demande.
- L'historique des versions de Google Sheets permet de toute façon de revenir en arrière.

**Production (sortie du mode plan)** :
1. Commiter et pousser `devis/`, et mettre à jour `connaissances/` (RCS, Panama, PMMA, Octopack, règle de réassurance par modèle).
2. Ajuster le générateur, le lecteur et les tests pour la colonne « Valable pour » des arguments.
3. **Mettre à jour le Google Sheet en ligne, par écritures ciblées après relecture** :
   - Panama → Masqué ;
   - suppression de la ligne PMMA ;
   - pieds RAL → Bientôt ;
   - RCS confirmé ;
   - ajout de la colonne « Valable pour » ;
   - brouillons d'arguments, au moins 4 par gamme, plus un argument par finition Référence : Formica noir brillant, blanc brillant, teck marron, chêne gris anthracite, chêne naturel. Statut « À valider », photos à fournir.
4. Attendre les photos des grilles Design et Prestige, puis les photos ultra zoomées.

## Grilles Design et Prestige + PDF « Différences selon les gammes » (18/11)

### Décisions
**Design** : 4 modèles à 4 390 €, style Moderne, pieds carrés en hêtre 120 × 120. Le libellé de finition est celui de la grille papier :
- New York : laqué blanc, vernis mat ;
- Washington : laqué gris anthracite, vernis mat ;
- Miami : laqué noir, vernis mat ;
- Boston : laqué gris clair, vernis mat.

| Option Design | Prix | Règle |
|---|---|---|
| Tapis (33 teintes) | inclus | |
| 1 jeu de bandes | inclus | |
| 2e jeu de bandes, quel qu'il soit | **700 €** | Différent du jeu inclus |
| RAL au choix | +250 € | |
| Vernis grand brillant + polissage du billard | +540 € | Seul niveau de vernis proposé |
| Vernis grand brillant + polissage du dessus | +270 € | Nécessite le plateau bois laqué |
| Plateau bois laqué (même configuration que le billard) | 990 € | |
| Plateau 100 % verre Sécurit 8 mm, motif à carré, 2 parties, sans allonge | 1 100 € | |
| Plateau vitré (cadre bois, verre Sécurit 6 mm, 2 parties) | 1 600 € | **Allonge incluse** |
| Allonge 45 cm, une seule finition laquée | +500 € | **Uniquement avec le plateau bois laqué** |
| Rangement des accessoires (queues, billes, craies, brosse) | +400 € | |

Retirés : vernis brillant simple (+150 € / +50 €), bandes peintes, incrustation de matière.

**Prestige** : 13 modèles. La ligne « Cardiff wengé » de la grille est obsolète.

| Modèle | Piètement | Style et finition | Prix |
|---|---|---|---|
| Douvres | pieds tournés hêtre Ø 100 | Rustique, chêne n°1 | 4 600 € |
| Cardiff | pieds carrés tauari 100 × 100 | Campagnard, chêne n°1 | 4 600 € |
| Rome | pieds tournés chêne Ø 100 | Louis XIV, chêne n°1 | 4 600 € |
| Venise | pieds carrés chêne 100 × 100 | Campagnard, chêne n°1 | 4 600 € |
| Rotterdam blanchi | pieds tournés chêne Ø 100 | Moderne, blanchi n°19 | 4 600 € |
| Rotterdam wengé | pieds tournés chêne Ø 100 | Moderne, wengé n°17 | 4 600 € |
| Athènes | pieds carrés chêne 100 × 100 | Moderne, blanc n°21 | 4 600 € |
| Florence | pieds carrés chêne 100 × 100 | Campagnard, vieilli ciré n°7 | 4 600 € |
| Sydney | pieds carrés chêne 100 × 100 | Moderne, naturel mat n°23 | 4 600 € |
| Helsinki blanchi | pieds carrés chêne 100 × 100 | Moderne, blanchi n°19 + rechampi wengé | **4 600 €** (prix du site) |
| Helsinki wengé | pieds carrés chêne 100 × 100 | Moderne, wengé n°17 + rechampi aluminium | 4 600 € |
| Pékin | pieds galbés chêne 130 × 100 | Moderne, naturel mat n°23 + rechampi noir | 5 400 € |
| Paris | pieds gainés de cuir 100 × 100 | Moderne, cuir noir + inserts chêne naturel n°23 | 8 800 € |

| Option Prestige | Prix | Règle |
|---|---|---|
| Tapis, 1 jeu de bandes | inclus | |
| 2e jeu de bandes | 700 € | |
| Plateau bois en 2 parties, teinte du billard | 990 € | **Allonge 45 cm incluse** |
| Motif décor à carré peint sur le plateau bois | +300 € | Exemples : Athènes, 4 carrés marron foncé ; Helsinki, 4 carrés aluminium |
| Plateau 100 % verre Sécurit 8 mm, motif à carré, sans allonge | 1 200 € | |
| Plateau vitré (cadre bois, verre 6 mm) | 1 600 € | Allonge incluse |
| Pieds métalliques | « Bientôt » | |

« Supplément teinte » : ne pas le noter.

**Inclus de série sur Prestige** :
- Simonis 760, porte-queues et rangement des bandes intégrés (Octopack) ;
- rangement du plateau sous le billard ;
- goulottes insonorisées et **un tiroir abattant de chaque côté** : réception centralisée des billes ;
- ardoise monobloc 19 mm avec longerons métalliques ;
- châssis Woodstone.

**Woodstone** (argument du PDF) : bois haute densité aux fibres serrées. Il absorbe le poids de l'ardoise sans fléchir et ne travaille pas avec l'humidité ni la température. La surface reste parfaitement plane dans le temps.

**Référence** :
- l'Octopack n'est **pas possible** : la ligne reste masquée, avec cette note ;
- on **ajoute** une ligne « Rangement des accessoires » à **400 €**, Actif (queues, billes, craies, brosse, comme sur Design) ;
- **pieds métalliques** : leur prix est l'écart entre la version bois et la version métal (Bogota 1 995 € → 2 395 €, soit 400 €). Ce supplément est déjà compris dans le prix des modèles « Pieds métalliques ». La couleur RAL des pieds passe donc à **0 €, Actif**, avec cette note ;
- Panama : on n'y touche pas (Masqué) ;
- PMMA : sorti du catalogue (déjà supprimé) ;
- RCS : confirmé.

**Strachan 777** : liste de la grille papier, qui fait foi : Vert, Bleu, Rouge, Gris, Bordeaux, Cherry, Violet. Simonis : on garde 26 teintes, même si la grille papier en annonce 25.

**Banc laqué** à 740 € : coloris blanc, noir, gris clair, anthracite ou aluminium. Il est proposé pour Référence, Design et Prestige.

**Décor du verre** (dépoli, etc.) : non proposé dans l'outil.

**Données internes du PDF à ne jamais reprendre côté client** : « Sous-traitant » (Référence), « 0 SAV en 10 ans ».

### Production
1. **Connaissances** : mettre à jour `design.md`, `prestige.md`, `reference.md`, `conditions.md` (Strachan) et `a-verifier.md` (écarts tranchés : 2e jeu à 700 €, vernis, Helsinki à 4 600 €, Cardiff wengé obsolète, Strachan papier).
2. **Trace** : mettre à jour `arguments_brouillons.py` et `construire_sheet.py`, et adapter les tests. Commit et push.
3. **Google Sheet en ligne**, par écritures ciblées après relecture de chaque bloc :
   - **Design** :
     - modèles : version = piètement, finition = grille, note « Vérifié grille papier » ;
     - options : 2e jeu américain 600 → 700 € ; libellés « grand brillant » ; vernis du dessus → nécessite « Plateau table bois laqué » ;
     - remplir la ligne « Plateau table » avec les 3 plateaux ; allonge → nécessite « Plateau table bois laqué » ; rangement des accessoires renommé.
   - **Prestige** :
     - modèles : piètement et finition, note « Vérifié grille papier » ;
     - options : 2e jeu américain 600 → 700 € ; détails des plateaux (allonge incluse) ; détail du motif à carré.
   - **Référence** :
     - Octopack reste masqué, note « Pas possible sur la Référence » ;
     - nouvelle ligne « Rangement des accessoires », 400 €, Actif ;
     - pieds couleur RAL → 0 €, Actif, note sur l'écart de 400 € déjà compris dans la version métal.
   - **Coloris** : les 7 lignes Strachan reprennent la liste papier, avec leurs codes couleur.
   - **Accessoires & mobilier** : coloris du banc.
   - **Arguments** :
     - Design : pieds en hêtre massif et laques vernis mat ;
     - Prestige : réception centralisée avec un tiroir de chaque côté, Woodstone détaillé, porte-queues et rangement des bandes, piètement et finition de chaque modèle.

     Les textes restent « À valider ».
4. **En attente** : la photo des accessoires (vous la renvoyez), puis les grilles Lafuge et livraison + montage, puis les photos ultra zoomées.

### État au 18/11 (interruption par redémarrage de session)
**Fait et poussé** (commit 9c1a821) :
- connaissances : design, prestige, reference, entreprise, a-verifier, `coloris.md`, sources ;
- trace : `grilles_papier.py`, `arguments_brouillons.py`, `construire_sheet.py` ;
- 6 tests verts.

**Relecture du Sheet en ligne avant écriture** :
- aucune modification de l'équipe sur les cellules visées ;
- **une modification de l'équipe à préserver** : onglet Coloris, colonne « Note interne » des 4 teintes Standard, qui contient « Référence uniquement ». On n'y touche pas.

**Écrit dans le Sheet et vérifié par relecture (18/11, terminé)** : toutes les écritures listées ci-dessous.
- Design, Prestige, Référence, Coloris et Accessoires sont conformes.
- Lignes vides réservées : 12 dans OPTIONS, 6 dans ARGUMENTS.
- Note de l'équipe « Référence uniquement » préservée.

**Méthode à partir de maintenant** : un seul appel d'écriture à la fois, jamais d'appels en parallèle (deux redémarrages de session sont survenus pendant des écritures parallèles). Relire après chaque groupe.

**Reste à écrire** : relire chaque plage juste avant d'écrire, et n'écrire que si elle contient encore l'ancienne valeur. Les valeurs exactes viennent de `grilles_papier.py` et `arguments_brouillons.py`.

1. **Design** :

   | Plage | Valeur |
   |---|---|
   | B44:C46 | Vernis grand brillant billard / dessus, Rangement des accessoires |
   | H45 | Plateau table bois laqué |
   | H47:K47 | Nécessite plateau bois laqué + note allonge |
   | A48:K50 | Les 3 plateaux : 990 / 1 100 / 1 600 € |
   | A65:F74 | 10 arguments |

   Mise en forme :
   - fond blanc sur A49:K50 et A74:F74 ;
   - insérer 1 ligne après la ligne 79 (index 79), puis 2 lignes après la ligne 60 (index 60), en héritant du format de la ligne précédente. Dans cet ordre, pour ne pas décaler les autres plages.
2. **Prestige** :

   | Plage | Valeur |
   |---|---|
   | B19:C31 | Piètement / finition, dans l'ordre Paris, Sydney, Venise, Athènes, Pekin, Helsinki Wengé, Helsinki blanchi, Rome, Florence, Rotterdam blanchi, Rotterdam Wengé, Cardiff, Douvres |
   | J19:J31 | Note « Vérifié sur la grille papier (18/11) » |
   | D49 | 700 |
   | C52:C55 et K52:K55 | Détails et notes des plateaux et du motif |
   | A73:F91 | 19 arguments |

3. **Référence** :

   | Plage | Valeur |
   |---|---|
   | D54:F54 | [0, "", "Actif"] |
   | K54:K55 | Notes RAL et Octopack |
   | A56:K56 | Nouvelle ligne « Rangement des accessoires », 400 € |

   Mise en forme : fond blanc sur A56:K56, puis insérer 1 ligne à l'index 67.
4. **Coloris** :
   - B36:C42 : Strachan papier avec codes couleur ;
   - fond de D36:D42 à la couleur de chaque teinte ;
   - ne pas toucher à F6:F9.
5. **Accessoires & mobilier** : C6 = « Banc laqué : blanc, noir, gris clair, anthracite ou aluminium ».
6. **Contrôle final** : relire les 5 onglets, comparer au contenu attendu, puis rendre compte.

## Questions encore ouvertes
1. **RCS** (confirmé le 17/11) : la mention légale prend la forme « RCS [ville du greffe] [SIREN] ». Pour une société du Gers, ce serait « RCS Auch 997 739 107 ». À confirmer, ou à corriger si le greffe est un autre.
2. **Panama** (pieds bois et pieds métalliques) : rangé dans « Bonnes affaires » sur le site. Toujours au catalogue ?
3. **Référence** :
   - prix de l'Octopack (option selon le comparatif) ;
   - prix des pieds en couleur RAL au choix ;
   - les pieds PMMA transparents (+1 800 €, vus uniquement sur Panama) sont-ils encore proposés ?

## Vérification
- **Phase A** :
  - contrôle automatique que chaque prix Référence extrait correspond à la fiche produit ;
  - aucune option sans gamme ;
  - chaque « nécessite » ou « exclut » pointe vers une option existante ;
  - test d'insertion d'une ligne et d'une colonne dans un onglet de gamme : la lecture reste identique ;
  - relecture par vous.
- **Phases B et C**, sur un banc local Playwright + Chromium avec un catalogue d'exemple :
  - 5 scénarios : Référence avec Oney et remise ; Design avec RAL, allonge et 2e jeu ; Prestige avec plateau bois et motif ; Lafuge avec échéancier en 3 temps ; option « Bientôt » masquée ;
  - PDF généré et capture de chaque page ;
  - contrôles : total égal à la somme des lignes moins la remise, TVA égale au TTC ÷ 6, échéancier égal au total, règle Oney, remise masquée si nulle, aucune origine ni « italienne » sur une Référence, références clients seulement sur Lafuge, email de validation de moins de 1 800 caractères avec son espace commentaires, liens cliquables.
- **Apps Script** :
  - sans mot de passe, aucune donnée renvoyée ;
  - blocage après 10 échecs ;
  - écriture au Journal ;
  - autorisations limitées aux deux permissions annoncées.
