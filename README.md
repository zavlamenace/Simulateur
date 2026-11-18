# Configurateur "Quelle taille de billard pour ma pièce" (Billards de France)

Prototype fonctionnel autonome (`configurateur-billard.html`) à remettre au
développeur pour intégration PrestaShop. Aucune dépendance de code (JS
vanilla) ; seule ressource externe : les polices Google Fonts de la charte
du site (EB Garamond, DM Sans). Tout le calcul se fait côté client.

## Ce que fait l'outil

1. Le client saisit la longueur et la largeur de sa pièce (cm).
2. Un **plan 2D vu du dessus s'affiche en permanence** dès que les deux
   dimensions sont saisies : la pièce (contour), la zone de recul
   (pointillés) et le billard illustré (cadre en bois arrondi, 6 poches,
   tapis vert), positionnés à l'échelle réelle. Ce plan se met à jour en
   direct à chaque frappe.
3. Pour chacune des 5 tailles vendues (7, 8, 9, 10, 12 pieds), le calcul
   détermine la plus grande longueur de queue (100 / 120 / 140 cm) qui tient
   sur chaque axe de la pièce, en testant les deux orientations possibles du
   billard. Les tailles qui ne rentrent pas sont affichées **verrouillées**
   (non cliquables, avec une icône de cadenas).
4. Une recommandation unique est mise en avant : la plus grande taille qui
   atteint le confort optimal (queue 140 cm sur les deux axes). Si aucune
   taille n'atteint 140, on redescend jusqu'à la plus petite taille qui rentre
   quand même, affichée avec son confort réel.
5. Le client peut cliquer sur n'importe quelle taille qui rentre pour la
   **prévisualiser** : le billard sur le plan grandit/rétrécit avec une
   animation, l'espacement disponible et la liste de produits se mettent à
   jour en conséquence. La taille conseillée reste identifiée par un badge
   "Conseillé" pendant ce temps. Les produits sont affichés **par marque,
   chacune sur sa propre rangée horizontale** (ex. Plaisance au-dessus de
   Lafuge pour le 7 pieds), pour comparer les modèles d'une même marque
   côte à côte ; à partir du 8 pieds, seule la rangée Lafuge est visible.
6. L'**espacement disponible** (Haut / Bas / Gauche / Droite, en cm) est
   annoté directement sur le plan 2D, comme des cotes de plan d'architecte,
   plutôt que dans un bloc de chiffres séparé, mesuré depuis le cadre du
   billard jusqu'aux murs, pour la taille actuellement prévisualisée.
7. Si même le 7 pieds ne rentre pas, **le plan reste visible** : il compare
   à l'échelle la pièce réelle (contour) à l'espace minimum qu'il faudrait
   pour notre plus petit billard (zone rouge), et l'outil bascule sur un
   écran d'invitation à appeler un conseiller (icône bulle + silhouette ou
   photo du conseiller, 05 62 69 30 20) plutôt que de bloquer le client.
8. Une **légende de confort toujours visible** (sans clic) est affichée
   juste au-dessus de la grille des tailles : elle explique en une ligne
   chacun des trois niveaux (Confortable = 140 cm, Confortable avec une
   légère gêne en mode jeu = 120 cm, Gêne = 100 cm), pour que le client
   comprenne d'où viennent les pastilles de couleur sans avoir à deviner.
9. Un raisonnement pédagogique ("Comment calculons-nous votre
   recommandation ?") est disponible en accordéon repliable tout en bas :
   trois étapes numérotées avec un exemple chiffré complet (211 - 30 = 181
   cm de tapis, puis 181 + 140 + 140 = 461 cm), suivies d'un **schéma
   illustré** (billard vu du dessus avec cadre en bois arrondi, 6 poches,
   tapis vert, et une **queue de billard dessinée** qui sort du billard
   vers le mur) pour visualiser concrètement le recul nécessaire, plutôt
   que de simples rectangles abstraits.

## Logique de calcul (référentiel métier)

```
espace de jeu nécessaire (par axe) = tapis de jeu (par axe) + 2 × longueur de queue
```

Formule vérifiée point par point contre le tableau de mesures fourni par le
client. Le cadre du billard déborde le tapis de jeu de **15 cm de chaque
côté**, sur toute la gamme (`table = tapis + 30 cm`), une constante vérifiée
sur les 5 tailles, pas une marge de confort ajoutée arbitrairement.

Cette constante explique l'écart entre deux informations affichées côte à
côte dans l'outil :
- **l'espacement affiché** ("Espacement disponible depuis le billard") est
  mesuré depuis le *cadre* du billard,
- **la queue conseillée** est mesurée depuis le *tapis*,
- donc `espacement affiché = queue conseillée - 15 cm`.

Le confort est calculé **indépendamment par axe**, et le client est conseillé
sur **deux jeux de queues distincts** quand les axes diffèrent (un pour la
longueur, un pour la largeur), afin de profiter du meilleur confort possible
sur chaque sens de jeu (ex. confortable en longueur avec 140 cm, gêne en
largeur avec 100 cm : deux jeux différents plutôt qu'un compromis unique).

Seule la classification globale d'une taille (utilisée pour décider la
recommandation et le repli en cascade) se base sur l'axe le plus contraignant
des deux, un raccourci de classement, pas une consigne d'achat.

Échelle de confort (wording commercial validé) :
- **140 cm** : *Confortable*
- **120 cm** : *Confortable avec une légère gêne en mode jeu*
- **100 cm** : *Gêne*

## Charte graphique appliquée

Charte réelle du site Billards de France (relevée sur le site) :

- Fond : Crème `#F6F3EE`, **majoritaire sur toute la page**
- Cartes/surfaces : Sable clair `#EFE9E3` ; champs de saisie et fonds
  "verrouillés" : Sable foncé `#D9CFBF`
- Texte : Encre `#151515`, texte secondaire : Anthracite `#3D4248`
- Rouge principal (CTA, taille conseillée, avatar conseiller, footer) :
  `#B01C2E`
- Titres : EB Garamond, 700 ; corps de texte : DM Sans (Google Fonts)
- Billard sur le plan 2D : illustré (cadre en bois, 6 poches, tapis vert),
  le vert et l'ambre restent des couleurs **sémantiques** (niveaux de
  confort), volontairement distinctes de l'identité de marque

**Remarque** : la charte réelle ne comporte pas de rouge pâle dédié ; la
teinte pâle utilisée pour la zone de recul sur le plan et le badge "Gêne"
est dérivée du rouge principal par `color-mix()` plutôt qu'une couleur
inventée.

**Thème unique, volontairement** : ce widget ne s'adapte pas au mode sombre
du système du visiteur, il impose toujours son fond crème et son rouge de
marque. C'est un choix délibéré suite à un retour du client : en mode
sombre système, le rouge de marque était automatiquement éclairci pour le
contraste, ce qui donnait l'impression visuelle d'utiliser le rouge
secondaire à la place du principal. Le code ne contient donc pas de bloc
`@media (prefers-color-scheme: dark)`.

## Responsive

Le widget s'adapte à la largeur réelle de son conteneur (et non à celle de
la fenêtre du navigateur) via les **CSS container queries**
(`container-type: inline-size` sur `#bdf-config`, règles `@container bdf
(min-width: …)`), pas seulement des `@media`. C'est important puisque
l'outil sera inséré dans une colonne de blog dont la largeur n'est pas
celle de l'écran. Sur un navigateur qui ne supporte pas les container
queries (rare aujourd'hui), le widget reste utilisable : il retombe
simplement sur la mise en page mobile (une colonne), sans rien de cassé,
pas de polyfill nécessaire, mais à vérifier une fois inséré dans le vrai
thème PrestaShop.

- **Mobile** (< 520px de large) : tout est empilé sur une colonne, grille
  des tailles en 2 colonnes.
- **Tablette** (520-760px) : grille des tailles en 3 colonnes.
- **Desktop** (≥ 700px) : le formulaire de saisie passe à gauche et le
  résultat (recommandation + plan 2D) à droite, côte à côte.
- **Grand écran** (≥ 760px) : grille des tailles sur une seule ligne de 5
  colonnes.

## À faire côté développeur avant mise en production

- [ ] **Sécurité** : revue générale demandée par le client. Le prototype
  valide déjà les entrées côté client (bornes numériques, pas d'`innerHTML`
  sur du contenu dynamique, tout passe par `textContent`/création de
  nœuds DOM), mais aucun traitement serveur n'existe à ce stade.
- [ ] **Catalogue produits** : remplacer le mapping statique `CATALOGUE`
  (en haut du `<script>`) par un appel au webservice PrestaShop. Conserver
  la forme `{ brand, name, url, image }` par produit. Point d'entrée unique :
  fonction `getProduits(sizeId)`.
- [ ] **Règle de marque** à respecter dans le mapping/l'API : le 7 pieds
  existe chez Plaisance ET Lafuge ; à partir du 8 pieds, seule la gamme
  Lafuge est proposée.
- [ ] **Analytics** : chaque interaction clé émet déjà un `CustomEvent` DOM
  préfixé `bdf-config:` (`dimensions_saisies`, `taille_recommandee`,
  `taille_selectionnee`, `produit_clique`, `aucune_taille_compatible`,
  `appel_conseiller_clic`) et pousse dans `window.dataLayer` s'il existe.
  Le client souhaite tracker spécifiquement les sessions où des dimensions
  sont saisies sans clic produit ensuite (`dimensions_saisies` sans
  `produit_clique` associé) pour des campagnes de relance.
- [ ] **Intégration CMS** : le widget est prévu pour être collé tel quel
  dans un bloc HTML de page/article PrestaShop (tout est scopé sous
  `#bdf-config`, pas de fuite de style global attendue, à vérifier quand
  même contre le CSS du thème en place).
- [ ] **Photos produits** : remplacer les vignettes placeholder (icône
  générique) par les vraies photos produit (`image` dans `CATALOGUE` ou la
  réponse API).
- [x] **Avatar conseiller** : la vraie photo fournie par le client est
  intégrée (variable `CONSEILLER_PHOTO_URL` en haut du `<script>`, section
  montage en bas de fichier). Le fichier source est aussi conservé dans
  `assets/conseiller.jpg` pour référence. **À faire côté développeur** :
  la photo est actuellement encodée en data URI directement dans le HTML
  (~780 Ko) pour garder le prototype autonome en un seul fichier ; en
  production, mieux vaut héberger ce fichier via le gestionnaire de médias
  PrestaShop et remplacer `CONSEILLER_PHOTO_URL` par son URL réelle, pour
  ne pas alourdir le poids de la page et bénéficier de la mise en cache
  navigateur. L'avatar SVG dessiné (`bubblePersonIcon()`) reste dans le
  code comme solution de repli si `CONSEILLER_PHOTO_URL` est vidé.
- [ ] **Polices** : EB Garamond et DM Sans sont chargées depuis Google
  Fonts (`<link>` en tête de fichier). Si la politique du site interdit les
  appels à des polices externes, héberger ces deux polices en local
  (fichiers woff2) et adapter les règles `@font-face`.
- [ ] **Animation du plan** : la transition du billard (cadre, tapis,
  poches) repose sur l'animation CSS des propriétés géométriques SVG
  (`x`/`y`/`width`/`height`/`cx`/`cy`), supportée nativement par les
  navigateurs modernes (Chrome/Firefox/Safari récents). Dégrade proprement
  (changement instantané sans animation) sur navigateur plus ancien, pas de
  polyfill nécessaire.

## Ce qui a été délibérément exclu de cette v1 (décisions client)

- Pas de hauteur sous plafond à saisir.
- Pas de gestion de zones d'exclusion dans la pièce (meuble, porte, etc.) :
  on demande directement l'espace de jeu disponible à hauteur de table (un
  meuble bas, type canapé, ne compte pas comme obstacle).
- Pas de back-office d'édition du référentiel : les tailles/mesures sont en
  dur dans le fichier, à modifier manuellement par le client ou son
  développeur si la gamme évolue.
- Pas de disclaimer légal, pas de fourchette de prix affichée, pas de
  fonction de partage du résultat : à la place, un CTA permanent vers le
  conseiller téléphonique (05 62 69 30 20), jugé suffisant par le client.
