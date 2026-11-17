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

## Questions encore ouvertes
1. **RCS** : la mention légale prend la forme « RCS [ville du greffe] [SIREN] ». Pour une société du Gers, ce serait « RCS Auch 997 739 107 ». À confirmer, ou à corriger si le greffe est un autre.

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
