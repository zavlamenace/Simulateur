# Projet n°2 — Visualisation 360 billard « Voir ce billard chez moi »

Prototype autonome (`projet-2-visualisation-360-billard.html`) à valider sur téléphone
avant toute intégration PrestaShop. Indépendant du configurateur de taille (projet n°1).

## Ce que fait le prototype

1. Sur la fiche produit, un bouton rouge « Voir ce billard chez moi » (affiché sur mobile ;
   sur desktop, un encart « Disponible sur mobile »).
2. Le client prend une photo de sa pièce (appareil photo natif, ou une photo de sa galerie).
   La photo reste sur le téléphone : aucun envoi serveur.
3. Le billard apparaît en vrai 3D sur la photo, avec une ombre portée au sol.
   - 1 doigt : déplacer
   - 2 doigts : zoomer (pincer) et tourner (rotation autour de l'axe vertical)
   - la hauteur de regard est verrouillée à une hauteur humaine (pas de vue du dessus)
   - une aide discrète apparaît 5 s au premier chargement, puis via le bouton « ? »
4. Menu déroulant pour changer de billard sans repasser par la fiche produit.
5. « Voir le produit » : retour vers la fiche du billard sélectionné (conversion).
6. « Enregistrer » : composition locale photo + 3D + logo discret en bas à droite,
   puis partage/enregistrement dans les photos (feuille de partage iOS/Android)
   ou appui long sur l'image si le partage de fichiers n'est pas disponible.
7. Portrait et paysage (en paysage, la fiche passe en colonne à droite).

## Chargement différé

La librairie 3D (`@google/model-viewer` 3.4.0, ~930 Ko, three.js inclus) n'est
téléchargée **qu'au clic sur le bouton**, jamais au chargement de la fiche produit.
Le modèle 3D du billard n'est décodé qu'après la prise de photo. La version 3.4.0 est
retenue volontairement : dernière version compatible WebGL 1, donc iPhone anciens non
mis à jour (iOS 13+) ; les versions 4.x exigent WebGL 2 (iOS 15+).

## Analytics (console pour le prototype)

Chaque événement s'affiche dans la console (`[BDF analytics]`) et s'accumule dans
`window.__bdfArEvents`. Événements : `ar_cta_click`, `ar_lib_loaded` / `ar_lib_error`,
`ar_unsupported`, `ar_photo_taken` (source camera/gallery), `ar_model_loaded` (durée),
`ar_first_gesture`, `ar_hint_opened`, `ar_product_switched`, `ar_retake`, `ar_capture`,
`ar_share`, `ar_view_product`, `ar_closed` (durée, nombre de gestes, changements,
captures). À brancher sur GA4/Matomo lors de l'intégration : une seule fonction
`analytics.track(nom, propriétés)` à remplacer.

## Sécurité

- Aucune donnée ne quitte l'appareil : ni photo, ni capture, ni événements.
- Un seul appel réseau : la librairie 3D, version épinglée, empreinte d'intégrité
  (`integrity` SHA-384) vérifiée par le navigateur. **En production, copier le fichier
  sur le domaine du site** et remplacer l'URL, pour ne dépendre d'aucun CDN tiers et
  rester compatible avec une CSP stricte (`script-src 'self'`).
- Les modèles 3D sont référencés par identifiant produit dans une liste fermée, jamais
  par une URL venant d'un paramètre.
- Aucun contenu utilisateur injecté dans le HTML, pas de `eval`, pas de stockage local.
- Le fichier sélectionné est refusé s'il n'est pas une image.
- Si le navigateur n'a pas WebGL, un message propre renvoie vers la fiche produit.

## Pipeline de production des modèles 3D (sans budget)

1. **Scan** : app KIRI Engine, mode *Photo Scan* (gratuit, export GLB sans watermark).
   80 à 150 photos, trois hauteurs, lumière diffuse, pas de flash. Pour les modèles
   laqués blanc/noir, tester d'abord en gratuit ; le mode payant « objet sans
   caractéristiques » ne se justifie que si le maillage sort troué.
2. **Nettoyage** (si besoin) : Blender, modificateur *Decimate*, suppression du sol.
3. **Optimisation** : `npx @gltf-transform/cli optimize scan.glb billard.glb --texture-compress webp`
   (compression Draco de la géométrie, textures 1024 px). Cible : 2 à 4 Mo par produit.
   Si Draco est utilisé, héberger aussi le décodeur sur le site
   (`ModelViewerElement.dracoDecoderLocation`).
4. **Orientation** : le modèle doit être posé au sol (Y = 0 sous les pieds), centré,
   en mètres, Y vers le haut. L'ombre et la hauteur de regard en dépendent.
5. **Remplacement** dans le prototype : les billards placeholder sont encodés en base64
   dans la constante `GLB` ; en production, servir des fichiers `.glb` depuis
   `/img/3d/<id>.glb` et donner l'URL à `model-viewer`.

Commencer par 3 produits pilotes (un billard, un baby-foot, un porte-queue) avant les 70.

## Intégration PrestaShop (à remettre à l'agence)

- Module custom accroché à la fiche produit (`displayProductAdditionalInfo`) : injecte le
  bouton, le catalogue des produits disposant d'un `.glb` (id, nom, marque, prix, URL
  fiche, URL glb) et l'écran plein écran.
- Le bouton n'est rendu que si le produit a un modèle 3D et si l'appareil est tactile.
- « Voir le produit » redirige vers l'URL de la fiche du billard sélectionné.
- Charte : rouge `#BE1E2D`, encre `#1A1A1A`, crème `#F6F4EF`, serif gras pour les titres,
  sans-serif pour le texte — à aligner sur les variables du thème.

## Limites connues du prototype

- Billards placeholder en géométrie simple (proportions réelles 210 × 120 × 80 cm et
  240 × 130 cm) : uniquement pour valider les gestes et le parcours.
- Pas d'ancrage au sol ni de détection de plan : le placement est libre, à l'œil.
- Le logo est une reconstitution vectorielle ; remplacer par le PNG officiel.
