# Arguments de réassurance — logique et règles (validé le 19/11/2026)

Les textes vivent dans le Google Sheet (bloc « ■ ARGUMENTS & PHOTOS » de chaque onglet de gamme), qui fait foi. La liste de départ se trouve dans `devis/outils/arguments_brouillons.py`.

## Fonctionnement dans l'outil de devis
1. On choisit le produit. L'outil liste les arguments de la gamme : ceux « Valable pour = Tous », plus ceux de la version du produit (« Pieds bois massif », « Pieds métalliques »), ou plus tard d'un modèle.
2. Le commercial **coche au maximum 4 arguments**, ceux qui parlent le plus à ce client. Les arguments « Proposé par défaut = Oui » sont pré-cochés (4 au maximum par gamme et par version).
3. **Argument avec photo** (colonne Photo = un lien) : la photo ultra zoomée s'affiche dans le PDF. **Argument sans photo** : texte seul. « À fournir » dans la colonne Photo signale une photo attendue ; l'outil le traite comme une absence de photo.
4. Le PDF affiche exactement les arguments cochés, dans l'ordre de la colonne « Ordre ».
5. **Pas d'arguments par produit** : ils ont été jugés trop faibles. On reste au niveau de la gamme et de la version.

## Règles de rédaction
- **Titre court et texte d'une phrase**, concis et factuel. Modèle à suivre : « Bandes en caoutchouc toilé : un rebond vif et régulier. »
- **Aucune formule de remplissage** : ni « partie après partie », ni « même tard le soir », ni « dès la livraison », ni « effet surprise », ni « en famille », etc.
- **Couleurs de tapis** : « 26 couleurs ». Jamais « 33 teintes ».
- **Ardoise** : jamais « rectifiée pour une planéité parfaite ». Pour la Référence, jamais « italienne ».
- **Bandes interchangeables** : « Plusieurs jeux sur un même billard : français, américain ou pool, à vous de choisir. » Jamais « offertes ».
- **Octopack** : c'est le **système** de rangement qui est inclus, pas les accessoires.
- **Interdits** : « exclusivité », « 0 SAV », et toute mention d'origine pour la Référence.
- **Arguments non différenciants à éviter** : par exemple « décor à carrés en option ».
- **Positionnements de gamme** voulus par la direction, en texte seul :

  | Gamme | Positionnement |
  |---|---|
  | Référence | le meilleur rapport qualité-prix du marché |
  | Design | le meilleur rapport qualité-prix en fabrication française |
  | Prestige | le billard convertible le plus fonctionnel du marché ; 12 couverts d'office, allonge incluse avec le plateau bois |
  | Lafuge | le billard le plus personnalisable |

## Recherches de fond (pour défendre les arguments)
**Ardoise contre MDF** :
- l'ardoise est une pierre naturelle, stable et dense, qui équipe toutes les tables professionnelles ;
- le MDF (panneau de fibres) gonfle et se déforme avec le temps et l'humidité, ce qui fait dévier ou ralentir la bille ;
- une ardoise garde sa planéité pendant des décennies ;
- l'ardoise **monobloc** est d'un seul tenant, sans joint.

Sources : Rue du Commerce (guide « Quel billard choisir »), Sawyer Twain, Pool Table Service, Tri Billiards, forum AZBilliards.

**Formica (stratifié haute pression, norme EN 438)** :
- plusieurs couches de papier kraft imprégnées de résine, pressées à chaud ;
- c'est le matériau historique des plans de travail de cuisine ;
- le papier décor (mélaminé basse pression) n'est qu'une feuille collée sur un panneau ;
- Formica indique lui-même que ce type de surface résiste nettement moins aux rayures, à l'usure et aux chocs.

Sources : Formica (« HPL and TFL »), Futura Sciences, Polyrey.

## Liste de départ (19/11)
Légende : ★ = proposé par défaut ; 📷 = photo ultra zoomée à fournir.

**Référence**
- ★ Le meilleur rapport qualité-prix du marché
- ★📷 Ardoise monobloc de 19 mm
- ★📷 Pack accessoires offert (330 €)
- ★📷 Pieds bois massif et Formica (version pieds bois)
- ★📷 Pieds métalliques de 5 mm (version pieds métalliques)
- 📷 Châssis bois massif renforcé
- 📷 6 boîtes insonorisées
- 📷 Vérins de réglage
- 📷 Bandes en caoutchouc toilé
- Billard et table à manger

**Design**
- ★ Le meilleur rapport qualité-prix en fabrication française
- ★📷 Drap Simonis 760 ou Strachan 777 inclus
- ★📷 Ardoise italienne monobloc de 19 mm
- ★📷 Bandes interchangeables brevetées
- 📷 Bandes en caoutchouc français
- 📷 Châssis bois massif renforcé
- 📷 Pieds en hêtre massif
- 📷 Finition laquée à la main
- 📷 6 boîtes insonorisées
- Votre couleur

**Prestige**
- ★ Le billard convertible le plus fonctionnel du marché
- ★ 12 couverts, allonge incluse
- ★📷 Châssis Woodstone
- ★📷 Réception centralisée et insonorisée
- 📷 Système de rangement Octopack
- 📷 Rangement des plateaux intégré
- 📷 Bandes interchangeables brevetées
- 📷 Ardoise italienne monobloc de 19 mm
- 📷 Drap Simonis 760 ou Strachan 777 inclus
- 📷 Bandes en caoutchouc français
- 📷 Pieds en bois massif
- Fabriqué dans le Gers

**Lafuge**
- ★ Le billard le plus personnalisable
- ★ Une pièce unique, faite à la main
- ★📷 Essences nobles massives
- ★ Ils nous ont choisis (références clients, uniquement sur Lafuge)
- 📷 Ardoise italienne jusqu'à 50 mm
- 📷 Bandes interchangeables brevetées
- Toutes les dimensions

## Lafuge (25/11)
- Deux listes : billard mixte et billard français (onglet « Lafuge contenus »).
- Ardoise : « jusqu'à 45 mm » en mixte, « jusqu'à 50 mm » en français.
- « Kotibé » retiré (absent des tarifs). L'ardoise n'est plus opposée au MDF sur Lafuge, car la fiche technique imprimée mentionne « MDF plaqué chêne » sur certains modèles.
- Français : « Bandes A37 toilées incluses dès 2,60 m » et « Chauffage de l'ardoise » (texte à valider).
- À mettre en avant à l'oral et dans les détails : multiplis plus résistant que le bois massif, plots Altuglas (effet de lévitation), cadre snooker (poches en cuir apparentes).

## Décisions du 27/11
- **3 points forts au maximum** par devis, chacun avec son texte et sa photo en gros plan. Ils sont pré-cochés par gamme (colonne « Proposé par défaut ») et le commercial peut en remplacer un. Les autres arguments s'impriment sous la ligne de l'option choisie (blocs « ARGUMENTS DES CHOIX » et colonne « Détail imprimé sur le devis »).
- **Phrase d'accroche** de gamme, en plus des 3 points forts :
  - Référence : « Le meilleur rapport qualité-prix du marché en 2,10 m », la taille standard du billard ;
  - Design : « Le billard convertible en table, laqué et fabriqué à la main dans notre atelier du Gers » (n'est plus « le meilleur rapport qualité-prix ») ;
  - Prestige : rangement intégré de tous les accessoires et des plateaux, réception des billes centralisée et insonorisée, allonge incluse pour recevoir jusqu'à 12 convives ;
  - Lafuge : « Le billard le plus personnalisable ».
- **Prestige** : le système de rangement Octopack et les bandes interchangeables (« et surtout ») passent avant le drap.
- **Bandes interchangeables brevetées** : photo à venir sous les fiches produit du site.
- **Photos des points forts** : elles arrivent au fur et à mesure sous les fiches produit du site.
- **Pack accessoires Référence** : valeur 300 €, à mettre en avant.
- **« Convertible » s'écrit toujours « convertible en table ».**
- **Atelier** : « dans notre atelier du Gers (Sud-Ouest) » pour Design et Prestige.
- **Réassurance** (bandeau de pictogrammes rouges) :
  - jamais le montage : soit le client l'a pris, soit il connaît son prix ;
  - toutes gammes : « 3e génération, famille d'ébénistes depuis 1946 » ;
  - Design et Prestige : « Fabrication à la main à Plaisance-du-Gers » (pas « Fabrication artisanale ») ;
  - Lafuge : « Fabrication artisanale » accepté ;
  - Référence : aucune mention d'origine.
- **Pourquoi on nous choisit** : le client veut un billard, il nous choisit parce que nous sommes les spécialistes du convertible. Le devis montre donc son billard en mode billard et en mode table.
