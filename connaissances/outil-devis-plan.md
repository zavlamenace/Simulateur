# Outil de devis Billards de France — plan (v8, 26/11) : publication Lafuge + page de création de devis

## Avancement au 26/11
La page de création de devis est **écrite et testée**, avec les décisions de l'utilisateur (questions déjà posées et tranchées).

**Fait :**
- `devis/appscript/` :
  - `Code.gs` : connexion, sessions, journal, versions ; fonctions d'administration réservées au propriétaire depuis l'éditeur ;
  - `calcul.js` (moteur) ;
  - `Index`, `Styles`, `App`, `Pdf` ;
  - `Calcul` et `Logos` produits par `devis/outils/assembler_appscript.py` ;
  - `appsscript.json` (droits : ce tableur seulement, plus l'email de l'utilisateur pour le contrôle propriétaire).
- `devis/logos/` : logos BdF (PNG) et Lafuge (SVG).
- **Banc d'essai `devis/banc/`** :
  - le vrai Code.gs tourne dans Node (`appsscript-simule.js`) ;
  - `serveur.js` sert la page ;
  - `exporter_catalogue.py` produit `catalogue.json` et `feuilles.json`.
- **Tests verts** :
  - 24 tests JS, dont les 5 parcours Playwright : Référence, Design RAL + plateau, Prestige remises + V2, Chambord 12 pieds, Lafuge français sur téléphone 390 px ;
  - 15 tests Python.
- **Corrections** :
  - mention Lafuge « Billard vendu hors accessoires », sans « rien n'est offert » (trace et `conditions.md`) ;
  - fiche technique : lignes propres à une taille filtrées ;
  - « Mention » affichée en tête de fiche.
- **Sheet en ligne, 26/11** :
  - « Lafuge contenus » : « Forme des pieds (City) | Biseautés » (mixte et bandes françaises) ;
  - « Mention accessoires » des deux onglets Lafuge : « Billard vendu hors accessoires ».

## Reste à faire
- **Installation dans Apps Script** (phase D), avec l'utilisateur : `devis/appscript/INSTALLATION.md`.
  - 26/11 : la page est déployée, mais la connexion répondait « Mot de passe non défini ».
  - Correction : le mot de passe se saisit désormais dans Paramètres du projet > Propriétés du script (`MOT_DE_PASSE`), sans modifier le code.
  - Ajout d'un diagnostic, `verifierInstallation`.
- **Adresse courte** `devis.billardsdefrance.fr` (validée le 26/11) : redirection Cloudflare vers l'adresse `/exec`, décrite dans INSTALLATION.md.
- **Journal, suivi commercial (26/11)** : trois colonnes ajoutées automatiquement par l'outil.
  - « Suivi », liste déroulante : Envoyé, En réflexion, À relancer, Relancé, En négociation, Validé (bon pour accord), Acompte reçu, Perdu, Sans suite, Remplacé par une nouvelle version.
  - « Prochaine relance », une date.
  - « Note de suivi ».
  - Règles automatiques : « Envoyé » à la génération ; une version précédente encore en cours passe à « Remplacé par une nouvelle version » quand la suivante est générée.
- **Retours du 26/11** :
  - champ de précision (RAL, teinte) élargi ;
  - remise affichée en % ou en € ;
  - livraison « par messagerie au pied de la porte » (Sheet mis à jour).
- **Simonis 330** : mêmes couleurs que le Simonis 760 (26/11). Le renvoi est dans le bloc « DRAPS » de l'onglet Coloris, en ligne et dans la trace.
- **Retours de l'équipe** sur l'ergonomie et sur le PDF provisoire (captures envoyées le 26/11).
- **Ensuite** :
  - grille montage ;
  - PDF premium (phase B) : storytelling, photos.

## Contexte
**Lafuge** :
- Les tarifs sont transcrits et contrôlés (commit poussé) : seuls écarts avec les 4 documents, les corrections validées ; HT = TTC ÷ 2.
- L'aperçu a été vu. L'utilisateur demande de publier, avec trois retouches :
  1. lisibilité des bandes initiales ;
  2. fiches techniques ;
  3. drap Simonis 330 inclus pour le billard français.

**Phase C** : la page de création de devis des commerciaux, « la plus simple et la plus intuitive possible ».
- Le PDF reste provisoire (propre et sobre). La mise en page premium (storytelling, photos) viendra ensuite.

**Lien du Sheet** : https://docs.google.com/spreadsheets/d/1_MZBcXsz-DqXfk_hN1X1WY5_9wfMXTx9I52tOmSEooY/edit
- Les onglets Lafuge sont en ligne depuis le 25/11.

## Partie 1 — Publication Lafuge

### Retouches avant publication
- **Bandes initiales** (`devis/outils/lafuge_tarifs.py`, `jeux_mixte`) :
  - groupe renommé « Bandes initiales (une au choix, incluse) » ;
  - condition : « Une seule au choix, incluse dans le prix ; le 2e jeu de bandes est en option (dès 860 €) » ;
  - sur le 2e jeu de bandes : « Jeu d'un autre type que les bandes initiales ».
- **Fiches techniques** (onglet « Lafuge contenus ») : colonnes Ordre | Fiche | Élément | De base | En option | Version laquée.
  - « De base » : uniquement la matière affichée sous le titre de la fiche. Exemples : Loft = érable sycomore massif ; Soho = MDF plaqué chêne.
  - « En option » : les essences massives proposées sur la fiche, déduites de ses options. Exemples :
    - Loft : « Chêne massif ou mélèze massif ; noyer sur demande » ;
    - Soho : « Chêne massif ou mélèze massif ».
  - Un élément en métal porte la mention « Inchangé (acier) ».
- **Drap du billard français** : « Simonis 330 inclus » (Gamme et `connaissances/coloris.md`).
- **Tests** : vérifier que « De base » ne contient jamais « ou » entre deux essences, et que « En option » liste les essences de la fiche.
- Retour centralisé des billes : déjà réservé à Compétition et Chambord (inchangé).

### Écriture en ligne
Étapes, après relecture des onglets existants :
1. Importer le xlsx dans un classeur temporaire et copier les 3 onglets dans le Sheet. Repli : écriture par blocs.
2. Reporter les arguments.
3. Supprimer l'ancien onglet squelette « Lafuge », après comparaison.
4. Ajouter les 47 accessoires Lafuge dans « Accessoires & mobilier » (insertion de lignes).
5. Mettre à jour le mode d'emploi (convention des cases ; « Nécessite » avec plusieurs noms = l'un d'eux).
6. Créer le classeur « BdF – Tarifs revendeurs HT (confidentiel) », non partagé.
7. Mettre à jour les connaissances : `lafuge.md`, `a-verifier.md`, `conditions.md`, `arguments.md`, `coloris.md`, `CLAUDE.md` (lien du classeur HT, règle de confidentialité).
8. Commit et push.

## Partie 2 — Page de création de devis (phase C)

### Décisions de l'utilisateur
- **Appareils** :
  - ordinateur de bureau ;
  - téléphone (devis pendant l'appel ou après, moins de 10 par semaine).
- **Une seule page**, avec des **sections qui s'ouvrent au fur et à mesure**. Le **total se met à jour en direct** : panneau à droite sur ordinateur, barre fixe en bas sur téléphone.
- **Client** :
  - nom, prénom, téléphone, email ;
  - adresse complète (code postal et ville en premier, rue facultative au stade du devis) ;
  - origine du contact.
- **Un seul billard par devis**, plus des accessoires.
- **Prix de chaque option entre parenthèses**, partout.
- **Remises** :
  - par ligne et globale ;
  - en % ou en € ;
  - prix d'origine barré ;
  - rien n'apparaît s'il n'y a pas de remise.
- **Lignes libres** : libellé + prix unitaire (positif ou négatif) + **quantité**.
- **Livraison** : offerte au pied de la porte par défaut ; « Livraison et montage » avec un prix saisi à la main. Branchement sur l'onglet montage quand la grille existera.
- **Numérotation** : BDF-2026-0001. Une nouvelle version devient BDF-2026-0001-2. Le n° du logiciel de facturation reste un champ facultatif.
- **Bouton « Enregistrer »** : brouillon dans le Journal, repris depuis n'importe quel appareil.
- **Rouvrir un devis** depuis le Journal : il repart en nouvelle version.
- **Après génération** :
  - télécharger le PDF ;
  - copier le récap CRM.
- **Pas de photo dans la page**, pour qu'elle reste légère.
- **Ordre** : la page d'abord, avec un PDF provisoire ; la maquette premium ensuite.

### Déroulé de la page (sections)
1. **Devis réalisé par** : liste des 4 personnes, mémorisée sur l'appareil. Puis le client, l'origine du contact et le n° de facturation (facultatif).
2. **Billard** :
   - gamme : Référence, Design, Prestige, Lafuge mixte, Lafuge bandes françaises ;
   - modèle ;
   - version ou taille, seules les tailles proposées étant cliquables ;
   - pour Lafuge mixte, bandes initiales.
3. **Options** :
   - par groupe, avec le prix entre parenthèses pour la taille choisie ;
   - règles « Un seul par groupe », « Nécessite » et « Exclut » appliquées en direct (option grisée avec la raison) ;
   - « Inclus » affiché sans prix ;
   - « Sur demande » ou case vide : champ de prix à saisir, obligatoire avant le PDF.
4. **Tapis** : couleur selon la gamme (onglet Coloris). Billard français : Simonis 330, couleur en texte libre en attendant la liste.
5. **Plateau** (si le modèle existe en version table), puis suppléments verre et rallonge selon les règles.
6. **Accessoires** : catalogue de la gamme, avec quantités.
7. **Lignes libres** : libellé, prix, quantité.
8. **Livraison** : offerte, ou livraison et montage (prix saisi).
9. **Remises** : par ligne (dans chaque ligne du récapitulatif) et globale.
10. **Arguments** : 4 au maximum, les « proposés par défaut » pré-cochés.
11. **Récapitulatif** :
    - lignes, remises, total TTC, TVA (TTC ÷ 6) ;
    - échéancier (Plaisance 30 % puis solde ; Lafuge 30 / 30 / solde) ;
    - encadré Oney si le total ≤ 3 000 € ;
    - validité 30 jours ;
    - boutons « Enregistrer » et « Générer le PDF ».

### Architecture (déjà validée, rappel)
- **Application web Apps Script** liée au Sheet, exécutée avec le compte propriétaire.
  - Mot de passe commun haché et salé dans les propriétés du script ; session de 8 h ; blocage après 10 échecs.
  - Aucune donnée avant authentification ; autorisations : ce tableur seulement.
- **Serveur** (`Code.gs`) :
  - lecture du Sheet par blocs « ■ » et noms de colonnes : portage de `devis/outils/lire_sheet.py`, relu à chaque ouverture de la page (pas de cache : une modification du Sheet est visible immédiatement) ;
  - compteur de références protégé par LockService ;
  - écriture du Journal : statut Brouillon ou Généré, version, configuration complète en JSON pour la reprise.
- **Calcul des prix** dans un module JavaScript pur (`calcul.js`), commun à la page et aux tests : options, règles, remises, échéancier, TVA.
- **PDF provisoire** généré dans le navigateur (pdfmake, EB Garamond / DM Sans) :
  - logos selon la gamme : BdF seul pour Plaisance ; BdF + Lafuge, avec la mention de groupe, pour Lafuge ;
  - lignes, remises, total, échéancier, arguments cochés ;
  - fiche technique Lafuge selon les options ;
  - « hors accessoires » pour Lafuge ;
  - lien « Je valide mon devis » (email pré-rempli vers contact@) et « Appeler mon conseiller » ;
  - mention « CGV sur billardsdefrance.fr ».
- Toutes les règles de `CLAUDE.md` s'appliquent (Référence sans origine, références clients seulement sur Lafuge, aucune mention qui rend frileux, etc.).
- **Interface** : charte du site (EB Garamond, DM Sans, encre, crème, sable), rouge réservé à « Générer le PDF », aucun gadget.

### Fichiers
- **`devis/appscript/`** :
  - `Code.gs` : serveur ;
  - `Index.html` (structure), `Styles.html`, `App.html` (interface) ;
  - `calcul.js` (moteur de prix, inclus aussi dans `App.html`) ;
  - `Pdf.html` (PDF provisoire) ;
  - `appsscript.json` (autorisations minimales) ;
  - `INSTALLATION.md` : copier les fichiers dans Extensions > Apps Script du Sheet, définir le mot de passe, déployer en application web.
- **`devis/banc/`** : banc d'essai local.
  - Il sert la page avec un faux `google.script.run` alimenté par le xlsx de trace, lu par `lire_sheet.py` puis exporté en JSON.
  - Tests Playwright, 5 scénarios :
    1. Référence simple ;
    2. Design avec RAL et plateau ;
    3. Prestige avec remise par ligne et remise globale ;
    4. Lafuge mixte Chambord 12 pieds avec une option sur demande et une ligne libre en quantité 2 ;
    5. Lafuge français avec A37 et chauffage.
  - Vérifié pour chacun : totaux, règles, 4 arguments au maximum, brouillon puis reprise en V2, PDF généré, récap CRM, affichage téléphone (390 px).
- **Tests unitaires** de `calcul.js` (Node).

### Hors de cette étape
- Grille montage (saisie manuelle en attendant) et liste des couleurs Simonis 330.
- PDF premium (phase B) et photos zoomées.
- Installation dans Apps Script (phase D), avec l'utilisateur : le code ne peut pas être déployé depuis cette session ; guide pas à pas fourni.

## Vérification
- `devis/tests/test_sheet.py` et `test_lafuge.py` verts après les retouches Lafuge ; relecture en ligne de chaque bloc publié.
- Tests unitaires du moteur de calcul et les 5 scénarios Playwright verts.
- Captures ordinateur et téléphone envoyées à l'utilisateur pour validation de l'ergonomie.

---

# Outil de devis — plan v9 (26/11) : retours de test, arguments liés aux choix, storytelling Lafuge

## Contexte
L'utilisateur a testé la page déployée. Il demande :
- des corrections (journal, livraison Lafuge, couleurs, zones de saisie, entrées de poche) ;
- des photos d'accessoires ;
- un accès sans compte Google pour les collègues ;
- des arguments qui apparaissent selon les choix ;
- une liste d'arguments Lafuge appuyés par des faits trouvés sur internet ;
- la définition du bloc histoire/storytelling Lafuge.

L'historique des versions précédentes est dans `connaissances/outil-devis-plan.md`.

**Décisions du 26/11 (réponses de l'utilisateur) :**
- **Suivi du Journal** : liste validée. Les colonnes « Prochaine relance » et « Note de suivi » sont refusées. Les automatismes sont validés : « Envoyé » à la génération, « Remplacé par une nouvelle version ».
- **Lafuge** : jamais de livraison offerte. Livraison et montage uniquement par nos équipes ou par des équipes formées par nous, en France. Prix saisi à chaque devis.
- **Arguments liés aux choix** : imprimés **sous la ligne de l'option choisie**. Les 4 « points forts » de gamme restent à part.
- **Gris** : sur le **Simonis seulement** (760, donc aussi 330), on garde Gris clair, Gris ardoise et Noir.
- **Photos d'accessoires** : maintenant, depuis billardsdefrance.fr uniquement, avec validation par l'utilisateur avant affichage.
- **Accès** : le lien doit marcher pour tous les collègues, avec un autre compte Google ou sans compte.

## Avancement (reprise après redémarrage)
**Fait en local, pas encore commité :**
- `Code.gs` : Journal sans « Prochaine relance » ni « Note de suivi ».
- `calcul.js` :
  - `formulesLivraison`, `livraisonOfferte(cat, g)`, `livraisonMontage`, `formuleLivraison` ;
  - Lafuge forcé en « Livraison et installation par nos équipes », prix obligatoire.
- `App.html` : carte livraison selon la gamme, `harmoniser()` force la formule, « Sans entrées de poche en cuir ».
- `lafuge_tarifs.py` : groupe `POCHES_CUIR`, « Un seul par groupe », sans Nécessite.
- `construire_sheet.py` : livraison Lafuge, offerte limitée à Plaisance, Gris clair, Gris requin masqué.
- Trace et `catalogue.json` régénérés, `a-copier/` réassemblé.
- Tests : 27/27 JS (dont livraison Lafuge, cuir exclusif, largeur ≥ 250 px, gris) et Python verts.

**Fait en ligne :** « Livraison & montage »!E6 = « Référence, Design, Prestige ».

**À refaire en ligne** (appels interrompus par le redémarrage ; relire avant d'écrire) :
- « Livraison & montage »!A10:G10 : nouvelle formule Lafuge (ligne 10 vide à la relecture) ;
- Coloris!B32:F33 : « Gris » → « Gris clair » (#A7ADB0) ; « Gris requin » → Masqué, note « N'existe pas (26/11) » ;
- « Lafuge mixte » : lignes « Entrées de poche en cuir noir » et « Cuir de couleur (gamme SOFIC) » de chaque fiche :
  - Groupe → « Entrées de poche en cuir » ;
  - Choix → « Un seul par groupe » ;
  - Nécessite → vide ;
  - Conditions du SOFIC → « Cuir noir ou cuir de couleur : l'un ou l'autre ».

  Lire A:B pour trouver les lignes, et la ligne d'en-têtes pour les colonnes.

**Puis :**
- connaissances : `coloris.md`, `conditions.md` (livraison Lafuge), `outil-devis-plan.md` ;
- commit et push ;
- envoi des fichiers `a-copier/` modifiés : Code, Calcul, App, et Styles s'il a changé ;
- ensuite les sections 2, 3 et 4.

## 1. Corrections
Toujours **relire en ligne avant d'écrire** ; écritures ciblées ; mise à jour de la trace (`construire_sheet.py`, `lafuge_tarifs.py`) et des tests.

- **Journal** (`Code.gs`) : retirer « Prochaine relance » et « Note de suivi » de `ENTETES_JOURNAL`. On garde « Suivi », sa liste déroulante et les deux automatismes ; tests du serveur adaptés.
- **Livraison Lafuge** :
  - **Sheet**, onglet « Livraison & montage » :
    - ajouter la formule « Livraison et installation par nos équipes » : Gammes compatibles « Lafuge », Prix TTC vide (saisi), Actif ;
    - texte du détail, à valider : « Par nos équipes ou par des installateurs formés par nos soins, partout en France : acheminement jusqu'à la pièce, pose de l'ardoise, mise à niveau et réglages » ;
    - la formule offerte passe en « Référence, Design, Prestige ».
  - **Moteur** (`calcul.js`) :
    - une formule n'est retenue que si elle est compatible avec la famille de la gamme ;
    - pour Lafuge, la livraison est forcée sur cette formule (aussi dans `harmoniser()` à la réouverture d'un ancien devis), avec prix obligatoire dans `problemes()`.
  - **Page** : la section Livraison ne montre que cette carte et le champ prix.
  - **Tests** : le Lafuge n'a jamais de ligne « offerte » ; le PDF est bloqué sans prix.
- **Couleurs Simonis 760**, onglet Coloris :
  - « Gris » → « Gris clair » ;
  - « Gris requin » → Statut « Masqué ». Règle du Sheet : on masque, on ne supprime pas ;
  - le Strachan 777 ne change pas ;
  - le Simonis 330 suit automatiquement (bloc DRAPS) ;
  - mettre à jour `coloris.md`.
- **Zones de saisie** : toutes en pleine largeur (précision, teinte, prix à saisir, prix du billard, montage, lignes libres).
  - Vérifier dans le banc la précision « Teinte incluse » Lafuge, et ajouter un test qui mesure la largeur (≥ 250 px sur ordinateur).
  - Rappeler à l'utilisateur de recoller **Styles** : la capture laisse penser que l'ancien est encore déployé.
- **Entrées de poche** (Lafuge mixte) : un choix exclusif.
  - Créer un groupe « Entrées de poche en cuir », « Un seul par groupe », sans Nécessite :
    - « Entrées de poche en cuir noir » (480 €) ;
    - « Cuir de couleur (gamme SOFIC) » (990 €) ;
    - plus la ligne « Sans entrées de poche en cuir ».
  - Les boîtes élasthanne restent dans « Poches ».
  - Écriture en ligne :
    - mettre à jour les cellules Groupe, Choix et Nécessite de chaque bloc fiche concerné ;
    - en un seul `update_spreadsheet` après relecture ;
    - vérifier qu'aucun « Exclut » ne vise l'ancien groupe.
  - Mettre à jour `lafuge_tarifs.py` et `test_lafuge.py`.
- **Accès pour tous** (`INSTALLATION.md` et vérification avec l'utilisateur) :
  - le déploiement doit être « Exécuter en tant que : Moi » et « Qui a accès : **Tout le monde** », et non « Tout le monde disposant d'un compte Google » ;
  - test sur un téléphone en 4G sans compte Google, puis dans une fenêtre privée déconnectée ;
  - si le compte est un Google Workspace qui interdit l'accès anonyme, solution de repli à étudier avec l'utilisateur ;
  - l'adresse courte devis.billardsdefrance.fr (redirection Cloudflare) est déjà documentée.

## 2. Arguments liés aux choix (sous la ligne)
- **Sheet**, onglet « Lafuge contenus » : nouveau bloc « ■ ARGUMENTS DES CHOIX », colonnes Choix | Texte imprimé sous la ligne | Source | Statut.
  - « Choix » vaut l'une de ces valeurs :
    - un nom d'option (Chêne massif, Noyer massif, Bandes A37 toilées, bandes initiales, 2e jeu de bandes, plateaux encastrés, plateau simple…) ;
    - un drap (Simonis 760, Strachan 777, Simonis 330) ;
    - une matière de base (Érable sycomore massif), imprimée sous la ligne du billard.
  - Un seul endroit, lisible par l'équipe : on évite de recopier le texte dans les 19 fiches des deux onglets.
- **Moteur** (`calcul.js`, `lignes()`) :
  - détail d'une ligne = « Détail imprimé » de l'option s'il existe, sinon le texte du bloc ;
  - ligne du drap Lafuge = texte du drap ;
  - ligne du billard = dimensions, puis le texte de la matière de base si aucune essence n'est choisie.
  - Seuls les textes au statut « Actif » sont imprimés. Les brouillons « À valider » restent invisibles sur le devis.
- **Textes de départ** (idées de l'utilisateur, à étayer par la recherche) :
  - chêne, érable et noyer massifs français ;
  - bandes A37 : le meilleur caoutchouc du marché ;
  - autres bandes : caoutchouc français premium ;
  - Simonis et Strachan : les leaders mondiaux ;
  - plateaux encastrés : ne font qu'un avec le billard ;
  - plateau : billard transformé en table en une minute ;
  - bandes interchangeables brevetées : deux jeux sur un seul billard, sur les mixtes uniquement.

## 3. Recherche, liste d'arguments Lafuge et storytelling (livrable à valider)
- **Sources internes** : `connaissances/` (lafuge.md, arguments.md, storytelling.md, entreprise.md), le Sheet, tout ce qui a été dit en conversation.
- **Recherche web (WebSearch / WebFetch)**, avec un fait concret sourcé (lien) par argument :
  - Simonis : histoire, compétitions officielles (UMB, WPA) ;
  - Strachan : snooker, World Snooker ;
  - bandes A37 : fabricant, usage en compétition ;
  - caoutchouc français ;
  - forêt française de chêne (ONF, IGN) ;
  - érable sycomore ;
  - noyer du Dauphiné et de l'Isère, proches de Miribel-les-Échelles ;
  - ardoise italienne de Ligurie ;
  - brevet des bandes interchangeables (Google Patents, INPI) ;
  - histoire de Lafuge et de l'atelier de Chartreuse ;
  - éventuels labels (Entreprise du patrimoine vivant…).
  - **Règle** : on n'écrit rien qu'on ne peut pas prouver. Un argument non vérifié est signalé comme tel.
- **Livrable 1 : liste complète des arguments Lafuge** :
  - arguments de gamme et arguments liés aux choix ;
  - chacun avec son texte court pour le devis, le fait qui le prouve et la source ;
  - plus les nouveaux arguments trouvés (labels, origine des essences, poids, durée de vie, accompagnement architecte, pyramide russe, etc.).
- **Livrable 2 : bloc storytelling Lafuge** :
  - place dans le PDF ;
  - structure : un titre, puis trois temps courts (le lieu, la main, le temps), tournés vers le client ;
  - brouillon de texte et photos nécessaires ;
  - mêmes garde-fous que `CLAUDE.md`.
- **Restitution** : dans `connaissances/arguments.md` et `connaissances/storytelling.md`, plus un résumé dans la conversation. L'utilisateur valide avant toute écriture en ligne (textes au statut « À valider » jusque-là).

## 4. Photos des accessoires
- Relier chaque accessoire du Sheet à sa fiche sur billardsdefrance.fr, par sa référence (colonne « Réf. »), à défaut par son nom.
- Récupérer l'adresse de la photo principale.
- Présenter un tableau de validation (miniatures et produits correspondants), en signalant les accessoires sans photo (Lafuge, sans doute).
- **Après validation** :
  - écrire les adresses dans la colonne « Photo » de l'onglet Accessoires (écritures ciblées) ;
  - la page affiche une miniature de 48 px, chargée seulement à l'ouverture de la catégorie, pour rester légère ;
  - aucune photo n'est imprimée sur le PDF provisoire.

## Fichiers touchés
- **Code** : `devis/appscript/` (`Code.gs`, `calcul.js`, `App.html`, `Styles.html`, puis `assembler_appscript.py` pour `a-copier/`).
- **Trace et tests** : `devis/outils/construire_sheet.py`, `lafuge_tarifs.py`, `devis/banc/tests/*`, `devis/tests/test_lafuge.py`.
- **Connaissances** : `coloris.md`, `conditions.md`, `arguments.md`, `storytelling.md`, `outil-devis-plan.md`, `a-verifier.md`.

## Vérification
- Tests JS : moteur, serveur, parcours Chromium. Nouveaux cas :
  - Lafuge sans livraison offerte, avec prix de montage obligatoire ;
  - entrées de poche exclusives ;
  - largeur des champs ;
  - gris du Simonis ;
  - textes sous la ligne affichés seulement au statut « Actif ».
- Tests Python verts.
- Relecture en ligne des cellules écrites.
- Envoi à l'utilisateur :
  - fichiers modifiés de `a-copier/` à recoller ;
  - captures et PDF d'exemple ;
  - liste d'arguments et brouillon storytelling à valider ;
  - tableau des photos à valider.
- Commit et push sur `claude/billiard-quote-tool-1wrwy3`.
