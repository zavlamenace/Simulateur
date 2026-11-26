/**
 * Outil de devis Billards de France — serveur Apps Script, lié au Google Sheet « BdF – Tarifs & contenus ».
 *
 * - Accès par un mot de passe commun (haché et salé dans les propriétés du script), session de 8 h,
 *   blocage de 30 minutes après 10 échecs. Aucune donnée n'est envoyée avant l'authentification.
 * - Lecture du Sheet par blocs « ■ TITRE » et par noms de colonnes (jamais par position).
 * - Journal des devis : brouillons et devis générés, configuration complète en JSON pour la reprise.
 *
 * Installation et mot de passe : voir INSTALLATION.md.
 */

var DUREE_SESSION_MS = 8 * 3600 * 1000;
var MAX_ECHECS = 10;
var BLOCAGE_MS = 30 * 60 * 1000;
var ITERATIONS = 2000;
var ONGLETS_IGNORES = { "Mode d'emploi": true, "Journal": true };
var ENTETES_JOURNAL = ["Référence", "Date", "Réalisé par", "N° facturation", "Client", "Ville", "Gamme", "Modèle",
  "Total TTC", "Remise", "Configuration complète", "Statut", "Version", "Téléphone", "Email", "Origine du contact",
  "Mis à jour", "Suivi"];
/** Étapes du suivi commercial (liste déroulante de la colonne « Suivi » du Journal). */
var SUIVI = ["Envoyé", "En réflexion", "À relancer", "Relancé", "En négociation", "Validé (bon pour accord)", "Acompte reçu",
  "Perdu", "Sans suite", "Remplacé par une nouvelle version"];
var SUIVI_FINAL = { "Validé (bon pour accord)": true, "Acompte reçu": true, "Perdu": true, "Sans suite": true };

// --------------------------------------------------------------------------------------------------------------
// Page

function doGet() {
  return HtmlService.createTemplateFromFile("Index").evaluate()
    .setTitle("Devis · Billards de France")
    .addMetaTag("viewport", "width=device-width, initial-scale=1");
}

/** Insère un fichier HTML du projet (Styles, Calcul, Logos, Pdf, App) dans Index. */
function include(nom) {
  return HtmlService.createHtmlOutputFromFile(nom).getContent();
}

// --------------------------------------------------------------------------------------------------------------
// Mot de passe et sessions

function hacher_(sel, motDePasse) {
  var valeur = sel + motDePasse;
  for (var i = 0; i < ITERATIONS; i++) {
    valeur = Utilities.base64Encode(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, valeur,
      Utilities.Charset.UTF_8));
  }
  return valeur;
}

/**
 * Les fonctions publiques peuvent être appelées depuis la page par google.script.run : celles d'administration
 * vérifient qu'elles sont lancées par le propriétaire, depuis l'éditeur.
 */
function proprietaire_() {
  var actif = Session.getActiveUser().getEmail();
  if (!actif || actif !== Session.getEffectiveUser().getEmail()) {
    throw new Error("Réservé au propriétaire du Sheet, depuis l'éditeur Apps Script.");
  }
}

/** Ferme toutes les sessions ouvertes (par exemple après un changement d'équipe). */
function fermerToutesLesSessions() {
  proprietaire_();
  fermerSessions_(PropertiesService.getScriptProperties());
}

function fermerSessions_(p) {
  Object.keys(p.getProperties()).forEach(function (k) { if (k.indexOf("SESSION_") === 0) p.deleteProperty(k); });
}

function connexion(motDePasse) {
  var verrou = LockService.getScriptLock();
  verrou.waitLock(10000);
  try {
    var p = PropertiesService.getScriptProperties();
    var bloque = Number(p.getProperty("BLOQUE_JUSQUA") || 0);
    if (bloque > Date.now()) {
      return { ok: false, message: "Trop d'essais. Réessayez dans " + Math.ceil((bloque - Date.now()) / 60000) + " minutes." };
    }
    var attente = appliquerMotDePasseEnAttente_(p);
    if (attente) return { ok: false, message: attente };
    var sel = p.getProperty("MDP_SEL"), empreinte = p.getProperty("MDP_EMPREINTE");
    if (!sel || !empreinte) {
      return { ok: false, message: "Mot de passe pas encore défini : ajoutez la propriété MOT_DE_PASSE dans les paramètres du projet Apps Script (INSTALLATION.md, étape 4)." };
    }
    if (hacher_(sel, String(motDePasse || "")) !== empreinte) {
      var echecs = Number(p.getProperty("ECHECS") || 0) + 1;
      p.setProperty("ECHECS", String(echecs));
      if (echecs >= MAX_ECHECS) {
        p.setProperty("BLOQUE_JUSQUA", String(Date.now() + BLOCAGE_MS));
        p.deleteProperty("ECHECS");
      }
      return { ok: false, message: "Mot de passe incorrect." };
    }
    p.deleteProperty("ECHECS");
    purgerSessions_(p);
    var jeton = Utilities.getUuid();
    p.setProperty("SESSION_" + jeton, String(Date.now() + DUREE_SESSION_MS));
    return { ok: true, jeton: jeton };
  } finally {
    verrou.releaseLock();
  }
}

/**
 * Mot de passe saisi par le propriétaire dans Paramètres du projet > Propriétés du script (MOT_DE_PASSE) :
 * il est haché et salé à la connexion suivante, puis la valeur en clair est effacée. Toutes les sessions sont fermées.
 * Renvoie un message d'erreur, ou null.
 */
function appliquerMotDePasseEnAttente_(p) {
  var clair = p.getProperty("MOT_DE_PASSE");
  if (clair === null || clair === undefined) return null;
  clair = String(clair).trim();
  if (clair.length < 10) return "Le mot de passe saisi dans les propriétés du script doit faire au moins 10 caractères.";
  var sel = Utilities.getUuid();
  p.setProperty("MDP_SEL", sel);
  p.setProperty("MDP_EMPREINTE", hacher_(sel, clair));
  p.deleteProperty("MOT_DE_PASSE");
  p.deleteProperty("ECHECS");
  p.deleteProperty("BLOQUE_JUSQUA");
  fermerSessions_(p);
  return null;
}

/** Diagnostic à lancer depuis l'éditeur : le résultat s'affiche dans le journal d'exécution. */
function verifierInstallation() {
  var p = PropertiesService.getScriptProperties();
  var l = ["Classeur : " + SpreadsheetApp.getActive().getName()];
  l.push("Mot de passe : " + (p.getProperty("MOT_DE_PASSE") ? "en attente, appliqué à la prochaine connexion"
    : p.getProperty("MDP_EMPREINTE") ? "défini" : "NON DÉFINI (étape 4)"));
  var onglets = [];
  SpreadsheetApp.getActive().getSheets().forEach(function (f) {
    if (!ONGLETS_IGNORES[f.getName()] && !f.isSheetHidden()) onglets.push(f.getName());
  });
  l.push("Onglets lus par la page : " + onglets.join(", "));
  try { journal_(); l.push("Journal : prêt"); } catch (e) { l.push("Journal : " + e.message); }
  Logger.log(l.join("\n"));
}

function purgerSessions_(p) {
  var maintenant = Date.now();
  var toutes = p.getProperties();
  Object.keys(toutes).forEach(function (k) {
    if (k.indexOf("SESSION_") === 0 && Number(toutes[k]) < maintenant) p.deleteProperty(k);
  });
}

function verifier_(jeton) {
  var fin = jeton && PropertiesService.getScriptProperties().getProperty("SESSION_" + jeton);
  if (!fin || Number(fin) < Date.now()) throw new Error("SESSION_EXPIREE");
}

function deconnexion(jeton) {
  if (jeton) PropertiesService.getScriptProperties().deleteProperty("SESSION_" + jeton);
  return true;
}

// --------------------------------------------------------------------------------------------------------------
// Lecture du Sheet (même règle que devis/outils/lire_sheet.py)

function lireOnglet_(valeurs) {
  var blocs = {}, courant = null, entetes = null;
  valeurs.forEach(function (ligne) {
    var premiere = ligne[0];
    if (typeof premiere === "string" && premiere.indexOf("■") === 0) {
      courant = premiere.replace(/^■\s*/, "").trim();
      entetes = null;
      blocs[courant] = [];
      return;
    }
    if (courant === null) return;
    if (entetes === null) {
      entetes = ligne.map(function (v) { return v === "" || v === null ? null : String(v).trim(); });
      return;
    }
    if (ligne.every(function (v) { return v === "" || v === null || (typeof v === "string" && !v.trim()); })) return;
    var objet = {};
    entetes.forEach(function (h, i) {
      if (!h) return;
      var v = ligne[i];
      objet[h] = v === "" ? null : (v instanceof Date ? v.toISOString() : v);
    });
    blocs[courant].push(objet);
  });
  return blocs;
}

/** Tout le catalogue (sauf le mode d'emploi et le journal), en JSON. */
function catalogue(jeton) {
  verifier_(jeton);
  var out = {};
  SpreadsheetApp.getActive().getSheets().forEach(function (feuille) {
    var nom = feuille.getName();
    if (ONGLETS_IGNORES[nom] || feuille.isSheetHidden()) return;
    out[nom] = lireOnglet_(feuille.getDataRange().getValues());
  });
  return JSON.stringify(out);
}

// --------------------------------------------------------------------------------------------------------------
// Journal

function journal_() {
  var feuille = SpreadsheetApp.getActive().getSheetByName("Journal");
  if (!feuille) throw new Error("Onglet « Journal » introuvable.");
  var valeurs = feuille.getDataRange().getValues();
  var ligneTitre = -1;
  for (var i = 0; i < valeurs.length; i++) {
    if (String(valeurs[i][0]).indexOf("■") === 0) { ligneTitre = i; break; }
  }
  if (ligneTitre < 0) throw new Error("Bloc « ■ DEVIS » introuvable dans le Journal.");
  var ligneEntetes = ligneTitre + 2;
  var entetes = feuille.getRange(ligneEntetes, 1, 1, Math.max(feuille.getLastColumn(), 1)).getValues()[0]
    .map(function (v) { return String(v || "").trim(); });
  ENTETES_JOURNAL.forEach(function (h) {
    if (entetes.indexOf(h) < 0) {
      var vide = entetes.indexOf("");
      var col = vide >= 0 ? vide : entetes.length;
      entetes[col] = h;
      feuille.getRange(ligneEntetes, col + 1).setValue(h).setFontWeight("bold");
    }
  });
  var colonnes = {};
  entetes.forEach(function (h, i) { if (h) colonnes[h] = i + 1; });
  var debut = ligneEntetes + 1, hauteur = Math.max(feuille.getMaxRows() - ligneEntetes, 1);
  if (!feuille.getRange(debut, colonnes["Suivi"]).getDataValidation()) {
    feuille.getRange(debut, colonnes["Suivi"], hauteur, 1).setDataValidation(
      SpreadsheetApp.newDataValidation().requireValueInList(SUIVI, true).setAllowInvalid(true).build());
  }
  return { feuille: feuille, ligneEntetes: ligneEntetes, colonnes: colonnes };
}

function lignesJournal_(j) {
  var derniere = j.feuille.getLastRow();
  if (derniere <= j.ligneEntetes) return [];
  var largeur = j.feuille.getLastColumn();
  var valeurs = j.feuille.getRange(j.ligneEntetes + 1, 1, derniere - j.ligneEntetes, largeur).getValues();
  return valeurs.map(function (ligne, i) {
    var o = { ligne: j.ligneEntetes + 1 + i };
    Object.keys(j.colonnes).forEach(function (h) { o[h] = ligne[j.colonnes[h] - 1]; });
    return o;
  }).filter(function (o) { return o["Référence"]; });
}

function prefixe_() {
  var feuille = SpreadsheetApp.getActive().getSheetByName("Paramètres");
  var p = feuille ? lireOnglet_(feuille.getDataRange().getValues())["PARAMÈTRES"] || [] : [];
  var ligne = p.filter(function (l) { return l["Paramètre"] === "Préfixe des références de devis"; })[0];
  return (ligne && ligne.Valeur) || "BDF";
}

function nouvelleReference_(lignes) {
  var annee = new Date().getFullYear();
  var debut = prefixe_() + "-" + annee + "-";
  var max = 0;
  lignes.forEach(function (o) {
    var r = String(o["Référence"]);
    if (r.indexOf(debut) === 0) max = Math.max(max, Number(r.substr(debut.length, 4)) || 0);
  });
  var p = PropertiesService.getScriptProperties();
  var compteur = Math.max(max, Number(p.getProperty("COMPTEUR_" + annee) || 0)) + 1;
  p.setProperty("COMPTEUR_" + annee, String(compteur));
  return debut + ("000" + compteur).slice(-4);
}

function nouvelleVersion_(lignes, base) {
  var max = 1;
  lignes.forEach(function (o) {
    var r = String(o["Référence"]);
    if (r === base) max = Math.max(max, 1);
    else if (r.indexOf(base + "-") === 0) max = Math.max(max, Number(r.substr(base.length + 1)) || 1);
  });
  return { ref: base + "-" + (max + 1), version: max + 1 };
}

/**
 * Enregistre un devis (statut « Brouillon » ou « Généré »). Attribue la référence au premier enregistrement ;
 * un devis rouvert après génération repart en nouvelle version (BDF-2026-0001-2).
 */
function enregistrer(jeton, configJson, statut, resume) {
  verifier_(jeton);
  var verrou = LockService.getScriptLock();
  verrou.waitLock(20000);
  try {
    var cfg = JSON.parse(configJson);
    resume = resume || {};
    var j = journal_();
    var lignes = lignesJournal_(j);
    var existante = cfg.ref ? lignes.filter(function (o) { return o["Référence"] === cfg.ref; })[0] : null;
    if (existante && existante.Statut === "Généré") {
      // Un devis déjà envoyé n'est jamais modifié : la modification devient une nouvelle version.
      var v = nouvelleVersion_(lignes, cfg.refBase || cfg.ref);
      cfg.ref = v.ref; cfg.version = v.version; cfg.date = null;
      existante = null;
    } else if (!cfg.ref) {
      cfg.ref = nouvelleReference_(lignes); cfg.version = 1; cfg.refBase = cfg.ref;
    }
    if (!cfg.date) cfg.date = Utilities.formatDate(new Date(), "Europe/Paris", "dd/MM/yyyy");
    var c = cfg.client || {};
    var valeurs = {
      "Référence": cfg.ref, "Date": existante ? existante.Date : new Date(), "Réalisé par": cfg.realisePar || "",
      "N° facturation": cfg.numeroFacturation || "", "Client": [c.prenom, c.nom].filter(Boolean).join(" "),
      "Ville": [c.codePostal, c.ville].filter(Boolean).join(" "), "Gamme": cfg.gamme || "", "Modèle": [cfg.modele, cfg.taille || cfg.versionModele].filter(Boolean).join(", "),
      "Total TTC": resume.total || 0, "Remise": resume.remise || 0, "Configuration complète": JSON.stringify(cfg),
      "Statut": statut, "Version": cfg.version || 1, "Téléphone": c.telephone || "", "Email": c.email || "",
      "Origine du contact": c.origine || "", "Mis à jour": new Date(),
    };
    var numero = existante ? existante.ligne : Math.max(j.feuille.getLastRow() + 1, j.ligneEntetes + 1);
    if (statut === "Généré" && !(existante && existante.Suivi)) valeurs.Suivi = "Envoyé";
    Object.keys(valeurs).forEach(function (h) {
      if (j.colonnes[h]) j.feuille.getRange(numero, j.colonnes[h]).setValue(valeurs[h]);
    });
    if (statut === "Généré" && cfg.version > 1) {
      // Les versions précédentes encore en cours sont marquées remplacées : le suivi ne compte qu'une fois le projet.
      var base = cfg.refBase || cfg.ref;
      lignes.forEach(function (o) {
        var r = String(o["Référence"]);
        if (r === cfg.ref || (r !== base && r.indexOf(base + "-") !== 0) || o.Statut !== "Généré" || SUIVI_FINAL[o.Suivi]) return;
        j.feuille.getRange(o.ligne, j.colonnes.Suivi).setValue("Remplacé par une nouvelle version");
      });
    }
    return { ref: cfg.ref, version: cfg.version, refBase: cfg.refBase, date: cfg.date, statut: statut };
  } finally {
    verrou.releaseLock();
  }
}

/** Derniers devis du journal (les plus récents d'abord), filtrés par texte. */
function listeDevis(jeton, recherche) {
  verifier_(jeton);
  var r = String(recherche || "").toLowerCase();
  return lignesJournal_(journal_()).reverse().filter(function (o) {
    return !r || [o["Référence"], o.Client, o.Ville, o.Gamme, o["Modèle"]].join(" ").toLowerCase().indexOf(r) >= 0;
  }).slice(0, 50).map(function (o) {
    return { ref: o["Référence"], date: o.Date instanceof Date ? Utilities.formatDate(o.Date, "Europe/Paris", "dd/MM/yyyy") : String(o.Date || ""),
             client: o.Client, ville: o.Ville, gamme: o.Gamme, modele: o["Modèle"], total: o["Total TTC"],
             statut: o.Statut || "Généré", suivi: o.Suivi || "", realisePar: o["Réalisé par"] };
  });
}

/** Configuration complète d'un devis du journal. */
function ouvrir(jeton, ref) {
  verifier_(jeton);
  var o = lignesJournal_(journal_()).filter(function (x) { return x["Référence"] === ref; })[0];
  if (!o) throw new Error("Devis introuvable : " + ref);
  return JSON.stringify({ statut: o.Statut || "Généré", config: JSON.parse(o["Configuration complète"] || "{}") });
}
