/**
 * Simulation des services Apps Script utilisés par Code.gs, pour exécuter le vrai serveur dans Node :
 * SpreadsheetApp (classeur en mémoire, chargé depuis feuilles.json), PropertiesService, LockService,
 * Utilities, HtmlService, Session, Logger.
 */
"use strict";
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const APPSCRIPT = path.join(__dirname, "..", "appscript");

class Feuille {
  constructor(nom, valeurs, cachee) {
    this.nom = nom;
    this.cachee = !!cachee;
    this.cellules = valeurs.map((l) => l.slice());
    this.validations = {};
  }
  getMaxRows() { return Math.max(this.cellules.length, 1000); }
  getName() { return this.nom; }
  isSheetHidden() { return this.cachee; }
  getLastRow() {
    for (let r = this.cellules.length; r > 0; r--) if (this.cellules[r - 1].some((v) => v !== "" && v !== null)) return r;
    return 0;
  }
  getLastColumn() {
    let max = 0;
    this.cellules.forEach((l) => l.forEach((v, c) => { if (v !== "" && v !== null) max = Math.max(max, c + 1); }));
    return max;
  }
  lire(r, c) { const l = this.cellules[r - 1]; return l && l[c - 1] !== undefined ? l[c - 1] : ""; }
  ecrire(r, c, v) {
    while (this.cellules.length < r) this.cellules.push([]);
    const l = this.cellules[r - 1];
    while (l.length < c) l.push("");
    l[c - 1] = v;
  }
  getRange(r, c, nr, nc) { return new Plage(this, r, c, nr || 1, nc || 1); }
  getDataRange() { return new Plage(this, 1, 1, Math.max(this.getLastRow(), 1), Math.max(this.getLastColumn(), 1)); }
}

class Plage {
  constructor(f, r, c, nr, nc) { Object.assign(this, { f, r, c, nr, nc }); }
  getValues() {
    const out = [];
    for (let i = 0; i < this.nr; i++) {
      const l = [];
      for (let j = 0; j < this.nc; j++) l.push(this.f.lire(this.r + i, this.c + j));
      out.push(l);
    }
    return out;
  }
  setValue(v) { this.f.ecrire(this.r, this.c, v); return this; }
  setFontWeight() { return this; }
  setNumberFormat() { return this; }
  getDataValidation() { return (this.f.validations[this.c] && this.r >= this.f.validations[this.c].debut) ? this.f.validations[this.c].regle : null; }
  setDataValidation(regle) { this.f.validations[this.c] = { debut: this.r, regle }; return this; }
}

function octetsSignes(buffer) {
  return Array.from(buffer, (b) => (b > 127 ? b - 256 : b));
}

/**
 * Crée un serveur Code.gs simulé.
 * @param {object} o { feuilles: [{nom, cachee, valeurs}], motDePasse?: string }
 */
function creerAppsScript(o) {
  const feuilles = o.feuilles.map((f) => new Feuille(f.nom, f.valeurs, f.cachee));
  const proprietes = {};
  const journalDesAppels = [];
  let editeur = false;

  const contexte = {
    console,
    SpreadsheetApp: {
      newDataValidation: () => {
        const r = {};
        const b = { requireValueInList: (l) => { r.liste = l; return b; }, setAllowInvalid: () => b, build: () => r };
        return b;
      },
      getActive: () => ({
        getName: () => "BdF – Tarifs & contenus (banc)",
        getSheets: () => feuilles.slice(),
        getSheetByName: (n) => feuilles.find((f) => f.getName() === n) || null,
      }),
    },
    PropertiesService: {
      getScriptProperties: () => ({
        getProperty: (k) => (k in proprietes ? proprietes[k] : null),
        setProperty: (k, v) => { proprietes[k] = String(v); },
        deleteProperty: (k) => { delete proprietes[k]; },
        getProperties: () => Object.assign({}, proprietes),
      }),
    },
    LockService: { getScriptLock: () => ({ waitLock() {}, releaseLock() {} }) },
    Utilities: {
      DigestAlgorithm: { SHA_256: "sha256" },
      Charset: { UTF_8: "utf8" },
      computeDigest: (alg, valeur) => octetsSignes(crypto.createHash(alg).update(String(valeur), "utf8").digest()),
      base64Encode: (octets) => Buffer.from(octets.map((b) => (b < 0 ? b + 256 : b))).toString("base64"),
      getUuid: () => crypto.randomUUID(),
      formatDate: (date, fuseau, format) => {
        const p = new Intl.DateTimeFormat("fr-FR", { timeZone: fuseau, day: "2-digit", month: "2-digit", year: "numeric" })
          .formatToParts(date).reduce((a, x) => Object.assign(a, { [x.type]: x.value }), {});
        if (format !== "dd/MM/yyyy") throw new Error("Format non simulé : " + format);
        return p.day + "/" + p.month + "/" + p.year;
      },
    },
    HtmlService: {
      createHtmlOutputFromFile: (nom) => ({ getContent: () => fs.readFileSync(path.join(APPSCRIPT, nom + ".html"), "utf8") }),
    },
    Session: {
      getActiveUser: () => ({ getEmail: () => (editeur ? "proprietaire@exemple.fr" : "") }),
      getEffectiveUser: () => ({ getEmail: () => "proprietaire@exemple.fr" }),
    },
    Logger: { log: () => {} },
  };
  vm.createContext(contexte);
  vm.runInContext(fs.readFileSync(path.join(APPSCRIPT, "a-copier", "Code.gs"), "utf8"), contexte, { filename: "Code.gs" });

  /** Exécute une fonction comme depuis l'éditeur Apps Script (propriétaire connecté). */
  function depuisEditeur(nom, ...args) {
    editeur = true;
    try { return contexte[nom](...args); } finally { editeur = false; }
  }

  if (o.motDePasse) {
    proprietes.MOT_DE_PASSE = o.motDePasse;
    contexte.appliquerMotDePasseEnAttente_(contexte.PropertiesService.getScriptProperties());
  }

  /** Appel comme google.script.run : seules les fonctions publiques (sans « _ » final) sont accessibles. */
  function appeler(nom, args) {
    journalDesAppels.push(nom);
    if (typeof contexte[nom] !== "function" || /_$/.test(nom)) throw new Error("Fonction inconnue : " + nom);
    const r = contexte[nom](...(args || []));
    return JSON.parse(JSON.stringify(r === undefined ? null : r));
  }

  return { appeler, depuisEditeur, contexte, feuilles, proprietes, journalDesAppels };
}

module.exports = { creerAppsScript };
