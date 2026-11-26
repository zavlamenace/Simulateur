"""Maquettes de la page 2 du PDF de devis, une par gamme (images fixes)."""
from pathlib import Path

ICI = Path(__file__).parent
MENTION = "Modèle similaire au devis, photo non représentative de votre configuration."

CSS = """
@font-face{font-family:'DM Sans';font-weight:400;src:url(fonts/dm-sans-latin-400-normal.woff2)}
@font-face{font-family:'DM Sans';font-weight:500;src:url(fonts/dm-sans-latin-500-normal.woff2)}
@font-face{font-family:'DM Sans';font-style:italic;src:url(fonts/dm-sans-latin-400-italic.woff2)}
@font-face{font-family:'EB Garamond';font-weight:400;src:url(fonts/eb-garamond-latin-400-normal.woff2)}
@font-face{font-family:'EB Garamond';font-weight:500;src:url(fonts/eb-garamond-latin-500-normal.woff2)}
@font-face{font-family:'EB Garamond';font-style:italic;src:url(fonts/eb-garamond-latin-400-italic.woff2)}
:root{--noir:#151515;--gris:#3d4248;--doux:#6b7075;--sable:#f6f3ee;--lin:#efe9e3;--rouge:#b01c2e;--r:6px}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body.dense .tuile{aspect-ratio:2/1}
body.dense h2{margin-top:16px}
body.dense .pos{margin-top:12px;padding:10px 0}
body.dense .sur{margin-top:16px}
body.dense h1{font-size:34px}
body.dense .histoire{margin-top:16px;margin-bottom:14px}
body{width:794px;height:1123px;padding:40px 52px 30px;font:400 11.5px/1.5 'DM Sans',sans-serif;color:var(--noir);
  display:flex;flex-direction:column}
header{display:flex;justify-content:space-between;align-items:flex-end;padding-bottom:14px;border-bottom:1px solid var(--lin)}
.logos{display:flex;align-items:center;gap:18px}
.logos img{height:34px}
.logos .laf{height:40px}
.maison{font-size:9.5px;color:var(--doux);margin-top:6px}
.ref{text-align:right;font-size:10px;color:var(--doux);line-height:1.6}
.ref b{color:var(--noir);font-weight:500}
.sur{font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--doux);margin-top:22px}
h1{font:400 38px/1.1 'EB Garamond',serif;margin-top:4px}
.sous{font-size:12px;color:var(--gris);margin-top:6px}
figure.hero{margin-top:14px}
figure.hero img{display:block;width:100%;border-radius:var(--r);object-fit:contain}
figure.hero.photo img{object-fit:cover}
figcaption{font-size:9px;font-style:italic;color:var(--doux);margin-top:6px}
.pos{margin-top:18px;padding:14px 0;border-top:1px solid var(--lin);border-bottom:1px solid var(--lin)}
.pos q{font:italic 400 23px/1.2 'EB Garamond',serif;quotes:none}
.pos p{color:var(--gris);font-size:11.5px;margin-top:4px}
h2{font:400 21px/1.2 'EB Garamond',serif;margin-top:22px}
.points{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:12px}
.tuile{aspect-ratio:4/3;border-radius:var(--r);overflow:hidden;background:var(--lin)}
.tuile img{width:100%;height:100%;object-fit:cover;display:block}
.tuile.blanc{background:#fff;border:1px solid var(--lin)}
.tuile.blanc img{object-fit:contain}
.tuile.vide{display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;
  color:var(--doux);font-size:9.5px;padding:12px;gap:2px}
.tuile.vide b{font-weight:500;color:var(--gris)}
.tuile.texte{display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;
  background:var(--sable);padding:14px}
.tuile.texte .grand{font:400 54px/1 'EB Garamond',serif}
.tuile.texte .grand + span{font:italic 15px 'EB Garamond',serif;color:var(--gris)}
.tuile.texte ul{list-style:none;font:400 14.5px/1.45 'EB Garamond',serif}
h3{font-size:12px;font-weight:500;margin-top:9px;line-height:1.35}
.point p{color:var(--gris);font-size:10.5px;margin-top:3px;line-height:1.45}
.histoire{display:grid;grid-template-columns:230px 1fr;gap:22px;margin-top:22px;background:var(--sable);
  border-radius:var(--r);overflow:hidden}
.histoire img{width:100%;height:100%;object-fit:cover;display:block}
.histoire div{padding:18px 20px 16px 0}
.histoire h2{margin:0 0 8px}
.histoire p{font-size:10.5px;color:var(--gris);margin-top:6px;line-height:1.5}
.histoire p b{color:var(--noir);font-weight:500}
.histoire .sign{font:italic 12px/1.4 'EB Garamond',serif;color:var(--noir);margin-top:10px}
.reass{display:flex;justify-content:space-around;gap:8px;margin-top:auto;padding:14px 10px 12px;background:var(--sable);border-radius:var(--r)}
.reass div{display:flex;flex-direction:column;gap:6px;align-items:center;text-align:center;flex:1}
.reass img{width:28px;height:28px;flex:none}
.reass b{display:block;font-weight:500;font-size:10.5px;line-height:1.3}
.reass span{display:block;font-size:9.5px;color:var(--doux);line-height:1.3}
footer{display:flex;justify-content:space-between;font-size:9px;color:var(--doux);margin-top:12px}
"""


def tuile(t):
    kind = t.get("kind", "photo")
    if kind == "photo":
        return f'<div class="tuile"><img src="img/{t["img"]}"></div>'
    if kind == "blanc":
        return f'<div class="tuile blanc"><img src="img/{t["img"]}"></div>'
    if kind == "vide":
        return f'<div class="tuile vide"><b>Photo ultra zoomée à fournir</b>{t["quoi"]}</div>'
    return f'<div class="tuile texte">{t["html"]}</div>'


def page(g):
    logos = '<img src="img/logo-bdf.png">'
    maison = ""
    if g.get("lafuge"):
        logos += '<img class="laf" src="img/logo-lafuge.svg">'
        maison = '<div class="maison">Billard Lafuge, maison du groupe Billards de France</div>'
    points = "".join(
        f'<div class="point">{tuile(p)}<h3>{p["titre"]}</h3><p>{p["texte"]}</p></div>' for p in g["points"])
    reass = "".join(
        f'<div><img src="img/{i}.svg"><p><b>{a}</b><span>{b}</span></p></div>' for i, a, b in g["reass"])
    hero_cls = "hero photo" if g.get("hero_photo") else "hero"
    hero_style = f'style="height:{g["hero_h"]}px"'
    histoire = g.get("histoire", "")
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{CSS}</style></head><body class="{'dense' if g.get('lafuge') else ''}">
<header><div><div class="logos">{logos}</div>{maison}</div>
<div class="ref"><b>Devis n° 2026-0142</b><br>Pour M. et Mme Martin · 26 novembre 2026</div></header>
<p class="sur">Votre billard</p>
<h1>{g["modele"]}</h1>
<p class="sous">{g["sous"]}</p>
<figure class="{hero_cls}"><img src="img/{g["hero"]}" {hero_style}><figcaption>{MENTION}</figcaption></figure>
<div class="pos"><q>{g["pos"]}</q><p>{g["pos_texte"]}</p></div>
<h2>Les points forts</h2>
<div class="points">{points}</div>
{histoire}
<div class="reass">{reass}</div>
<footer><span>billardsdefrance.fr · 05 62 69 30 20</span><span>Page 2 sur 3</span></footer>
</body></html>"""


LIVRAISON = ("truck", "Livraison offerte", "partout en France")
MONTAGE = ("unloading", "Montage à domicile", "avec des experts dédiés")
ONEY = ("lock", "Paiement en 3x ou 4x", "sans frais avec Oney")
SECURISE = ("lock", "Paiement sécurisé", "carte, PayPal, Apple Pay, Wero")
PLAISANCE = ("hands", "Fabrication artisanale", "à Plaisance-du-Gers")
FAMILLE = ("wood", "Famille d'ébénistes", "3 générations depuis 1946")

GAMMES = {
    "reference": dict(
        modele="Caracas Premium",
        sous="Billard convertible 2,10 m · pieds bois massif · tapis bleu",
        hero="hero-ref.jpg", hero_h=345,
        pos="Le meilleur rapport qualité-prix du marché.",
        pos_texte="Ardoise monobloc, structure en bois massif et pack accessoires inclus.",
        points=[
            dict(kind="vide", quoi="Tranche de l'ardoise", titre="Ardoise monobloc de 19 mm",
                 texte="Une pierre naturelle d'un seul tenant : elle ne gonfle pas et ne se déforme pas avec "
                       "l'humidité, contrairement au MDF."),
            dict(kind="blanc", img="ref-pack.jpg", titre="Pack accessoires offert",
                 texte="16 billes, 4 queues, triangle, craies, brosse et porte-queue inclus (valeur 330 €)."),
            dict(img="ref-pieds.jpg", titre="Pieds bois massif et Formica",
                 texte="Le matériau des plans de travail de cuisine : il résiste aux chocs, aux rayures et aux taches."),
        ],
        reass=[LIVRAISON, MONTAGE, ONEY],
    ),
    "design": dict(
        modele="Boston",
        sous="Billard convertible laqué 2,10 m · laque gris clair · tapis noir",
        hero="hero-design.jpg", hero_h=300,
        pos="Le meilleur rapport qualité-prix en fabrication française.",
        pos_texte="Un billard laqué, fabriqué à la main dans nos ateliers du Gers.",
        points=[
            dict(img="design-drap.jpg", titre="Drap Simonis 760 ou Strachan 777 inclus",
                 texte="Les draps des grandes compétitions internationales, en 26 couleurs, sans supplément."),
            dict(kind="vide", quoi="Tranche de l'ardoise", titre="Ardoise italienne monobloc de 19 mm",
                 texte="Une pierre naturelle d'un seul tenant : elle ne se déforme pas avec l'humidité, "
                       "contrairement au MDF."),
            dict(img="design-bandes.jpg", titre="Bandes interchangeables brevetées",
                 texte="Plusieurs jeux sur un même billard : français, américain ou pool, à vous de choisir."),
        ],
        reass=[PLAISANCE, FAMILLE, LIVRAISON, MONTAGE, SECURISE],
    ),
    "prestige": dict(
        modele="Paris",
        sous="Billard convertible 2,10 m · pieds bois massif · tapis bleu",
        hero="hero-prest.jpg", hero_h=300,
        pos="Le billard convertible le plus fonctionnel du marché.",
        pos_texte="Rangements intégrés, réception centralisée des billes, allonge incluse.",
        points=[
            dict(kind="texte", html='<span class="grand">12</span><span>couverts</span>',
                 titre="12 couverts, allonge incluse",
                 texte="Avec le plateau bois, l'allonge de 45 cm est fournie."),
            dict(img="prest-reception.jpg", titre="Réception centralisée et insonorisée",
                 texte="Goulottes capitonnées en 3 épaisseurs, un tiroir abattant de chaque côté."),
            dict(img="prest-drap.jpg", titre="Drap Simonis 760 ou Strachan 777 inclus",
                 texte="Les draps des grandes compétitions internationales, en 26 couleurs, sans supplément."),
        ],
        reass=[PLAISANCE, FAMILLE, LIVRAISON, MONTAGE, SECURISE],
    ),
    "lafuge": dict(
        lafuge=True,
        modele="Chambord",
        sous="Billard mixte 2,60 m · chêne massif français, finition brossée blanchie · drap Simonis 760",
        hero="chambord.jpg", hero_photo=True, hero_h=190,
        pos="Le billard le plus personnalisable.",
        pos_texte="Essence, teinte, laque, taille, finitions, liserés : chaque détail est à votre choix.",
        points=[
            dict(img="laf-mains.jpg", titre="Une pièce unique, faite à la main",
                 texte="Fabriquée à l'unité par un seul ébéniste, du début à la fin."),
            dict(img="laf-planches.jpg", titre="Essences nobles massives",
                 texte="Chêne, érable et noyer massifs français, ou mélèze massif."),
            dict(kind="texte", html="<ul><li>Yacht Club de Monaco</li><li>Sheraton Paris</li>"
                                    "<li>Villas de la Côte d'Azur</li></ul>",
                 titre="Ils nous ont choisis",
                 texte="Et des villas prestigieuses de la côte atlantique."),
        ],
        histoire="""<section class="histoire"><img src="img/laf-atelier.jpg"><div>
<h2>Votre billard naîtra en Chartreuse</h2>
<p><b>Le lieu.</b> Au cœur du parc naturel régional de Chartreuse, notre atelier de Miribel-les-Échelles ne fabrique que des pièces uniques.</p>
<p><b>La main.</b> Tout part du tronc d'arbre. Un seul ébéniste façonne votre billard, du choix du bois à la dernière finition.</p>
<p><b>Le temps.</b> Quelques semaines pour le fabriquer, des générations pour en profiter.</p>
<p class="sign">Trois générations de la famille Fitan au service du bois massif depuis 1946.</p>
</div></section>""",
        reass=[("hands", "Fait à la main", "à Miribel-les-Échelles"),
               ("sliders", "Sur mesure", "chaque détail à votre choix"),
               ("unloading", "Livraison et installation", "par nos équipes"),
               SECURISE],
    ),
}

if __name__ == "__main__":
    for nom, g in GAMMES.items():
        (ICI / f"page2-{nom}.html").write_text(page(g), encoding="utf-8")
        print(nom)
