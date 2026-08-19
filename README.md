# Configurateur "Quelle taille de billard pour ma pièce" — Billards de France

Prototype fonctionnel autonome (`configurateur-billard.html`) à remettre au
développeur pour intégration PrestaShop. Zéro dépendance externe : pas de
Google Fonts, uniquement des polices système (Georgia / Helvetica). Tout le
calcul se fait côté client, en JS vanilla.

## Ce que fait l'outil

1. Le client saisit la longueur et la largeur de sa pièce (cm).
2. Un **plan 2D vu du dessus s'affiche en permanence** dès que les deux
   dimensions sont saisies : la pièce (contour gris), la zone de recul
   (pointillés) et le billard (vert), positionnés à l'échelle réelle. Ce plan
   se met à jour en direct à chaque frappe.
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
   "Conseillé" pendant ce temps.
6. Un bloc **"Espacement disponible depuis le billard"** (Haut / Bas / Gauche
   / Droite, en cm) affiche l'espace réel entre le cadre du billard et les
   murs, pour la taille actuellement prévisualisée.
7. Si même le 7 pieds ne rentre pas, l'outil bascule sur un écran d'invitation
   à appeler un conseiller (05 62 69 30 20), plutôt que de bloquer le client.
8. Un raisonnement condensé ("Comment calculons-nous votre recommandation ?")
   est disponible en accordéon repliable tout en bas, pour ne pas alourdir la
   page tout en offrant une explication commerciale à qui la demande.

## Logique de calcul (référentiel métier)

```
espace de jeu nécessaire (par axe) = tapis de jeu (par axe) + 2 × longueur de queue
```

Formule vérifiée point par point contre le tableau de mesures fourni par le
client. Le cadre du billard déborde le tapis de jeu de **15 cm de chaque
côté**, sur toute la gamme (`table = tapis + 30 cm`) — c'est une constante
vérifiée sur les 5 tailles, pas une marge de confort ajoutée arbitrairement.

Cette constante explique l'écart entre deux informations affichées côte à
côte dans l'outil :
- **l'espacement affiché** ("Espacement disponible depuis le billard") est
  mesuré depuis le *cadre* du billard,
- **la queue conseillée** est mesurée depuis le *tapis*,
- donc `espacement affiché = queue conseillée − 15 cm`.

Le confort est calculé **indépendamment par axe**, et le client est conseillé
sur **deux jeux de queues distincts** quand les axes diffèrent — un pour la
longueur, un pour la largeur — afin de profiter du meilleur confort possible
sur chaque sens de jeu (ex. confortable en longueur avec 140 cm, gêne en
largeur avec 100 cm : deux jeux différents plutôt qu'un compromis unique).

Seule la classification globale d'une taille (utilisée pour décider la
recommandation et le repli en cascade) se base sur l'axe le plus contraignant
des deux — c'est un raccourci de classement, pas une consigne d'achat.

Échelle de confort (wording commercial validé) :
- **140 cm** — *Confortable*
- **120 cm** — *Moyennement confortable*
- **100 cm** — *Gêne*

## Charte graphique appliquée

- Fond : gris clair neutre (`#F2F3F3`)
- Titres : Georgia, gras
- Corps de texte : Helvetica
- Rouge (accent principal, CTA, taille conseillée) : `#AD132C`
- Rouge pâle (accent secondaire, zone de recul sur le plan, badge "Gêne") :
  `#E37688`
- Noir/encre pour le texte et les tracés
- Billard sur le plan 2D : vert (couleur neutre du tapis, distincte de
  l'accent de marque)

## À faire côté développeur avant mise en production

- [ ] **Sécurité** : revue générale demandée par le client. Le prototype
  valide déjà les entrées côté client (bornes numériques, pas d'`innerHTML`
  sur du contenu dynamique — tout passe par `textContent`/création de
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
  `#bdf-config`, pas de fuite de style global attendue — à vérifier quand
  même contre le CSS du thème en place).
- [ ] **Photos produits** : remplacer les vignettes placeholder (icône
  générique) par les vraies photos produit (`image` dans `CATALOGUE` ou la
  réponse API).
- [ ] **Animation du plan** : la transition du rectangle billard repose sur
  l'animation CSS des propriétés géométriques SVG (`x`/`y`/`width`/`height`
  sur `<rect>`), supportée nativement par les navigateurs modernes
  (Chrome/Firefox/Safari récents). Dégrade proprement (changement instantané
  sans animation) sur navigateur plus ancien — pas de polyfill nécessaire.

## Ce qui a été délibérément exclu de cette v1 (décisions client)

- Pas de hauteur sous plafond à saisir.
- Pas de gestion de zones d'exclusion dans la pièce (meuble, porte…) : on
  demande directement l'espace de jeu disponible à hauteur de table (un
  meuble bas ne compte pas comme obstacle).
- Pas de back-office d'édition du référentiel : les tailles/mesures sont en
  dur dans le fichier, à modifier manuellement par le client ou son
  développeur si la gamme évolue.
- Pas de disclaimer légal, pas de fourchette de prix affichée, pas de
  fonction de partage du résultat : à la place, un CTA permanent vers le
  conseiller téléphonique (05 62 69 30 20), jugé suffisant par le client.
