/**
 * Parcours complets dans Chromium (Playwright) : la vraie page, le vrai Code.gs simulé, le vrai PDF.
 * Captures et PDF dans banc/sorties/ (non versionné).
 */
"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const { execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const { demarrer } = require("../serveur");

const SORTIES = path.join(__dirname, "..", "sorties");
const INTERDITS_TOUS = [/sans frais/i, /payplug/i, /rétractation/i, /0 SAV/i, /rappel/i, /hauteur/i];
const INTERDITS_REFERENCE = [/italien/i, /fabriqué(e)?s? (à|dans|en)/i, /atelier/i, /fabrication (française|artisanale)/i, /made in/i];

let banc, navigateur;

test.before(async () => {
  fs.mkdirSync(SORTIES, { recursive: true });
  banc = await demarrer(0);
  navigateur = await chromium.launch();
});

test.after(async () => {
  await navigateur.close();
  banc.serveur.close();
});

// ---------------------------------------------------------------------------------------------------------
// Outils

async function nouvellePage(options) {
  const contexte = await navigateur.newContext(Object.assign({ viewport: { width: 1440, height: 900 }, acceptDownloads: true,
    permissions: ["clipboard-read", "clipboard-write"] }, options || {}));
  const page = await contexte.newPage();
  page.erreurs = [];
  page.on("pageerror", (e) => page.erreurs.push(e.message));
  page.on("console", (m) => { if (m.type() === "error") page.erreurs.push(m.text()); });
  await page.goto(`http://127.0.0.1:${banc.port}/`);
  await page.fill("#mdp", banc.motDePasse);
  await page.click("#form-connexion button");
  await page.waitForSelector("#app:not([hidden])");
  assert.equal(await page.isHidden("#erreur-demarrage"), true);
  return page;
}

async function saisirClient(page, c) {
  await page.selectOption("#c-realisePar", c.par || "Xavier Fitan");
  await page.fill("#c-client-prenom", c.prenom);
  await page.fill("#c-client-nom", c.nom);
  await page.fill("#c-client-telephone", c.telephone || "06 12 34 56 78");
  await page.fill("#c-client-codePostal", c.codePostal);
  await page.fill("#c-client-ville", c.ville);
  await page.click('[data-action="continuer"][data-id="client"]');
}

const carte = (page, action, valeur) => page.click(`[data-action="${action}"][data-valeur="${valeur}"]`);

async function ouvrirSection(page, id) {
  const titre = page.locator(`[data-action="basculer-section"][data-id="${id}"]`);
  if ((await titre.getAttribute("aria-expanded")) !== "true") await titre.click();
}

const option = (page, nom) => page.locator(`input[data-option$="|${nom.replace(/"/g, '\\"')}"]`);

async function texte(page, selecteur) { return (await page.textContent(selecteur)).replace(/[\u00a0\u202f]/g, " "); }

async function total(page) { return texte(page, "#recap-total"); }

async function aCompleter(page) {
  return page.locator(".a-completer li").allTextContents();
}

async function generer(page, nom) {
  const [telechargement] = await Promise.all([page.waitForEvent("download"), page.click('[data-action="generer"]')]);
  const fichier = path.join(SORTIES, nom + ".pdf");
  await telechargement.saveAs(fichier);
  await page.waitForSelector(".fait");
  const texte = execFileSync("pdftotext", ["-layout", fichier, "-"], { encoding: "utf8" }).replace(/[  ]/g, " ");
  execFileSync("pdftoppm", ["-png", "-r", "70", fichier, path.join(SORTIES, nom)]);
  return { fichier, texte, nomPropose: telechargement.suggestedFilename() };
}

function sansMentionsInterdites(texte, reference) {
  for (const r of INTERDITS_TOUS.concat(reference ? INTERDITS_REFERENCE : [])) assert.doesNotMatch(texte, r);
}

async function sansDebordement(page) {
  const l = await page.evaluate(() => ({ page: document.scrollingElement.scrollWidth, fenetre: window.innerWidth }));
  assert.ok(l.page <= l.fenetre, `débordement horizontal : ${l.page} > ${l.fenetre}`);
}

// ---------------------------------------------------------------------------------------------------------
// Parcours

test("0. Démarrage impossible : message visible au lieu d'une page blanche", async () => {
  const contexte = await navigateur.newContext();
  const page = await contexte.newPage();
  await page.route("**/rpc/**", (r) => r.abort());
  await page.addInitScript(() => { Object.defineProperty(window, "LOGOS", { get() { throw new Error("Logos absent"); } }); });
  await page.goto(`http://127.0.0.1:${banc.port}/`);
  await page.waitForSelector("#erreur-demarrage:not([hidden])");
  assert.match(await page.textContent("#erreur-demarrage"), /n'a pas pu démarrer/);
  await contexte.close();
});

test("1. Référence simple : kit inclus, Oney, aucune mention d'origine, récap CRM", async () => {
  const page = await nouvellePage();
  await saisirClient(page, { prenom: "Claire", nom: "Martin", codePostal: "33000", ville: "Bordeaux" });
  await carte(page, "choisir-gamme", "Référence");
  await carte(page, "choisir-modele", "Santiago");
  assert.match(await texte(page, '[data-action="choisir-modele"][data-valeur="Santiago"]'), /dès 1 995 €/);
  await carte(page, "choisir-version", "Pieds bois massif");
  assert.equal(await option(page, "Billard américain").isChecked(), true, "jeu inclus coché d'office");
  await page.click('[data-action="continuer"][data-id="billard"]');
  assert.deepEqual(await aCompleter(page), ["Choisir la couleur du drap"]);
  assert.equal(await page.isDisabled('[data-action="generer"]'), true);
  await carte(page, "choisir-teinte", "Rouge");
  await ouvrirSection(page, "options");
  assert.match(await texte(page, ".option:has(input[data-option$='|Rangement des accessoires'])"), /\(400 €\)/);
  await option(page, "Rangement des accessoires").click();
  assert.equal(await total(page), "2 395 €");
  assert.match(await texte(page, "#recap"), /Oney/);
  await ouvrirSection(page, "arguments");
  assert.equal(await page.locator("input[data-argument]:checked").count(), 4);
  assert.equal(await page.locator("input[data-argument]:not(:checked):not([disabled])").count(), 0, "un 5e argument est impossible");

  const pdf = await generer(page, "1-reference");
  const ref = pdf.texte.match(/BDF-\d{4}-\d{4}/)[0];
  assert.equal(pdf.nomPropose, `Devis ${ref} Martin.pdf`);
  for (const attendu of ["Billard Référence Premium Santiago", "Tapis standard, couleur Rouge", "Kit accessoires inclus", "330 €",
    "Rangement des accessoires", "2 395 €", "Livraison par messagerie au pied de la porte", "Sur une palette fabriquée sur mesure", "Offerte", "Oney", "Je valide mon devis", "Bon pour accord",
    "Conditions générales de vente sur billardsdefrance.fr", "Xavier Fitan", "Claire Martin"]) {
    assert.ok(pdf.texte.includes(attendu), attendu);
  }
  sansMentionsInterdites(pdf.texte, true);
  assert.doesNotMatch(pdf.texte, /Lafuge/);
  assert.doesNotMatch(pdf.texte, /lancement en fabrication/);

  await page.click('[data-action="copier-crm"]');
  const crm = await page.evaluate(() => navigator.clipboard.readText());
  assert.match(crm, new RegExp(`^Devis ${ref} du \\d{2}/\\d{2}/\\d{4}`));
  assert.match(crm, /Total TTC : 2 395 €/);
  assert.match(crm, /Réalisé par : Xavier Fitan/);
  assert.deepEqual(page.erreurs, []);
});

test("2. Design : couleur RAL précisée, plateau, allonge soumise au plateau, brouillon puis reprise", async () => {
  const page = await nouvellePage();
  await saisirClient(page, { prenom: "Paul", nom: "Durand", codePostal: "75011", ville: "Paris" });
  await carte(page, "choisir-gamme", "Design");
  await carte(page, "choisir-modele", "Boston");
  await page.click('[data-action="continuer"][data-id="billard"]');
  await page.locator('[data-action="choisir-teinte"]').first().click();
  await ouvrirSection(page, "options");
  await option(page, "Couleur RAL au choix").click();
  await page.fill('input[data-precision-option$="|Couleur RAL au choix"]', "RAL 7016");
  await ouvrirSection(page, "plateau");
  assert.equal(await option(page, "Allonge de plateau 45 cm").isDisabled(), true);
  assert.match(await texte(page, ".option:has(input[data-option$='|Allonge de plateau 45 cm'])"), /Nécessite « Plateau table bois laqué »/);
  await option(page, "Plateau table bois laqué").click();
  await option(page, "Allonge de plateau 45 cm").click();
  assert.equal(await total(page), "6 130 €");
  await option(page, "Plateau 100 % verre Sécurit 8 mm").click();
  assert.match(await texte(page, "#message"), /Retiré automatiquement : Allonge de plateau 45 cm/);
  assert.equal(await total(page), "5 740 €");
  assert.match(await texte(page, "#recap"), /Couleur RAL au choix : RAL 7016/);

  await page.click('[data-action="enregistrer"]');
  await page.waitForFunction(() => /brouillon enregistré/.test(document.querySelector("#entete-ref").textContent));
  const ref = (await texte(page, "#entete-ref")).match(/BDF-\d{4}-\d{4}/)[0];
  await page.click('[data-action="nouveau"]');
  assert.equal(await texte(page, "#entete-ref"), "Nouveau devis");
  assert.equal(await page.inputValue("#c-client-nom"), "");

  await page.click('[data-action="ouvrir-liste"]');
  await page.fill("#recherche-devis", "durand");
  await page.click(`[data-action="ouvrir-devis"][data-ref="${ref}"]`);
  await page.waitForFunction((r) => document.querySelector("#entete-ref").textContent.startsWith(r), ref);
  assert.match(await texte(page, "#entete-ref"), /brouillon enregistré/);
  assert.equal(await total(page), "5 740 €");
  assert.match(await texte(page, "#recap"), /RAL 7016/);
  assert.deepEqual(page.erreurs, []);
});

test("3. Prestige : remises par ligne (% et €) et globale, prix barrés, nouvelle version après génération", async () => {
  const page = await nouvellePage();
  await saisirClient(page, { prenom: "Inès", nom: "Bernard", codePostal: "69006", ville: "Lyon" });
  await carte(page, "choisir-gamme", "Prestige");
  await carte(page, "choisir-modele", "Paris");
  await page.click('[data-action="continuer"][data-id="billard"]');
  await page.locator('[data-action="choisir-teinte"]').first().click();
  await ouvrirSection(page, "plateau");
  await option(page, "Plateau table bois").click();
  await option(page, "Motif décor à carré").click();
  assert.equal(await total(page), "10 090 €");

  await ouvrirSection(page, "remises");
  await page.fill('input[data-remise="billard"]', "10");
  const idDecor = "OPTIONS|Décor|Motif décor à carré";
  await page.click(`[data-action="type-remise"][data-id="${idDecor}"][data-type="€"]`);
  await page.fill(`input[data-remise="${idDecor}"]`, "100");
  await page.fill('input[data-remise="global"]', "5");
  assert.equal(await total(page), "8 654,50 €");
  assert.match(await texte(page, "#recap"), /\(remise 10 %\)8 800 €\s*7 920 €/);
  assert.match(await texte(page, "#recap"), /Remise sur le total \(5 %\)− 455,50 €/);

  const pdf = await generer(page, "3-prestige");
  const ref = pdf.texte.match(/BDF-\d{4}-\d{4}/)[0];
  for (const attendu of ["Prix catalogue", "10 090 €", "Remise 10 %", "Remise 100 €", "Remises sur les articles", "980 €",
    "Remise sur le total (5 %)", "455,50 €", "8 654,50 €", "7 920 €", "8 800 €"]) {
    assert.ok(pdf.texte.includes(attendu), attendu);
  }
  sansMentionsInterdites(pdf.texte, false);

  await ouvrirSection(page, "accessoires");
  await page.fill("#recherche-accessoires", "craie");
  await page.locator('[data-action="quantite"][data-pas="1"]').first().click();
  assert.match(await texte(page, "#entete-ref"), /nouvelle version/);
  const pdf2 = await generer(page, "3-prestige-v2");
  assert.ok(pdf2.texte.includes(ref + "-2"), "version 2");
  assert.deepEqual(page.erreurs, []);
});

test("4. Lafuge mixte Chambord 12 pieds : prix sur demande, règles, ligne libre en quantité 2, fiche technique", async () => {
  const page = await nouvellePage();
  await saisirClient(page, { prenom: "Marc", nom: "Lefèvre", codePostal: "06400", ville: "Cannes", par: "Philippe Fitan" });
  await carte(page, "choisir-gamme", "Lafuge mixte");
  await carte(page, "choisir-modele", "Chambord");
  await carte(page, "choisir-taille", "12 pieds");
  assert.equal(await option(page, "Snooker").isChecked(), true);
  assert.equal(await option(page, "Bandes initiales américaines").count(), 0, "américaines impossibles en 12 pieds");
  await page.click('[data-action="continuer"][data-id="billard"]');
  await carte(page, "choisir-drap", "Strachan 777");
  await page.locator('[data-action="choisir-teinte"]').first().click();
  await ouvrirSection(page, "options");
  assert.equal(await option(page, "Piètement démontable").isChecked(), true, "inclus coché d'office");
  await option(page, "Noyer massif").click();
  assert.equal(await option(page, "Laque").isDisabled(), true);
  assert.match(await texte(page, ".option:has(input[data-option$='|Laque'])"), /Incompatible avec « Noyer massif »/);
  assert.ok((await aCompleter(page)).includes("Saisir le prix : Noyer massif"));
  assert.equal(await page.isDisabled('[data-action="generer"]'), true);
  await page.fill('input[data-prix-option$="|Noyer massif"]', "3000");
  await option(page, "Cadre snooker").click();
  await ouvrirSection(page, "libres");
  await page.click('[data-action="ajouter-libre"]');
  await page.fill("#libre-libelle-0", "Housse de protection sur mesure");
  await page.fill("#libre-prix-0", "150");
  await page.fill("#libre-quantite-0", "2");
  assert.equal(await total(page), "28 300 €");
  assert.match(await texte(page, "#recap"), /2 × Housse de protection sur mesure\s*300 €/);
  assert.match(await texte(page, "#recap"), /lancement en fabrication \(30 %\) : 8 490 €/);
  await page.screenshot({ path: path.join(SORTIES, "ordinateur-lafuge.png"), fullPage: false });

  const pdf = await generer(page, "4-lafuge-mixte");
  for (const attendu of ["Billard mixte Chambord, 12 pieds", "Noyer massif", "3 000 €", "Cadre snooker", "Housse de protection sur mesure",
    "28 300 €", "Caractéristiques de votre billard", "Surface de jeu", "Ardoise italienne", "Strachan 777",
    "Billard vendu hors accessoires", "maison du groupe Billards de France", "Au lancement en fabrication", "Piètement démontable",
    "Philippe Fitan", "Miribel-les-Échelles"]) {
    assert.ok(pdf.texte.includes(attendu), attendu);
  }
  assert.match(pdf.texte, /Cadre\s+Noyer massif/, "la fiche suit l'essence choisie");
  assert.doesNotMatch(pdf.texte, /Érable sycomore massif/, "plus d'érable une fois le noyer choisi");
  assert.doesNotMatch(pdf.texte, /2,80 m : 6 pieds/, "ligne propre à une autre taille");
  sansMentionsInterdites(pdf.texte, false);
  assert.deepEqual(page.erreurs, []);
});

test("5. Lafuge bandes françaises sur téléphone (390 px) : A37, chauffage, Simonis 330 et ses couleurs", async () => {
  const page = await nouvellePage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  await sansDebordement(page);
  await saisirClient(page, { prenom: "Julie", nom: "Roux", codePostal: "38000", ville: "Grenoble", par: "Stéphanie Guigon" });
  await carte(page, "choisir-gamme", "Lafuge bandes françaises");
  await carte(page, "choisir-modele", "Loft");
  assert.equal(await page.isDisabled('[data-action="choisir-taille"][data-valeur="2,60 m"]'), true, "taille non proposée");
  await carte(page, "choisir-taille", "2,40 m");
  await page.click('[data-action="continuer"][data-id="billard"]');
  assert.match(await texte(page, '[data-section="tapis"]'), /Simonis 330/);
  await carte(page, "choisir-teinte", "Vert anglais");
  await sansDebordement(page);
  await ouvrirSection(page, "options");
  await option(page, "Bandes A37 toilées").click();
  await option(page, "Chauffage de l'ardoise").click();
  await sansDebordement(page);
  assert.equal(await texte(page, "#barre-total"), "10 320 €");
  assert.equal(await page.isVisible("#barre-mobile"), true);
  await page.screenshot({ path: path.join(SORTIES, "telephone-options.png") });
  await page.click('[data-action="voir-recap"]');
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(SORTIES, "telephone-recap.png") });
  const pdf = await generer(page, "5-lafuge-francais");
  for (const attendu of ["Billard français à bandes fixes Loft, 2,40 m", "Bandes A37 toilées", "Chauffage de l'ardoise",
    "Simonis 330, Vert anglais", "10 320 €", "Stéphanie Guigon"]) {
    assert.ok(pdf.texte.includes(attendu), attendu);
  }
  sansMentionsInterdites(pdf.texte, false);
  await sansDebordement(page);
  assert.deepEqual(page.erreurs, []);
});
