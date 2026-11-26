/** Le vrai Code.gs, exécuté avec les services Apps Script simulés. */
"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const { execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");
const { creerAppsScript } = require("../appsscript-simule");

const feuilles = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "feuilles.json"), "utf8"));
const catalogueTrace = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "catalogue.json"), "utf8"));
const MDP = "un-mot-de-passe-de-test";

function serveur() { return creerAppsScript({ feuilles, motDePasse: MDP }); }

function connecter(gas) {
  const r = gas.appeler("connexion", [MDP]);
  assert.equal(r.ok, true);
  return r.jeton;
}

test("Mot de passe : haché et salé, jamais stocké en clair ; session de 8 h", () => {
  const gas = serveur();
  assert.ok(gas.proprietes.MDP_SEL && gas.proprietes.MDP_EMPREINTE);
  assert.ok(!Object.values(gas.proprietes).some((v) => v.includes(MDP)));
  assert.deepEqual(gas.appeler("connexion", ["faux"]), { ok: false, message: "Mot de passe incorrect." });
  const jeton = connecter(gas);
  const fin = Number(gas.proprietes["SESSION_" + jeton]);
  assert.ok(Math.abs(fin - Date.now() - 8 * 3600 * 1000) < 5000);
});

test("Blocage de 30 minutes après 10 échecs", () => {
  const gas = serveur();
  for (let i = 0; i < 10; i++) assert.equal(gas.appeler("connexion", ["faux"]).ok, false);
  const r = gas.appeler("connexion", [MDP]);
  assert.equal(r.ok, false);
  assert.match(r.message, /Trop d'essais\. Réessayez dans 30 minutes/);
});

test("Aucune donnée sans session valide", () => {
  const gas = serveur();
  for (const [nom, args] of [["catalogue", []], ["catalogue", ["jeton-inventé"]], ["listeDevis", [""]], ["ouvrir", ["", "BDF-2026-0001"]],
    ["enregistrer", ["", "{}", "Brouillon", {}]]]) {
    assert.throws(() => gas.appeler(nom, args), /SESSION_EXPIREE/, nom);
  }
  const jeton = connecter(gas);
  gas.proprietes["SESSION_" + jeton] = String(Date.now() - 1);
  assert.throws(() => gas.appeler("catalogue", [jeton]), /SESSION_EXPIREE/);
});

test("Fonctions d'administration refusées depuis la page, privées inaccessibles", () => {
  const gas = serveur();
  const jeton = connecter(gas);
  assert.throws(() => gas.appeler("fermerToutesLesSessions", []), /Réservé au propriétaire/);
  assert.ok(gas.proprietes["SESSION_" + jeton], "la session n'a pas été fermée");
  assert.throws(() => gas.appeler("verifier_", [jeton]), /Fonction inconnue/);
  gas.depuisEditeur("fermerToutesLesSessions");
  assert.equal(gas.proprietes["SESSION_" + jeton], undefined);
});

test("Le catalogue lu par Code.gs est identique à la lecture de référence (lire_sheet.py)", () => {
  const gas = serveur();
  const cat = JSON.parse(gas.appeler("catalogue", [connecter(gas)]));
  const attendu = Object.assign({}, catalogueTrace);
  delete attendu.Journal;
  assert.deepEqual(cat, attendu);
});

test("Journal : références, brouillon mis à jour, devis généré jamais modifié, versions", () => {
  const gas = serveur();
  const jeton = connecter(gas);
  const annee = new Date().getFullYear();
  const cfg = { client: { prenom: "Claire", nom: "Martin", codePostal: "33000", ville: "Bordeaux" }, gamme: "Design", modele: "Boston" };
  const b = gas.appeler("enregistrer", [jeton, JSON.stringify(cfg), "Brouillon", { total: 4390, remise: 0 }]);
  assert.equal(b.ref, `BDF-${annee}-0001`);
  assert.match(b.date, /^\d{2}\/\d{2}\/\d{4}$/);
  const b2 = gas.appeler("enregistrer", [jeton, JSON.stringify(Object.assign({}, cfg, b)), "Brouillon", { total: 4500, remise: 0 }]);
  assert.equal(b2.ref, b.ref, "un brouillon est mis à jour sur place");
  assert.equal(gas.appeler("listeDevis", [jeton, ""]).length, 1);
  const g = gas.appeler("enregistrer", [jeton, JSON.stringify(Object.assign({}, cfg, b2)), "Généré", { total: 4500, remise: 0 }]);
  assert.equal(g.ref, b.ref);
  assert.equal(g.statut, "Généré");
  const j0 = gas.feuilles.find((f) => f.getName() === "Journal");
  const colonne = (h) => j0.getRange(5, 1, 1, j0.getLastColumn()).getValues()[0].indexOf(h) + 1;
  assert.equal(j0.lire(6, colonne("Suivi")), "Envoyé", "suivi posé à la génération");
  assert.ok(j0.validations[colonne("Suivi")].regle.liste.includes("Validé (bon pour accord)"));
  const v2 = gas.appeler("enregistrer", [jeton, JSON.stringify(Object.assign({}, cfg, g)), "Brouillon", { total: 4600, remise: 0 }]);
  assert.equal(j0.lire(6, colonne("Suivi")), "Envoyé", "un brouillon V2 ne change pas le suivi de la V1");
  gas.appeler("enregistrer", [jeton, JSON.stringify(Object.assign({}, cfg, v2)), "Généré", { total: 4600, remise: 0 }]);
  assert.equal(j0.lire(6, colonne("Suivi")), "Remplacé par une nouvelle version");
  assert.equal(j0.lire(7, colonne("Suivi")), "Envoyé");
  assert.equal(v2.ref, `${b.ref}-2`);
  assert.equal(v2.version, 2);
  const autre = gas.appeler("enregistrer", [jeton, JSON.stringify({ client: { nom: "Durand" } }), "Brouillon", {}]);
  assert.equal(autre.ref, `BDF-${annee}-0002`);
  const liste = gas.appeler("listeDevis", [jeton, "martin"]);
  assert.deepEqual(liste.map((d) => [d.ref, d.statut, d.total, d.suivi]),
    [[`${b.ref}-2`, "Généré", 4600, "Envoyé"], [b.ref, "Généré", 4500, "Remplacé par une nouvelle version"]]);
  const ouvert = JSON.parse(gas.appeler("ouvrir", [jeton, b.ref]));
  assert.equal(ouvert.statut, "Généré");
  assert.equal(ouvert.config.modele, "Boston");
  const j = gas.feuilles.find((f) => f.getName() === "Journal");
  const entetes = j.getRange(5, 1, 1, j.getLastColumn()).getValues()[0];
  for (const h of ["Statut", "Version", "Téléphone", "Email", "Origine du contact", "Mis à jour", "Suivi"]) {
    assert.ok(!entetes.includes("Prochaine relance") && !entetes.includes("Note de suivi"));
    assert.ok(entetes.includes(h), h);
  }
});

test("Mot de passe saisi dans les propriétés du script : haché à la connexion suivante, puis effacé", () => {
  const gas = creerAppsScript({ feuilles });
  assert.match(gas.appeler("connexion", ["x"]).message, /pas encore défini/);
  gas.proprietes.MOT_DE_PASSE = "court";
  assert.match(gas.appeler("connexion", ["court"]).message, /au moins 10 caractères/);
  gas.proprietes.MOT_DE_PASSE = "  billard-2026-equipe ";
  const r = gas.appeler("connexion", ["billard-2026-equipe"]);
  assert.equal(r.ok, true);
  assert.equal(gas.proprietes.MOT_DE_PASSE, undefined);
  assert.ok(gas.proprietes.MDP_EMPREINTE);
  assert.ok(!Object.values(gas.proprietes).some((v) => v.includes("billard-2026-equipe")));
  gas.proprietes.MOT_DE_PASSE = "nouveau-mot-de-passe";
  assert.equal(gas.appeler("connexion", ["billard-2026-equipe"]).ok, false, "l'ancien ne marche plus");
  assert.equal(gas.proprietes["SESSION_" + r.jeton], undefined, "sessions fermées");
  assert.equal(gas.appeler("connexion", ["nouveau-mot-de-passe"]).ok, true);
  gas.depuisEditeur("verifierInstallation");
  const diag = gas.journaux.join("\n");
  assert.match(diag, /Mot de passe : défini/);
  assert.match(diag, /Règles du Sheet : aucune anomalie/);
});

test("Fichiers dérivés à jour (Calcul.html, Logos.html)", () => {
  execFileSync("python3", [path.join(__dirname, "..", "..", "outils", "assembler_appscript.py"), "--verifier"]);
});
