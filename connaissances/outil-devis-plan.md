# Outil de devis Billards de France — plan (v5, 19/11)

## Contexte
Aujourd'hui, chaque devis billard se monte à la main alors que la combinatoire est forte. On construit trois éléments :
1. un Google Sheet de tarifs et de contenus, qui fait foi ;
2. une page web de saisie, protégée par un mot de passe commun ;
3. un PDF épuré et premium, qui pousse le client à valider.

Les décisions détaillées (gammes, prix, conditions, charte, équipe) sont consignées dans `connaissances/` et `CLAUDE.md`. Ce plan ne garde que l'état d'avancement, les règles et l'étape en cours.

## Où on en est (phase A — données)
**Fait et poussé** :
- base de connaissances ;
- extraction du site ;
- grilles Design et Prestige ;
- accessoires (grille p. 11) et arguments du 19/11 ;
- Sheet en ligne à jour (Référence, Design, Prestige, Lafuge, Coloris, Accessoires, Mode d'emploi), relu le 19/11 ;
- 8 tests verts.

**Reste** :
1. **Les grilles papier Lafuge et livraison + montage.**
2. **Les photos ultra zoomées des arguments** (colonne Photo = « À fournir »).
3. **La relecture des arguments par l'équipe** : statut « À valider » → « Actif ».

Viennent ensuite la phase B (maquette du PDF), la phase C (page de saisie) et la phase D (installation et recette).

## Architecture (rappel, inchangée)
- **Application web Apps Script** liée au Sheet :
  - accès par mot de passe commun, sans compte Google ;
  - deux autorisations seulement : « ce tableur » et « images de billardsdefrance.fr / Drive » ;
  - aucun accès au Gmail.
- **PDF généré par le code** (pdfmake) : téléchargement en un clic.
- **Journal** des devis tenu dans le Sheet.
- **Boutons après génération** : email pré-rempli vers contact@, copie du récap CRM, copie de l'email client.
- **Sécurité** :
  - mot de passe haché et salé dans les propriétés du script ;
  - session de 8 h ;
  - blocage après 10 échecs ;
  - aucune donnée envoyée avant authentification.

## Règles du Sheet
- **Lecture** : par titre de bloc « ■ » et par nom de colonne, jamais par position.
- **Écriture** :
  - relire avant d'écrire ;
  - requêtes atomiques par onglet, un appel à la fois ;
  - ne jamais écraser une modification de l'équipe. Exemple à préserver : « Référence uniquement » dans Coloris.

## Étape faite : accessoires + arguments (19/11)

### Nouvelle logique des arguments dans l'outil
1. On choisit le produit. L'outil affiche la **liste des arguments de sa gamme** : ceux « Tous », plus ceux de la version, par exemple « Pieds métalliques ».
2. On **coche au maximum 4 arguments**, choisis selon ce qui parle à ce client. Les 4 arguments « proposés par défaut » sont pré-cochés, et on peut les changer.
3. **Arguments avec photo** : la photo ultra zoomée apparaît dans le PDF. **Arguments sans photo** : le texte seul, par exemple un positionnement de gamme.
4. Le PDF affiche exactement les 4 arguments cochés.

**Conséquences pour le Sheet** :
- nouvelle colonne **« Proposé par défaut »** (Oui / Non) dans chaque bloc ARGUMENTS & PHOTOS ;
- les **arguments par produit sont retirés**, car trop faibles : il ne reste que des arguments de gamme et de version ;
- la colonne « Valable pour » reste disponible pour personnaliser plus tard.

### Règles de rédaction
- **Concis et puissant**, sur le modèle « Bandes en caoutchouc toilé : un rebond vif et régulier ».
- **Aucune formule de remplissage** : ni « partie après partie », ni « même tard le soir », ni « dès la livraison », ni « effet surprise ».
- **Couleurs de tapis** : on annonce **26 couleurs** (Simonis et Strachan ont les mêmes couleurs).
- **Mots supprimés** : « rectifié pour une planéité parfaite » et « exclusivité ».
- **Bandes interchangeables** : écrire « plusieurs jeux sur un même billard : français, américain ou pool, à vous de choisir ».
- **Octopack** : c'est le **système** de rangement qui est inclus, pas les accessoires.

### Recherches faites
**Ardoise contre MDF** (sources multiples, surtout des fabricants et revendeurs) :
- l'ardoise est une pierre naturelle stable ;
- le MDF (panneau de fibres) gonfle et se déforme avec l'humidité et le temps ;
- une surface qui ondule fait dévier ou ralentir la bille ;
- l'ardoise garde sa planéité pendant des décennies, et toutes les tables professionnelles en sont équipées.

**Formica** :
- c'est un stratifié haute pression (norme EN 438), le matériau historique des plans de travail de cuisine ;
- le papier décor (mélaminé) n'est qu'une feuille collée ;
- Formica indique lui-même une résistance nettement inférieure du papier décor aux rayures, à l'usure et aux chocs.

### Arguments proposés
Légende : 📷 = avec photo zoomée à venir ; — = texte seul ; ★ = proposé par défaut.

**Référence**
| | Valable pour | Titre | Texte |
|---|---|---|---|
| — ★ | Tous | Le meilleur rapport qualité-prix du marché | Ardoise monobloc, structure en bois massif et pack accessoires inclus. |
| 📷 ★ | Tous | Ardoise monobloc de 19 mm | Une pierre naturelle d'un seul tenant : elle ne gonfle pas et ne se déforme pas avec l'humidité, contrairement au MDF. La bille roule droit, durablement. |
| 📷 ★ | Tous | Pack accessoires offert | 16 billes, 4 queues, triangle, craies, brosse et porte-queue inclus (valeur 330 €). |
| 📷 ★ | Pieds bois massif | Pieds bois massif et Formica | Le Formica, le matériau des plans de travail de cuisine : il résiste aux chocs, aux rayures et aux taches, là où le papier décor courant s'abîme. |
| 📷 ★ | Pieds métalliques | Pieds métalliques de 5 mm | Acier de 5 mm d'épaisseur, laqué époxy : une rigidité à toute épreuve. |
| 📷 | Tous | Châssis bois massif renforcé | Bois massif et renforts métalliques pour une stabilité maximale. |
| 📷 | Tous | 6 boîtes insonorisées | Les billes tombent sans bruit. |
| 📷 | Tous | Vérins de réglage | Une planéité parfaite, même sur un sol irrégulier. |
| 📷 | Tous | Bandes en caoutchouc toilé | Un rebond vif et régulier. |
| — | Tous | Billard et table à manger | Avec le plateau en 2 parties, une table pour 8 à 10 personnes. |

**Design**
| | Valable pour | Titre | Texte |
|---|---|---|---|
| — ★ | Tous | Le meilleur rapport qualité-prix en fabrication française | Un billard laqué, fabriqué à la main dans nos ateliers du Gers. |
| 📷 ★ | Tous | Drap Simonis 760 ou Strachan 777 inclus | Les draps des grandes compétitions internationales, en 26 couleurs, sans supplément. |
| 📷 ★ | Tous | Ardoise italienne monobloc de 19 mm | Une pierre naturelle d'un seul tenant, dans un schiste italien réputé pour sa densité : elle ne se déforme pas avec l'humidité, contrairement au MDF. |
| 📷 ★ | Tous | Bandes interchangeables brevetées | Plusieurs jeux sur un même billard : français, américain ou pool, à vous de choisir. |
| 📷 | Tous | Bandes en caoutchouc français | Un rebond précis, calibré pour chaque jeu. |
| 📷 | Tous | Châssis bois massif renforcé | Bois massif et renforts métalliques pour une stabilité maximale. |
| 📷 | Tous | Pieds en hêtre massif | Pieds carrés de 120 mm. |
| 📷 | Tous | Finition laquée à la main | Mate, satinée ou brillante. |
| 📷 | Tous | 6 boîtes insonorisées | Les billes tombent sans bruit. |
| — | Tous | Votre couleur | Laque dans la couleur RAL de votre choix. |

**Prestige**
| | Valable pour | Titre | Texte |
|---|---|---|---|
| — ★ | Tous | Le billard convertible le plus fonctionnel du marché | Rangements intégrés, réception centralisée des billes, allonge incluse. |
| — ★ | Tous | 12 couverts, allonge incluse | Avec le plateau bois, l'allonge de 45 cm est fournie. |
| 📷 ★ | Tous | Châssis Woodstone | Un bois haute densité aux fibres serrées : il absorbe le poids de l'ardoise sans fléchir et ne travaille ni avec l'humidité ni avec la température. |
| 📷 ★ | Tous | Réception centralisée et insonorisée | Goulottes capitonnées en 3 épaisseurs, un tiroir abattant de chaque côté. |
| 📷 | Tous | Système de rangement Octopack | Un système intégré sous le billard pour ranger queues, bandes, billes et craies. |
| 📷 | Tous | Rangement des plateaux intégré | Pendant la partie, les plateaux se rangent sous le billard. |
| 📷 | Tous | Bandes interchangeables brevetées | Plusieurs jeux sur un même billard : français, américain ou pool, à vous de choisir. |
| 📷 | Tous | Ardoise italienne monobloc de 19 mm | Une pierre naturelle d'un seul tenant, sur longerons métalliques : elle ne se déforme pas avec l'humidité, contrairement au MDF. |
| 📷 | Tous | Drap Simonis 760 ou Strachan 777 inclus | Les draps des grandes compétitions internationales, en 26 couleurs, sans supplément. |
| 📷 | Tous | Bandes en caoutchouc français | Un rebond précis, calibré pour chaque jeu. |
| 📷 | Tous | Pieds en bois massif | Chêne, hêtre ou tauari selon le modèle, teintés et vernis à la main. |
| — | Tous | Fabriqué dans le Gers | Bois massif teinté et verni à la main dans nos ateliers de Plaisance-du-Gers. |

**Lafuge**
| | Valable pour | Titre | Texte |
|---|---|---|---|
| — ★ | Tous | Le billard le plus personnalisable | Essence, teinte, laque RAL, dimensions, incrustations : chaque détail est à votre choix. |
| — ★ | Tous | Une pièce unique, faite à la main | Fabriquée à l'unité par un seul ébéniste, du début à la fin, à Miribel-les-Échelles. |
| 📷 ★ | Tous | Essences nobles massives | Chêne, érable, noyer, mélèze ou kotibé. |
| — ★ | Tous | Ils nous ont choisis | Yacht Club de Monaco, Sheraton Paris, villas prestigieuses de la Côte d'Azur et de la côte atlantique. |
| 📷 | Tous | Ardoise italienne jusqu'à 50 mm | Une pierre naturelle épaisse : elle ne se déforme pas avec l'humidité, contrairement au MDF. |
| 📷 | Tous | Bandes interchangeables brevetées | Plusieurs jeux sur un même billard : français, américain ou pool, à vous de choisir. |
| — | Tous | Toutes les dimensions | Du 7 pieds au snooker 12 pieds, jusqu'au billard russe. |

**Correction** : « bandes interchangeables offertes » est supprimé. L'information venait du résumé d'entreprise fourni au départ (« offert pour les projets multi-jeux »). Il faut aussi la corriger dans `lafuge.md` et `entreprise.md`.

### Accessoires & mobilier (page 11)
Une ligne par référence, avec une nouvelle colonne « Réf. ».
- **Toutes gammes, Actif** :
  - jeu de 7 éléments 250 € ;
  - 16 billes US ou pool + triangle + règle 80 € ;
  - 3 billes françaises + règle 35 € ;
  - 16 billes US ou pool seules 60 € ;
  - triangles 20 € ;
  - boîtes de 12 craies (4 couleurs) 8 € ;
  - brosse 22 € ;
  - clé 6 pans 20 € ;
  - règle de jeux 20 € ;
  - porte-queue simple 20 € ;
  - porte-queues avec horloge 189 € ;
  - queues classiques 100 / 120 / 140 cm 50 € ;
  - queue luxe américaine 95 € ;
  - queue luxe pool frêne 50 € ;
  - queue luxe française 70 € ;
  - queues fibre de verre 120 cm 60 € et 140 cm 65 € ;
  - protection PVC des dessus 80 € ;
  - équerre de rangement des dessus et de l'allonge 150 €.
- **Design et Prestige** : rehausse de pieds carrés 200 €.
- **Inchangé** : banc laqué 740 €.
- **Non repris** :
  - grand dessus MDF ;
  - tissu au mètre ;
  - poches en cuir ;
  - finition brut ;
  - laque Prestige ;
  - billard de 1,90 m ;
  - supplément teinte.

### Production (après validation)
1. **Connaissances** :
   - nouveau `accessoires.md` ;
   - nouveau `arguments.md` : la liste ci-dessus et les règles de rédaction ;
   - corrections : Lafuge « offert », 26 couleurs, caractéristiques 2,10 m, points du site à corriger (fiche Panama « assemblé en France », vernis de la fiche New-York).
2. **Trace** :
   - `arguments_brouillons.py` et `construire_sheet.py` : colonne « Proposé par défaut », plus d'arguments par produit, onglet Accessoires ;
   - tests : au plus 4 arguments par défaut par gamme et par version ; aucune formule de remplissage ; aucun « offert » côté Lafuge ; au moins 1 argument avec photo prévue par gamme.
   - commit et push.
3. **Sheet en ligne**, un appel atomique par onglet, après relecture :
   - réécriture des 4 blocs ARGUMENTS : colonne « Proposé par défaut », lignes par produit retirées, 6 lignes vides conservées ;
   - onglet Accessoires.
4. **Contrôle** : relecture complète et compte rendu.

**Fait le 19/11** : les 4 étapes. En ligne, la règle de mise en forme « Masqué » des blocs Arguments pointait sur la colonne Photo au lieu de Statut : corrigée. Le mode d'emploi en ligne reprend la nouvelle logique des arguments.

## Vérification
- **Phase A** :
  - `devis/tests/test_sheet.py` vert ;
  - relecture du Sheet en ligne après chaque requête ;
  - aucune valeur de l'équipe écrasée.
- **Phases B et C** : banc Playwright avec 5 scénarios, contrôles des totaux, de l'échéancier, de la règle Oney, des règles Référence et Lafuge, de **la sélection de 4 arguments au maximum** et des liens cliquables.
- **Apps Script** : mot de passe, blocage, Journal, autorisations limitées.
