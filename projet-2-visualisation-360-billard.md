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
6. « Enregistrer » : composition locale photo + 3D à la résolution native de l'écran,
   logo sur une plaque blanche translucide en bas à droite, puis feuille de partage
   native (Enregistrer dans Photos, AirDrop, WhatsApp…) ; repli sur un téléchargement
   direct, puis sur l'appui long sur l'image.
7. Portrait et paysage (en paysage, la fiche passe en colonne à droite sur un tiers
   de l'écran). Reprendre la photo recentre le billard ; changer de billard conserve
   position et zoom.

## Conversion (validé, en place)

- **Oney 4 fois** : ligne discrète sous le prix (fiche et écran de visualisation), calcul
  automatique (`SHOP.oneyParts`).
- **Recevoir mon aperçu** (étape 2, après la capture) : e-mail obligatoire, téléphone
  facultatif, consentement. L'image composée est jointe.
- **Conseiller** : pendant les horaires (`SHOP.hours`, lundi–vendredi 8h–12h / 13h–17h,
  heure du téléphone) « Appelez un conseiller » en appel direct ; sinon « Être rappelé »
  (nom, téléphone, créneau).
- **Devis sur-mesure** : bouton sur les produits `quote: true` (Lafuge) ; e-mail, téléphone,
  taille, essence, message, aperçu joint.
- **Sortie douce** : à la fermeture sans capture ni demande, une seule proposition
  « Recevoir cet aperçu avant de partir ? », puis on laisse partir.
- **Lien profond** : `?ar=1` ouvre directement la visualisation (pubs Meta, QR code) ;
  `&produit=bogota` présélectionne ; les `utm_*` sont conservés dans les événements et
  les demandes.
- **GA4** : chaque événement est poussé dans `dataLayer` (`event: 'bdf_ar'`, `ar_event`)
  et vers `gtag('event', …)` s'il existe. Entonnoir : `ar_cta_click` → `ar_photo_taken` →
  `ar_model_loaded` → `ar_first_gesture` → `ar_capture` → `ar_lead_submitted` /
  `ar_view_product` / `ar_call_click`.

### Envoi des demandes (à brancher par l'agence)

Le prototype n'a pas de serveur : l'envoi est simulé (panneau Diagnostic, objet
`window.__bdfLastLead`). En production, renseigner `SHOP.leadEndpoint` avec l'URL d'un
contrôleur du module PrestaShop qui reçoit un POST JSON :

```
{ type: "lead" | "callback" | "quote",
  to: "contact@billardsdefrance.fr", sentAt, page, utm,
  product: { id, name, brand, price },
  contact: { name, email, phone },
  fields: { slot, size, wood, message },
  image: "data:image/jpeg;base64,…" (lead et quote, ~0,5–1 Mo) | null,
  consent: true, session: { gestures, switches, captures } }
```

Traitement attendu : e-mail à `contact@billardsdefrance.fr` avec l'image en pièce jointe
et toutes les informations ; pour `lead`, copie au client avec l'image et le lien de la
fiche ; taille de requête à autoriser ≥ 2 Mo ; limitation de débit par IP ; jamais de
rendu HTML des champs sans échappement.

## Moteur 3D et chargement différé

Le rendu est fait directement avec three.js r160 (+ GLTFLoader), regroupés dans le
fichier HTML (~700 Ko) pour que le prototype fonctionne sans aucune requête réseau,
y compris dans le bac à sable de la page de test claude.ai. Le modèle est décodé en
mémoire (pas de fetch), le moteur WebGL n'est initialisé qu'après la prise de photo.
r160 est la dernière version compatible WebGL 1 : iPhone anciens (iOS 12/13) et
Android d'entrée de gamme fonctionnent, WebGL 2 est utilisé quand il existe.

**En production** : sortir three.js dans un fichier séparé sur le domaine du site,
chargé uniquement au clic sur le bouton (jamais au chargement de la fiche produit),
et servir les `.glb` depuis le domaine.

## Tester sur une vraie URL (GitHub Pages)

La page de test claude.ai exige une connexion et bloque l'enregistrement/partage de
fichiers. Pour tester l'enregistrement de l'image sur iPhone et Android :
Settings du dépôt → *Pages* → *Deploy from a branch* → branche
`claude/ar-billard-visualization-d8gtr4`, dossier `/ (root)` → Save. Le dépôt doit
être public. URL obtenue :
`https://zavlamenace.github.io/Simulateur/projet-2-visualisation-360-billard.html`

## Diagnostic

Lien « Diagnostic » en pied de page : panneau qui affiche l'appareil (navigateur,
écran, WebGL 1/2, partage de fichiers disponible), puis chaque événement et chaque
erreur en direct. Bouton « Copier » pour coller le rapport dans une conversation.
À retirer à l'intégration.

## Analytics (console pour le prototype)

Chaque événement s'affiche dans la console (`[BDF analytics]`) et s'accumule dans
`window.__bdfArEvents`. Événements : `ar_cta_click`, `ar_lib_loaded` / `ar_lib_error`,
`ar_unsupported`, `ar_photo_taken` (source camera/gallery), `ar_model_loaded` (durée),
`ar_first_gesture`, `ar_hint_opened`, `ar_product_switched`, `ar_retake`, `ar_capture`,
`ar_share`, `ar_download`, `ar_view_product`, `ar_closed` (durée, nombre de gestes, changements,
captures). À brancher sur GA4/Matomo lors de l'intégration : une seule fonction
`analytics.track(nom, propriétés)` à remplacer.

## Sécurité

- Aucune donnée ne quitte l'appareil : ni photo, ni capture, ni événements.
- Aucun appel réseau : three.js est dans le fichier, le modèle est décodé en mémoire.
  Vérifié sous une CSP stricte (`default-src 'self'; connect-src 'self'`).
  En production, three.js devient un fichier séparé servi par le domaine du site.
- Les modèles 3D sont référencés par identifiant produit dans une liste fermée, jamais
  par une URL venant d'un paramètre.
- Aucun contenu utilisateur injecté dans le HTML, pas de `eval`, pas de stockage local.
- Le fichier sélectionné est refusé s'il n'est pas une image.
- Si le navigateur n'a pas WebGL, un message propre renvoie vers la fiche produit.

## Premier scan réel (baby-foot, Kiri Engine, vidéo)

Fichier reçu : 17,5 Mo, 250 000 triangles, texture 4K, sol capturé autour de l'objet.
Traitement appliqué (`scratchpad/gt/crop.mjs` puis gltf-transform) :
1. détection du plan du sol (histogramme des hauteurs) et suppression des triangles
   au niveau du sol ;
2. conservation de la composante connexe principale (l'objet) et des fragments dans
   sa boîte ; suppression des morceaux de sol et de mur isolés ;
3. recentrage, pose au sol, `weld`, texture réduite à 1024 px (JPEG), `quantize`,
   `prune` → 1,46 Mo, 32 000 triangles.

Le modèle n'a pas d'échelle métrique : le prototype le met à la hauteur réelle du produit
(`height` dans le catalogue, 0,90 m pour le baby-foot) et le pose au sol automatiquement.

Qualité observée : silhouette et couleurs correctes, surfaces lissées, barres et joueurs
transformés en bosses, quelques trous sur le terrain. Pour améliorer : mode photo plutôt
que vidéo, 120 à 150 photos, trois hauteurs, lumière diffuse, fond uni, et ne pas
tourner trop vite ; les pièces fines (barres, poignées) resteront le point faible de la
photogrammétrie.

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

- Nom et prix du baby-foot scanné sont des valeurs de démonstration, à remplacer.
- Billards placeholder en géométrie simple (proportions réelles 210 × 120 × 80 cm et
  240 × 130 cm) : uniquement pour valider les gestes et le parcours.
- Pas d'ancrage au sol ni de détection de plan : le placement est libre, à l'œil.
- Le logo est une reconstitution vectorielle ; remplacer par le PNG officiel.
