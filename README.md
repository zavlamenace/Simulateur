# Configurateur "Quelle taille de billard pour ma pièce" — Billards de France

Prototype fonctionnel autonome (`configurateur-billard.html`) à remettre au
développeur pour intégration PrestaShop. Zéro dépendance externe hors Google
Fonts (Fraunces + Inter). Tout le calcul se fait côté client, en JS vanilla.

## Ce que fait l'outil

1. Le client saisit la longueur et la largeur de sa pièce (cm).
2. Pour chacune des 5 tailles vendues (7, 8, 9, 10, 12 pieds), le calcul
   détermine la plus grande longueur de queue (100 / 120 / 140 cm) qui tient
   simultanément sur les deux axes de la pièce, en testant les deux
   orientations possibles du billard dans le rectangle.
3. Une recommandation unique est mise en avant : la plus grande taille qui
   atteint le confort optimal (queue 140 cm sur les deux axes). Si aucune
   taille n'atteint 140, on redescend jusqu'à la plus petite taille qui rentre
   quand même, affichée avec son confort réel (queue réduite).
4. Si même le 7 pieds ne rentre pas, l'outil bascule sur un écran d'invitation
   à appeler un conseiller (05 62 69 30 20), plutôt que de bloquer le client.
5. Chaque taille compatible est dépliable : elle révèle un plan 2D vu du
   dessus (pièce, zone de recul, billard) et la liste des produits
   disponibles dans cette taille (marque, photo, nom, lien).

## Logique de calcul (référentiel métier)

```
espace nécessaire (par axe) = tapis de jeu (par axe) + 2 × longueur de queue
```

Formule vérifiée point par point contre le tableau de mesures fourni par le
client (la marge de confort de 15 cm/côté est déjà intégrée dans les
longueurs de queue commercialisées — pas de terme supplémentaire à ajouter).

Le confort est calculé **séparément par axe**, mais le client n'achète qu'un
seul jeu de queues : la queue réellement utilisable = la plus contraignante
des deux axes (le minimum des deux résultats). Le détail par axe reste
affiché dans chaque fiche taille pour la transparence.

Voir les commentaires en tête de `configurateur-billard.html` (section
"RÉFÉRENTIEL DE CALCUL") pour la version commentée de cette règle, validée
avec le client le 19/08/2026.

## À faire côté développeur avant mise en production

- [ ] **Sécurité** : revue générale demandée par le client. Le prototype
  valide déjà les entrées côté client (bornes numériques, pas d'`innerHTML`
  sur du contenu dynamique — tout passe par `textContent`/création de
  nœuds DOM), mais aucun traitement serveur n'existe à ce stade : à
  auditer/durcir si un endpoint serveur est ajouté (webservice produits).
- [ ] **Catalogue produits** : remplacer le mapping statique `CATALOGUE`
  (en haut du `<script>`) par un appel au webservice PrestaShop. Conserver
  la forme `{ brand, name, url, image }` par produit pour ne pas casser le
  rendu. Point d'entrée unique : fonction `getProduits(sizeId)`.
- [ ] **Règle de marque** à respecter dans le mapping/l'API : le 7 pieds
  existe chez Plaisance ET Lafuge ; à partir du 8 pieds, seule la gamme
  Lafuge est proposée.
- [ ] **Analytics** : chaque interaction clé émet déjà un `CustomEvent` DOM
  préfixé `bdf-config:` (`dimensions_saisies`, `taille_recommandee`,
  `taille_depliee`, `produit_clique`, `aucune_taille_compatible`,
  `appel_conseiller_clic`) et pousse dans `window.dataLayer` s'il existe.
  Brancher GA4/Matomo en écoutant ces events, ou en s'appuyant sur le
  dataLayer.
- [ ] **Intégration CMS** : le widget est prévu pour être collé tel quel
  dans un bloc HTML de page/article PrestaShop (tout est scopé sous
  `#bdf-config`, pas de fuite de style global attendue — à vérifier quand
  même contre le CSS du thème en place).
- [ ] **Photos produits** : remplacer les vignettes placeholder (icône
  générique) par les vraies photos produit (`image` dans `CATALOGUE` ou la
  réponse API).

## Ce qui a été délibérément exclu de cette v1 (décisions client)

- Pas de hauteur sous plafond à saisir.
- Pas de gestion de zones d'exclusion dans la pièce (meuble, porte…) : on
  demande directement l'espace de jeu disponible à hauteur de table.
- Pas de back-office d'édition du référentiel : les tailles/mesures sont en
  dur dans le fichier, à modifier manuellement par le client ou son
  développeur si la gamme évolue.
- Pas de disclaimer légal : à la place, un CTA permanent vers le conseiller
  téléphonique.
