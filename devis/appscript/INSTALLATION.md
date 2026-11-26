# Installer la page de devis (Apps Script)

Comptez 20 minutes environ, avec le compte Google propriétaire du Sheet « BdF – Tarifs & contenus ».
Les commerciaux n'ont pas besoin d'accès au Sheet : seule la page le lit, avec le compte propriétaire.

## 1. Ouvrir l'éditeur
1. Ouvrir le Sheet, puis **Extensions > Apps Script**.
2. Renommer le projet « Devis Billards de France ».

## 2. Copier les fichiers
Les 8 fichiers à coller sont réunis dans `devis/appscript/a-copier/`. Pour créer un fichier HTML : bouton **+** > **HTML**, puis le nommer sans « .html ». Dans chaque fichier : tout sélectionner, puis coller par-dessus.

| Fichier de `a-copier/` | Dans l'éditeur |
|---|---|
| `Code.gs` | `Code.gs` |
| `Index.html` | `Index` |
| `Styles.html` | `Styles` |
| `Calcul.html` | `Calcul` |
| `Logos.html` | `Logos` |
| `Pdf.html` | `Pdf` |
| `App.html` | `App` |
| `appsscript.json` | voir l'étape 3 |

Les noms doivent être exactement ceux-ci, majuscule comprise : `Index` appelle les autres par leur nom.

**Enregistrez** (icône disquette, ou Cmd+S / Ctrl+S) après chaque collage. Un fichier non enregistré n'entre pas dans le déploiement.

## 3. Manifeste
1. **Paramètres du projet** (roue dentée) : cocher « Afficher le fichier manifeste "appsscript.json" dans l'éditeur ».
2. Ouvrir `appsscript.json` dans l'éditeur, coller le contenu de `a-copier/appsscript.json` par-dessus, puis enregistrer.

Autorisations demandées :
- ce tableur seulement ;
- l'adresse email du compte, qui sert à réserver les fonctions d'administration au propriétaire.

## 4. Mot de passe de l'équipe
Aucune modification du code n'est nécessaire.
1. Dans l'éditeur Apps Script, ouvrir **Paramètres du projet** (roue dentée, à gauche).
2. Tout en bas, dans **Propriétés du script**, cliquer **Ajouter une propriété du script** (ou **Modifier les propriétés du script**).
3. Propriété : `MOT_DE_PASSE` (en majuscules). Valeur : le mot de passe choisi, de 10 caractères au moins.
4. **Enregistrer les propriétés du script**.

À la première connexion sur la page, le mot de passe est haché et salé, puis la valeur en clair est effacée des propriétés.

Pour le changer plus tard, recréer la propriété `MOT_DE_PASSE` avec la nouvelle valeur. Toutes les sessions ouvertes sont alors fermées.

**En cas de doute**, choisir `verifierInstallation` dans la liste en haut de l'éditeur, puis **Exécuter**. Le journal d'exécution indique :
- le classeur lu ;
- l'état du mot de passe ;
- les onglets lus par la page ;
- l'état du Journal.

## 5. Déployer
1. **Déployer > Nouveau déploiement**, type **Application Web**.
2. Description : « Devis v1 ».
3. **Exécuter en tant que** : Moi. **Qui a accès** : **Tout le monde**, et non « Tout le monde disposant d'un compte Google ». Les collègues ouvrent ainsi la page sans compte Google, ou avec leur propre compte ; seul le mot de passe de l'équipe est demandé.
4. Copier l'URL de l'application Web (elle finit par `/exec`).
5. La transmettre à l'équipe avec le mot de passe, par un canal privé.

## 6. Premiers contrôles
0. **Accès** : ouvrir l'adresse sur un téléphone en 4G, sans être connecté à Google. La page de connexion doit s'afficher directement. Si Google demande de se connecter, le réglage « Qui a accès » n'est pas sur « Tout le monde » : corriger dans Déployer > Gérer les déploiements.
1. **Sur ordinateur** :
   - ouvrir l'URL et se connecter ;
   - faire un devis Référence complet, puis **Générer le PDF** ;
   - vérifier que le PDF se télécharge et qu'une ligne apparaît dans l'onglet « Journal ».
2. **Sur téléphone** : même parcours. Si le téléchargement ne démarre pas, utiliser **Ouvrir le PDF dans un onglet**.
3. **Récap CRM** : cliquer **Copier le récap CRM**, puis coller dans le CRM.

## Adresse courte : devis.billardsdefrance.fr
La page Apps Script ne peut pas s'afficher sous votre nom de domaine. L'adresse courte **redirige** vers son adresse `/exec`.

Le site passe par Cloudflare. Si le domaine est géré dans Cloudflare :
1. **DNS > Enregistrements > Ajouter** :
   - type `AAAA`, nom `devis`, contenu `100::` ;
   - proxy activé (nuage orange).
2. **Règles > Redirect Rules > Créer une règle** :
   - nom « Devis » ;
   - condition « Nom d'hôte égal à `devis.billardsdefrance.fr` » ;
   - URL statique : l'adresse `/exec` de l'étape 5, code 302 ;
   - **Déployer**.
3. Tester `https://devis.billardsdefrance.fr` dans une fenêtre de navigation privée.

Une redirection « masquée » (cadre) ne fonctionne pas : Google refuse de s'afficher dans le cadre d'un autre site.

La page est protégée par le mot de passe, et non par le secret de son adresse.

## Mettre à jour la page
- **Code** :
  1. recoller les fichiers modifiés depuis `a-copier/` et enregistrer ;
  2. **Déployer > Gérer les déploiements**, crayon, Version « Nouvelle version », **Déployer** ;
  3. l'URL ne change pas.
- **Contenus** : prix, options, arguments, équipe et paramètres se modifient dans le Sheet. Rien à redéployer : la page relit le Sheet à chaque ouverture.
- **Si la page reste blanche ou affiche « La page n'a pas pu démarrer »** : un fichier n'est pas le bon, ou n'a pas été enregistré avant le déploiement.

## Sécurité
- Session de 8 heures. Après 10 mots de passe erronés, les connexions sont bloquées 30 minutes.
- Après un départ, changer le mot de passe (étape 4) : tout le monde est déconnecté. `fermerToutesLesSessions` (depuis l'éditeur) déconnecte aussi tout le monde, sans changer le mot de passe.
- Les fonctions d'administration refusent tout appel venant de la page.
- Le classeur « Tarifs revendeurs HT » n'est jamais lu par l'outil.

## Pour les développeurs
- **Fichiers produits** : `python3 devis/outils/assembler_appscript.py` produit `Calcul.html`, `Logos.html` et le dossier `a-copier/` (les 8 fichiers à coller). Le relancer après toute modification de `devis/appscript/` ou de `devis/logos/`. Le banc d'essai sert les fichiers de `a-copier/` : ce sont exactement eux qui sont testés.
- **Banc d'essai** :
  - lancement : `cd devis/banc && npm install && node serveur.js` ;
  - adresse : http://127.0.0.1:8787, mot de passe `banc-essai-2026` ;
  - le vrai `Code.gs` y tourne avec des services Apps Script simulés (`appsscript-simule.js`).
- **Tests** : `npm test` couvre le moteur de calcul, le serveur, et 5 parcours dans Chromium avec PDF. Captures et PDF dans `devis/banc/sorties/`.
- **Données du banc**, après une modification de la trace :
  1. `python3 devis/outils/construire_sheet.py devis/donnees devis/banc/classeur-trace.xlsx` ;
  2. `python3 -I devis/banc/exporter_catalogue.py devis/banc/classeur-trace.xlsx`.
