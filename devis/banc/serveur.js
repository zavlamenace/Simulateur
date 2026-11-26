/**
 * Banc d'essai local : sert la page Apps Script avec le vrai Code.gs exécuté dans Node (appsscript-simule.js).
 * - les inclusions <?!= include('X'); ?> sont résolues comme dans Apps Script ;
 * - les adresses cdn.jsdelivr.net/npm/ sont servies depuis node_modules (versions vérifiées) ;
 * - Google Fonts est remplacé par les mêmes polices, servies localement ;
 * - google.script.run est remplacé par des appels HTTP vers le serveur simulé.
 *
 * Usage : node serveur.js [port]   (mot de passe du banc : banc-essai-2026)
 */
"use strict";
const fs = require("fs");
const http = require("http");
const path = require("path");
const { creerAppsScript } = require("./appsscript-simule");

const APPSCRIPT = path.join(__dirname, "..", "appscript");
const MODULES = path.join(__dirname, "node_modules");
const MOT_DE_PASSE = "banc-essai-2026";
const TYPES = { ".js": "text/javascript", ".woff": "font/woff", ".woff2": "font/woff2", ".css": "text/css", ".map": "application/json" };

const POLICES_CSS = [["DM Sans", "dm-sans", "5.2.8", [400, 500, 700]], ["EB Garamond", "eb-garamond", "5.2.7", [500, 700]]]
  .map(([famille, paquet, version, graisses]) => graisses.map((g) =>
    `@font-face{font-family:"${famille}";font-weight:${g};font-style:normal;font-display:swap;` +
    `src:url(/npm/@fontsource/${paquet}@${version}/files/${paquet}-latin-${g}-normal.woff) format("woff")}`).join("\n")).join("\n");

const RUN_SIMULE = `
window.google = { script: { run: (function () {
  function executeur(succes, echec) {
    return new Proxy({}, { get: function (_, nom) {
      if (nom === "withSuccessHandler") return function (f) { return executeur(f, echec); };
      if (nom === "withFailureHandler") return function (f) { return executeur(succes, f); };
      return function () {
        var args = Array.prototype.slice.call(arguments);
        fetch("/rpc/" + nom, { method: "POST", body: JSON.stringify(args) }).then(function (r) { return r.json(); }).then(function (r) {
          if ("erreur" in r) { if (echec) echec(new Error(r.erreur)); } else if (succes) succes(r.resultat);
        });
      };
    } });
  }
  return executeur(null, null);
})() } };`;

function page(origine) {
  // Les fichiers réellement collés dans Apps Script (dossier a-copier), inclusions résolues comme par include().
  const COPIER = path.join(APPSCRIPT, "a-copier");
  let html = fs.readFileSync(path.join(COPIER, "Index.html"), "utf8");
  html = html.replace(/<\?!=\s*include\('([^']+)'\);\s*\?>/g, (_, nom) => fs.readFileSync(path.join(COPIER, nom + ".html"), "utf8"));
  // Adresse absolue : pdfmake ne télécharge que les polices dont l'adresse commence par http(s)://.
  html = html.split("https://cdn.jsdelivr.net/npm/").join(origine + "/npm/");
  html = html.replace(/<link rel="preconnect"[^>]*>\s*/g, "");
  html = html.replace(/<link href="https:\/\/fonts\.googleapis\.com[^>]*>/, '<link href="/polices.css" rel="stylesheet">');
  html = html.replace("<script", "<script>" + RUN_SIMULE + "</script>\n  <script");
  // Toute autre ressource externe passerait inaperçue dans le banc (réseau fermé) : on la signale.
  const externes = (html.match(/https?:\/\/[a-z0-9.-]+/gi) || []).filter((u) => !/^https?:\/\/www\.w3\.org$/i.test(u) && u !== origine.replace(/:\d+$/, ""));
  if (externes.length) throw new Error("Ressource externe non servie par le banc : " + Array.from(new Set(externes)).join(", "));
  return html;
}

function fichierNpm(url) {
  const m = /^\/npm\/((?:@[^/]+\/)?[^@/]+)@([^/]+)\/(.+)$/.exec(url);
  if (!m) return null;
  const [, paquet, version, reste] = m;
  const installe = JSON.parse(fs.readFileSync(path.join(MODULES, paquet, "package.json"), "utf8")).version;
  if (installe !== version) throw new Error(`${paquet} : la page demande ${version}, le banc a ${installe}`);
  const chemin = path.normalize(path.join(MODULES, paquet, reste));
  if (!chemin.startsWith(path.join(MODULES, paquet) + path.sep)) return null;
  return chemin;
}

function demarrer(port) {
  const feuilles = JSON.parse(fs.readFileSync(path.join(__dirname, "feuilles.json"), "utf8"));
  const gas = creerAppsScript({ feuilles, motDePasse: MOT_DE_PASSE });
  const serveur = http.createServer((req, res) => {
    try {
      const url = decodeURIComponent(req.url.split("?")[0]);
      if (req.method === "GET" && url === "/") {
        const html = page("http://" + req.headers.host);
        res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
        return res.end(html);
      }
      if (req.method === "GET" && url === "/polices.css") {
        res.writeHead(200, { "Content-Type": "text/css" });
        return res.end(POLICES_CSS);
      }
      if (req.method === "GET" && url.startsWith("/npm/")) {
        const f = fichierNpm(url);
        if (!f || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
        res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream", "Access-Control-Allow-Origin": "*" });
        return fs.createReadStream(f).pipe(res);
      }
      if (req.method === "POST" && url.startsWith("/rpc/")) {
        let corps = "";
        req.on("data", (d) => { corps += d; });
        req.on("end", () => {
          let r;
          try { r = { resultat: gas.appeler(url.slice(5), JSON.parse(corps || "[]")) }; } catch (e) { r = { erreur: e.message }; }
          res.writeHead(200, { "Content-Type": "application/json" });
          res.end(JSON.stringify(r));
        });
        return undefined;
      }
      res.writeHead(404);
      return res.end();
    } catch (e) {
      res.writeHead(500, { "Content-Type": "text/plain; charset=utf-8" });
      return res.end(e.message);
    }
  });
  return new Promise((ok) => serveur.listen(port || 0, "127.0.0.1", () => ok({ serveur, gas, port: serveur.address().port, motDePasse: MOT_DE_PASSE })));
}

module.exports = { demarrer, page };

if (require.main === module) {
  demarrer(Number(process.argv[2]) || 8787).then(({ port }) => console.log(`Banc d'essai : http://127.0.0.1:${port} (mot de passe ${MOT_DE_PASSE})`));
}
