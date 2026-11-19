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
