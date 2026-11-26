// Tests du moteur de devis (devis/appscript/calcul.js) sur le catalogue exporté du classeur de trace.
// Lancer : cd devis/banc && npm test
const test = require("node:test");
const assert = require("node:assert/strict");
const path = require("node:path");
const C = require("../../appscript/calcul.js");
const cat = require(path.join(__dirname, "..", "catalogue.json"));

function config(extra) {
  const cfg = Object.assign({ realisePar: "Xavier Fitan", client: { nom: "Martin", telephone: "0600000000", codePostal: "32160", ville: "Plaisance" },
    options: {}, accessoires: {}, lignesLibres: [], remises: {}, livraison: { formule: "offerte" } }, extra);
  C.nettoyer(C.options(cat, cfg), cfg);
  return cfg;
}

function choisir(cfg, nom) {
  const opts = C.options(cat, cfg);
  const o = opts.find((x) => x.nom === nom);
  assert.ok(o, "option introuvable : " + nom);
  C.basculer(opts, cfg, o.id, true);
  return o;
}

test("gammes : 5 gammes, Lafuge par taille", () => {
  const g = C.gammes(cat).map((x) => x.id);
  assert.deepEqual(g, ["Référence", "Design", "Prestige", "Lafuge mixte", "Lafuge bandes françaises"]);
  assert.equal(C.gamme(cat, "Lafuge mixte").jeu, "mixte");
  assert.equal(C.gamme(cat, "Lafuge bandes françaises").famille, "Lafuge");
});

test("format des prix", () => {
  assert.equal(C.euros(12600), "12 600 €");
  assert.equal(C.euros(598.5), "598,50 €");
});

test("Référence : billard, tapis et jeu inclus par défaut, kit, livraison offerte, échéancier Plaisance, Oney", () => {
  const cfg = config({ gamme: "Référence", modele: "Santiago", versionModele: "Pieds bois massif", tapis: { drap: "Standard", teinte: "Vert" } });
  const l = C.lignes(cat, cfg);
  assert.equal(l[0].prixUnitaire, 1995);
  assert.ok(l.some((x) => x.libelle.startsWith("Tapis standard") && x.inclus));
  const kit = l.find((x) => x.id === "kit");
  assert.ok(kit && kit.inclus && kit.valeurOfferte === 330);
  assert.equal(l.find((x) => x.id === "livraison").valeurOfferte, 300);
  const t = C.totaux(cat, cfg, l);
  assert.equal(t.total, 1995);
  assert.equal(t.echeances.length, 2);
  assert.equal(t.echeances[0].montant, 598.5);
  assert.equal(t.echeances[1].montant, 1396.5);
  assert.equal(t.tva, 332.5);
  assert.ok(t.oney);
  assert.deepEqual(C.problemes(cat, cfg), []);
});

test("Référence : couleur des pieds seulement sur la version métal", () => {
  const bois = config({ gamme: "Référence", modele: "Rio", versionModele: "Pieds bois massif" });
  assert.ok(!C.options(cat, bois).some((o) => o.groupe === "Couleur des pieds"));
  const metal = config({ gamme: "Référence", modele: "Rio", versionModele: "Pieds métalliques" });
  assert.ok(C.options(cat, metal).some((o) => o.groupe === "Couleur des pieds"));
  assert.equal(C.lignes(cat, metal)[0].prixUnitaire, 2395);
});

test("Design : nécessite (allonge, vernis du dessus) et exclusion du 2e jeu identique au jeu inclus", () => {
  const cfg = config({ gamme: "Design", modele: "Boston", versionModele: "Pieds carrés hêtre 120 × 120", tapis: { drap: "Simonis 760", teinte: "Noir" } });
  let opts = C.options(cat, cfg);
  let e = C.etats(opts, cfg);
  const allonge = opts.find((o) => o.nom === "Allonge de plateau 45 cm");
  assert.equal(e[allonge.id].disponible, false);
  const jeuInclus = opts.find((o) => o.groupe === "Jeu de bandes inclus" && cfg.options[o.id] && cfg.options[o.id].choisi);
  assert.equal(jeuInclus.nom, "Jeu de bandes français");
  const deuxiemeFr = opts.find((o) => o.nom === "2e jeu de bandes français");
  assert.equal(e[deuxiemeFr.id].disponible, false);
  choisir(cfg, "Couleur RAL au choix");
  choisir(cfg, "Plateau table bois laqué");
  choisir(cfg, "Allonge de plateau 45 cm");
  choisir(cfg, "2e jeu de bandes américain");
  const t = C.totaux(cat, cfg);
  assert.equal(t.total, 4390 + 250 + 990 + 500 + 700);
  // retirer le plateau retire l'allonge en cascade
  opts = C.options(cat, cfg);
  const retirees = C.basculer(opts, cfg, opts.find((o) => o.nom === "Plateau table bois laqué").id, false);
  assert.deepEqual(retirees, ["Allonge de plateau 45 cm"]);
  assert.equal(C.totaux(cat, cfg).total, 4390 + 250 + 700);
});

test("Prestige : remise par ligne en %, remise globale en €", () => {
  const cfg = config({ gamme: "Prestige", modele: "Paris", versionModele: "Pieds gainés de cuir 100 × 100", tapis: { drap: "Simonis 760", teinte: "Vert anglais" } });
  choisir(cfg, "Plateau table bois");
  cfg.remises = { billard: { type: "%", valeur: 10 } };
  cfg.remiseGlobale = { type: "€", valeur: 500 };
  const t = C.totaux(cat, cfg);
  assert.equal(t.brut, 8800 + 990);
  assert.equal(t.remisesLignes, 880);
  assert.equal(t.remiseGlobale, 500);
  assert.equal(t.total, 8800 + 990 - 880 - 500);
  assert.ok(!t.oney);
});

test("Lafuge mixte : Chambord 12 pieds, snooker par défaut, laque et chêne exclusifs, sur demande, ligne libre ×2", () => {
  const cfg = config({ gamme: "Lafuge mixte", modele: "Chambord", taille: "12 pieds", tapis: { drap: "Simonis 760", teinte: "Vert anglais" } });
  let opts = C.options(cat, cfg);
  assert.ok(!opts.some((o) => o.nom === "Retour centralisé des billes"), "impossible en 12 pieds");
  assert.ok(!opts.some((o) => o.nom === "2e jeu de bandes interchangeables"));
  assert.ok(!opts.some((o) => o.section === "plateau"), "pas de version table");
  const jeu = opts.filter((o) => o.groupe === "Bandes initiales (une incluse)" && cfg.options[o.id] && cfg.options[o.id].choisi);
  assert.deepEqual(jeu.map((o) => o.nom), ["Snooker"]);
  choisir(cfg, "Laque");
  opts = C.options(cat, cfg);
  const e = C.etats(opts, cfg);
  assert.equal(e[opts.find((o) => o.nom === "Chêne massif").id].disponible, false);
  assert.equal(e[opts.find((o) => o.nom === "Repères de bandes en nacre").id].disponible, false);
  const cadre = choisir(cfg, "Cadre snooker");
  assert.equal(cadre.prix, 1000);
  const sd = choisir(cfg, "Cadre démontable");
  assert.equal(sd.etat, "sur_demande");
  assert.ok(C.problemes(cat, cfg).some((p) => p.startsWith("Saisir le prix : Cadre démontable")));
  cfg.options[sd.id].prixManuel = 600;
  cfg.lignesLibres = [{ libelle: "Queue de compétition", prix: 350, quantite: 2 }];
  const t = C.totaux(cat, cfg);
  assert.equal(t.total, 24000 + 2760 + 1000 + 600 + 700);
  assert.equal(t.echeances.length, 3);
  assert.equal(t.echeances[0].montant, 8718);
  assert.equal(t.echeances[1].montant, 8718);
  assert.equal(t.echeances[2].montant, 29060 - 2 * 8718);
  assert.deepEqual(C.problemes(cat, cfg), ["Saisir le prix : Livraison et installation par nos équipes"]);
  cfg.livraison = { formule: "montage", prix: 1500 };
  assert.deepEqual(C.problemes(cat, cfg), []);
  assert.equal(C.totaux(cat, cfg).total, 29060 + 1500);
});

test("Lafuge français : Loft 2,40 m, A37 en option, chauffage, finitions sur chêne uniquement", () => {
  const cfg = config({ gamme: "Lafuge bandes françaises", modele: "Loft", taille: "2,40 m", tapis: { drap: "Simonis 330", teinte: "Bleu" } });
  const opts = C.options(cat, cfg);
  assert.equal(opts.find((o) => o.nom === "Bandes A37 toilées").prix, 750);
  assert.equal(opts.find((o) => o.nom === "Chauffage de l'ardoise").prix, 1800);
  const e = C.etats(opts, cfg);
  assert.equal(e[opts.find((o) => o.nom === "Finition brossée").id].disponible, false);
  choisir(cfg, "Chêne massif");
  choisir(cfg, "Finition brossée");
  choisir(cfg, "Bandes A37 toilées");
  assert.equal(C.totaux(cat, cfg).total, 7770 + 820 + 820 + 750);
  assert.deepEqual(C.draps(cat, cfg).map((d) => d.nom), ["Simonis 330"]);
});

test("Lafuge : A37 inclus dès 2,60 m, plateau encastré et supplément verre", () => {
  const cfg = config({ gamme: "Lafuge bandes françaises", modele: "Arcade", taille: "2,60 m", tapis: { drap: "Simonis 330", teinte: "Vert" } });
  assert.equal(C.options(cat, cfg).find((o) => o.nom === "Bandes A37 toilées").etat, "inclus");
  const mixte = config({ gamme: "Lafuge mixte", modele: "Loft", taille: "2,30 m", tapis: { drap: "Simonis 760", teinte: "Gris" } });
  let opts = C.options(cat, mixte);
  const verre = opts.find((o) => o.nom === "Verre Sécurit 8 mm transparent et bois");
  assert.equal(C.etats(opts, mixte)[verre.id].disponible, false);
  choisir(mixte, "Plateau encastré laqué");
  choisir(mixte, "Verre Sécurit 8 mm transparent et bois");
  choisir(mixte, "Rallonge 50 cm teintée");
  assert.equal(C.totaux(cat, mixte).total, 6300 + 1720 + 1400 + 470);
});

test("Fiche technique Lafuge : de base, bois massif, laquée", () => {
  const cfg = config({ gamme: "Lafuge mixte", modele: "Soho", taille: "2,30 m" });
  const base = Object.fromEntries(C.ficheTechnique(cat, cfg).map((x) => [x.element, x.valeur]));
  assert.equal(base.Cadre, "MDF plaqué chêne");
  choisir(cfg, "Chêne massif");
  const massif = Object.fromEntries(C.ficheTechnique(cat, cfg).map((x) => [x.element, x.valeur]));
  assert.equal(massif.Cadre, "Chêne massif");
  const city = config({ gamme: "Lafuge mixte", modele: "City", taille: "2,30 m" });
  const f = C.ficheTechnique(cat, city);
  assert.ok(f.some((x) => x.element === "Forme des pieds" && x.valeur === "Biseautés"));
  assert.equal(f.find((x) => x.element === "Châssis").valeur.startsWith("Double barre"), true);
  const eos = config({ gamme: "Lafuge mixte", modele: "Éos", taille: "2,30 m" });
  assert.ok(!C.ficheTechnique(cat, eos).some((x) => x.element === "Forme des pieds"));
  const laque = config({ gamme: "Lafuge mixte", modele: "Loft", taille: "2,30 m" });
  choisir(laque, "Laque");
  assert.equal(Object.fromEntries(C.ficheTechnique(cat, laque).map((x) => [x.element, x.valeur])).Cadre, "MDF");
});

test("Arguments : 4 au maximum par défaut, liste Lafuge par jeu", () => {
  const r = config({ gamme: "Référence", modele: "Rio", versionModele: "Pieds métalliques" });
  const d = C.argumentsParDefaut(cat, r);
  assert.ok(d.length <= 4 && d.includes("Pieds métalliques de 5 mm") && !d.includes("Pieds bois massif et Formica"));
  const fr = config({ gamme: "Lafuge bandes françaises", modele: "Loft", taille: "2,30 m" });
  assert.ok(C.argumentsGamme(cat, fr).some((a) => a.titre === "Chauffage de l'ardoise"));
});

test("Contrôles avant PDF et récap CRM", () => {
  const vide = { gamme: "Design", options: {} };
  const p = C.problemes(cat, vide);
  assert.ok(p.includes("Nom du client") && p.includes("Choisir un modèle") && p.includes("Choisir qui réalise le devis"));
  const cfg = config({ gamme: "Design", modele: "Miami", versionModele: "Pieds carrés hêtre 120 × 120", tapis: { drap: "Strachan 777", teinte: "Bleu" } });
  const recap = C.recapCRM(cat, cfg, "BDF-2026-0001");
  assert.match(recap, /Devis BDF-2026-0001/);
  assert.match(recap, /Total TTC : 4 390 €/);
});

test("26/11 : Lafuge livré et installé par nos équipes, cuir noir ou SOFIC, gris du Simonis", () => {
  const cfg = { gamme: "Lafuge mixte", modele: "Loft", taille: "2,30 m", options: {}, livraison: { formule: "offerte" } };
  assert.equal(C.formuleLivraison(cat, cfg), "montage");
  const liv = C.lignes(cat, cfg).find((l) => l.id === "livraison");
  assert.equal(liv.libelle, "Livraison et installation par nos équipes");
  assert.equal(liv.aSaisir, true);
  assert.ok(C.problemes(cat, cfg).includes("Saisir le prix : Livraison et installation par nos équipes"));
  assert.equal(C.livraisonOfferte(cat, C.gamme(cat, "Lafuge bandes françaises")), null);
  assert.equal(C.formuleLivraison(cat, { gamme: "Design", livraison: { formule: "offerte" } }), "offerte");
  const opts = C.options(cat, cfg);
  const cuir = opts.filter((o) => o.groupe === "Entrées de poche en cuir");
  assert.deepEqual(cuir.map((o) => [o.nom, o.choix, o.necessite.length]),
    [["Entrées de poche en cuir noir", C.UN_SEUL, 0], ["Cuir de couleur (gamme SOFIC)", C.UN_SEUL, 0]]);
  C.basculer(opts, cfg, cuir[0].id, true);
  C.basculer(opts, cfg, cuir[1].id, true);
  assert.equal(cfg.options[cuir[0].id].choisi, false);
  const gris = C.teintes(cat, "Simonis 760").map((t) => t.nom).filter((n) => /^Gris|^Noir/.test(n));
  assert.deepEqual(gris, ["Gris clair", "Gris ardoise", "Noir"]);
  assert.deepEqual(C.teintes(cat, "Simonis 330").map((t) => t.nom), C.teintes(cat, "Simonis 760").map((t) => t.nom));
  assert.ok(C.teintes(cat, "Strachan 777").some((t) => t.nom === "Gris"));
});

test("Arguments liés aux choix : imprimés sous la ligne, seulement au statut « Actif »", () => {
  const c = JSON.parse(JSON.stringify(cat));
  c["Lafuge contenus"]["ARGUMENTS DES CHOIX"] = [
    { Choix: "Chêne massif", "Texte imprimé sous la ligne": "Chêne massif de France", Statut: "Actif" },
    { Choix: "Strachan 777", "Texte imprimé sous la ligne": "Le drap des grands tournois", Statut: "Actif" },
    { Choix: "Érable sycomore massif", "Texte imprimé sous la ligne": "Érable sycomore massif", Statut: "Actif" },
    { Choix: "Bandes initiales américaines", "Texte imprimé sous la ligne": "Brouillon", Statut: "À valider" },
  ];
  const cfg = { gamme: "Lafuge mixte", modele: "Loft", taille: "2,30 m", options: {}, tapis: { drap: "Strachan 777", teinte: "Vert" } };
  let opts = C.options(c, cfg);
  C.nettoyer(opts, cfg);
  let l = C.lignes(c, cfg);
  assert.match(l[0].detail, /\nÉrable sycomore massif$/, "matière de base sous le billard");
  assert.equal(l.find((x) => x.id === "tapis").detail, "Le drap des grands tournois");
  assert.equal(l.find((x) => /Bandes initiales américaines/.test(x.libelle)).detail, "", "brouillon jamais imprimé");
  C.basculer(opts, cfg, opts.find((o) => o.nom === "Chêne massif").id, true);
  l = C.lignes(c, cfg);
  assert.equal(l.find((x) => x.libelle === "Chêne massif").detail, "Chêne massif de France");
  assert.doesNotMatch(l[0].detail, /Érable/, "plus d'érable sous le billard une fois l'essence choisie");
});

