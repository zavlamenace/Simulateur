# Installer la page de devis (Apps Script)

Comptez 20 minutes environ, avec le compte Google propriétaire du Sheet « BdF – Tarifs & contenus ».
Les commerciaux n'ont pas besoin d'accès au Sheet : seule la page le lit, avec le compte propriétaire.

## 1. Ouvrir l'éditeur
1. Ouvrir le Sheet, puis **Extensions > Apps Script**.
2. Renommer le projet « Devis Billards de France ».

## 2. Copier les fichiers
Les fichiers sont dans `devis/appscript/` du dépôt. Pour un fichier HTML : bouton **+** > **HTML**, puis nommer le fichier sans « .html ».

| Fichier du dépôt | Dans l'éditeur |
|---|---|
| `Code.gs` | `Code.gs` (remplacer le contenu existant) |
| `Index.html` | `Index` |
| `Styles.html` | `Styles` |
| `Calcul.html` | `Calcul` |
| `Logos.html` | `Logos` |
| `Pdf.html` | `Pdf` |
| `App.html` | `App` |

Ne pas copier `calcul.js` : son contenu est déjà dans `Calcul.html`.

## 3. Manifeste
1. **Paramètres du projet** (roue dentée) : cocher « Afficher le fichier manifeste "appsscript.json" dans l'éditeur ».
2. Ouvrir `appsscript.json` dans l'éditeur et remplacer son contenu par celui de `devis/appscript/appsscript.json`.

Autorisations demandées :
- ce tableur seulement ;
- l'adresse email du compte, qui sert à réserver les fonctions d'administration au propriétaire.

## 4. Mot de passe de l'équipe
1. Dans `Code.gs`, fonction `definirMotDePasse` : remplacer `REMPLACER-PAR-LE-MOT-DE-PASSE` par le mot de passe choisi (10 caractères au moins).
2. Choisir `definirMotDePasse` dans la liste en haut de l'éditeur, puis **Exécuter**. Accepter les autorisations.
3. Remettre le texte `REMPLACER-PAR-LE-MOT-DE-PASSE`, puis enregistrer. Le mot de passe n'est conservé que haché.

Pour changer le mot de passe plus tard, refaire ces trois étapes : toutes les sessions ouvertes sont fermées.

## 5. Déployer
1. **Déployer > Nouveau déploiement**, type **Application Web**.
2. Description : « Devis v1 ».
3. **Exécuter en tant que** : Moi. **Qui a accès** : Tout le monde.
4. Copier l'URL de l'application Web (elle finit par `/exec`).
5. La transmettre à l'équipe avec le mot de passe, par un canal privé.

## 6. Premiers contrôles
1. **Sur ordinateur** :
   - ouvrir l'URL et se connecter ;
   - faire un devis Référence complet, puis **Générer le PDF** ;
   - vérifier que le PDF se télécharge et qu'une ligne apparaît dans l'onglet « Journal ».
2. **Sur téléphone** : même parcours. Si le téléchargement ne démarre pas, utiliser **Ouvrir le PDF dans un onglet**.
3. **Récap CRM** : cliquer **Copier le récap CRM**, puis coller dans le CRM.

## Mettre à jour la page
- **Code** :
  1. remplacer le contenu des fichiers modifiés ;
  2. **Déployer > Gérer les déploiements**, crayon, Version « Nouvelle version », **Déployer** ;
  3. l'URL ne change pas.
- **Contenus** : prix, options, arguments, équipe et paramètres se modifient dans le Sheet. Rien à redéployer : la page relit le Sheet à chaque ouverture.

## Sécurité
- Session de 8 heures. Après 10 mots de passe erronés, les connexions sont bloquées 30 minutes.
- `fermerToutesLesSessions` (depuis l'éditeur) déconnecte tout le monde, par exemple après un départ. Changer aussi le mot de passe.
- Les fonctions d'administration refusent tout appel venant de la page.
- Le classeur « Tarifs revendeurs HT » n'est jamais lu par l'outil.

## Pour les développeurs
- **Fichiers produits** : `Calcul.html` et `Logos.html` viennent de `python3 devis/outils/assembler_appscript.py`. Le relancer après une modification de `calcul.js` ou de `devis/logos/`.
- **Banc d'essai** :
  - lancement : `cd devis/banc && npm install && node serveur.js` ;
  - adresse : http://127.0.0.1:8787, mot de passe `banc-essai-2026` ;
  - le vrai `Code.gs` y tourne avec des services Apps Script simulés (`appsscript-simule.js`).
- **Tests** : `npm test` couvre le moteur de calcul, le serveur, et 5 parcours dans Chromium avec PDF. Captures et PDF dans `devis/banc/sorties/`.
- **Données du banc**, après une modification de la trace :
  1. `python3 devis/outils/construire_sheet.py devis/donnees devis/banc/classeur-trace.xlsx` ;
  2. `python3 -I devis/banc/exporter_catalogue.py devis/banc/classeur-trace.xlsx`.
