"""Maquettes finales de la présentation en tête du PDF (28/11).

Base : la première version (26/11), retenue par la direction. Ajouts :
- la photo détourée est rétrécie d'un quart de la largeur de la page et décalée à gauche ;
- une vignette « En table » à sa droite, à la même hauteur ;
- le jeu choisi dans la ligne de configuration ;
- Lafuge : deuxième page « bois brut → billard brut → finitions → drap », dans l'aspect du bloc histoire de la V1.
Textes : ceux du Sheet, relus par l'équipe le 27/11.
"""
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
:root{--noir:#151515;--gris:#3d4248;--doux:#6b7075;--sable:#f6f3ee;--lin:#efe9e3;--r:6px}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{width:794px;height:1123px;padding:40px 52px 30px;font:400 11.5px/1.5 'DM Sans',sans-serif;color:var(--noir);
  display:flex;flex-direction:column}
header{display:flex;justify-content:space-between;align-items:flex-end;padding-bottom:14px;border-bottom:1px solid var(--lin)}
header img{height:34px;display:block}
header img.laf{height:46px}
.ref{text-align:right;font-size:10px;color:var(--doux);line-height:1.6}
.ref b{color:var(--noir);font-weight:500}
.sur{font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--doux);margin-top:26px}
h1{font:400 38px/1.1 'EB Garamond',serif;margin-top:4px}
.sous{font-size:12px;color:var(--gris);margin-top:6px}
.hero{display:grid;grid-template-columns:492px 1fr;align-items:center;margin-top:22px}
.hero .vignette{justify-self:end}
.hero .principale{display:block;width:100%;height:auto;max-height:300px;object-fit:contain;object-position:left center;border-radius:var(--r)}
.hero .principale.photo{height:300px;object-fit:cover;object-position:center}
.vignette img,.vignette .vide{display:block;width:190px;height:143px;border-radius:var(--r);object-fit:cover}
.vignette img.detouree{object-fit:contain;border:1px solid var(--lin);background:#fff}
.vignette figcaption{font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--doux);margin-top:7px}
.vide{display:flex;align-items:center;justify-content:center;flex-direction:column;background:var(--lin);color:var(--doux);
  font-size:9.5px;text-align:center;padding:10px}
.mention{font-size:9px;font-style:italic;color:var(--doux);margin-top:6px}
.pos{margin-top:24px;padding:14px 0;border-top:1px solid var(--lin);border-bottom:1px solid var(--lin)}
.pos q{font:italic 400 23px/1.25 'EB Garamond',serif;quotes:none}
h2{font:400 21px/1.2 'EB Garamond',serif;margin-top:30px}
.points{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:12px}
.tuile{aspect-ratio:4/3;border-radius:var(--r);overflow:hidden;background:var(--lin)}
.tuile img{width:100%;height:100%;object-fit:cover;display:block}
.tuile.blanc{background:#fff;border:1px solid var(--lin)}
.tuile.blanc img{object-fit:contain}
.tuile.texte{display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;
  background:var(--sable);padding:14px;font:400 14.5px/1.45 'EB Garamond',serif}
h3{font-size:12px;font-weight:500;margin-top:9px;line-height:1.35}
.point p{color:var(--gris);font-size:10.5px;margin-top:3px;line-height:1.45}
.reass{display:flex;justify-content:space-around;gap:8px;margin-top:auto;padding:14px 10px 12px;background:var(--sable);border-radius:var(--r)}
.reass div{display:flex;flex-direction:column;gap:6px;align-items:center;text-align:center;flex:1}
.reass img{width:28px;height:28px;flex:none}
.reass b{display:block;font-weight:500;font-size:10.5px;line-height:1.3}
.reass span{display:block;font-size:9.5px;color:var(--doux);line-height:1.3}
footer{display:flex;justify-content:space-between;font-size:9px;color:var(--doux);margin-top:12px}
/* Page « Votre billard naîtra en Chartreuse » */
.intro{font:400 15px/1.5 'EB Garamond',serif;color:var(--gris);margin-top:8px;max-width:600px}
.etapes{display:flex;flex-direction:column;gap:14px;margin-top:20px}
.etape{display:grid;grid-template-columns:240px 1fr;grid-template-rows:176px;gap:22px;background:var(--sable);border-radius:var(--r);overflow:hidden;height:176px}
.etape img{width:240px;height:176px;object-fit:cover;display:block}
.etape img.bas{object-position:center 80%}
.etape div{padding:20px 22px 16px 0;display:flex;flex-direction:column;justify-content:center}
.etape .num{font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--doux)}
.etape h2{margin:4px 0 8px}
.etape p{font-size:11px;color:var(--gris);line-height:1.55}
.sign{font:italic 13px/1.4 'EB Garamond',serif;color:var(--noir);margin-top:auto;padding-top:16px}
"""


def tete(g):
    logo = '<img class="laf" src="img/logo-lafuge.svg">' if g.get("lafuge") else '<img src="img/logo-bdf.png">'
    return (f'<header>{logo}<div class="ref"><b>Devis n° 2026-0142</b><br>'
            f'Pour M. et Mme Martin · 28 novembre 2026</div></header>')


def pied(g, page):
    gauche = ("Billard Lafuge, maison du groupe Billards de France · billard-lafuge.fr" if g.get("lafuge")
              else "billardsdefrance.fr · 05 62 69 30 20")
    return f'<footer><span>{gauche}</span><span>{page}</span></footer>'


def visuel(src, cls=""):
    if src.startswith("vide:"):
        return f'<div class="vide">{src[5:]}</div>'
    return f'<img class="{cls}" src="img/{src}">'


def tuile(p):
    if "texte_tuile" in p:
        return f'<div class="tuile texte">{p["texte_tuile"]}</div>'
    if p["img"].startswith("vide:"):
        return f'<div class="tuile vide">{p["img"][5:]}</div>'
    cls = "tuile blanc" if p.get("blanc") else "tuile"
    return f'<div class="{cls}"><img src="img/{p["img"]}"></div>'


def presentation(g, page):
    hero_cls = "principale photo" if g.get("photo") else "principale"
    vign = g["vignette"]
    vign_cls = "detouree" if vign[2] else ""
    points = "".join(f'<div class="point">{tuile(p)}<h3>{p["titre"]}</h3><p>{p["texte"]}</p></div>'
                     for p in g["points"])
    reass = "".join(f'<div><img src="img/{i}.svg"><p><b>{a}</b><span>{b}</span></p></div>' for i, a, b in g["reass"])
    return html(f"""{tete(g)}
<p class="sur">Votre billard</p>
<h1>{g["modele"]}</h1>
<p class="sous">{g["sous"]}</p>
<section class="hero"><img class="{hero_cls}" src="img/{g["hero"]}">
<figure class="vignette">{visuel(vign[0], vign_cls)}<figcaption>{vign[1]}</figcaption></figure></section>
<p class="mention">{MENTION}</p>
<div class="pos"><q>{g["accroche"]}</q></div>
<h2>Les points forts</h2>
<div class="points">{points}</div>
<div class="reass">{reass}</div>
{pied(g, page)}""")


def html(corps):
    return f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{corps}</body></html>'


FAMILLE = ("wood", "3e génération", "famille d'ébénistes depuis 1946")
INVENTEUR = ("sliders", "Inventeur du convertible en table", "depuis 1985")
LIVRAISON = ("truck", "Livraison offerte", "partout en France")
MAIN_GERS = ("hands", "Fabrication à la main", "à Plaisance-du-Gers")
SECURISE = ("lock", "Paiement sécurisé", "carte, PayPal, Apple Pay, Wero")
A_VENIR = "vide:Photo à venir"

GAMMES = {
    "reference": dict(
        modele="Caracas Premium",
        sous="Billard convertible en table 2,10 m · jeu américain · pieds bois massif · tapis bleu royal",
        hero="hero-ref.jpg", vignette=("ref-table-detouree.jpg", "En table", True),
        accroche="Le meilleur rapport qualité-prix du marché en 2,10 m.",
        points=[dict(img=A_VENIR, titre="Ardoise monobloc de 19 mm",
                     texte="Une pierre naturelle durable : elle ne se déforme pas avec l'humidité, contrairement au "
                           "MDF ou aggloméré."),
                dict(img="ref-pack.jpg", blanc=True, titre="Pack accessoires inclus, d'une valeur de 300 €",
                     texte="16 billes (US Ø 57 mm ou Pool Ø 50,8 mm), 1 boîte de craies, 4 queues de 120 cm, "
                           "1 triangle, 1 brosse, 1 porte-queue."),
                dict(img="ref-pieds.jpg", titre="Pieds bois massif et Formica",
                     texte="Le Formica, le matériau robuste des plans de travail de cuisine : il résiste aux chocs, aux "
                           "rayures, à l'humidité et aux taches, contrairement au papier décor.")],
        reass=[INVENTEUR, FAMILLE, LIVRAISON, ("lock", "Paiement en 3x ou 4x", "sans frais avec Oney")],
    ),
    "design": dict(
        modele="Boston",
        sous="Billard convertible en table 2,10 m · jeu américain · laque gris clair · tapis Simonis 760 bleu",
        hero="hero-design.jpg", vignette=("design-table.jpg", "En table", False),
        accroche="Le billard convertible en table, laqué et fabriqué à la main dans notre atelier du Gers.",
        points=[dict(img="design-drap.jpg", titre="Drap Simonis 760 ou Strachan 777 inclus",
                     texte="Les draps des grandes compétitions internationales, disponibles en 26 couleurs, sans "
                           "supplément."),
                dict(img=A_VENIR, titre="Ardoise italienne monobloc de 19 mm",
                     texte="Une pierre naturelle durable provenant d'un schiste italien réputé pour sa densité : elle ne "
                           "se déforme pas avec l'humidité, contrairement au MDF ou à l'aggloméré."),
                dict(img=A_VENIR, titre="Bandes interchangeables brevetées",
                     texte="Plusieurs jeux sur un même billard : français, américain ou pool, à vous de choisir.")],
        reass=[MAIN_GERS, FAMILLE, INVENTEUR, LIVRAISON, SECURISE],
    ),
    "prestige": dict(
        modele="Paris",
        sous="Billard convertible en table 2,10 m · jeu américain · cuir noir et chêne naturel · tapis Simonis 760 bleu",
        hero="hero-prest.jpg", vignette=("vide:Photo détourée<br>en table à venir", "En table", False),
        accroche="Le billard convertible en table le plus fonctionnel du marché.",
        points=[dict(img=A_VENIR, titre="Bandes interchangeables brevetées",
                     texte="Plusieurs jeux sur un même billard : vous passez d'un jeu à l'autre en changeant de bandes."),
                dict(img=A_VENIR, titre="Rangement intégré de tous les accessoires",
                     texte="Le système Octopack permet de ranger sous le billard queues, billes, bandes, craies, brosse "
                           "et plateaux."),
                dict(img="prest-reception.jpg", titre="Réception centralisée et insonorisée",
                     texte="Goulottes capitonnées en 3 épaisseurs, un tiroir abattant de chaque côté.")],
        reass=[MAIN_GERS, FAMILLE, INVENTEUR, LIVRAISON, SECURISE],
    ),
    "lafuge": dict(
        lafuge=True, modele="Chambord", photo=True,
        sous="Billard mixte 2,60 m · jeu américain · chêne massif français, finition brossée blanchie · drap Simonis 760",
        hero="laf-billard.jpg", vignette=("laf-detail2.jpg", "Détail du pied", False),
        accroche="Le billard le plus personnalisable.",
        points=[dict(img="laf-mains.jpg", titre="Une pièce unique, faite à la main",
                     texte="Fabriquée à l'unité par un seul ébéniste, du début à la fin."),
                dict(img="laf-planches.jpg", titre="Essences nobles massives",
                     texte="Chêne, érable et noyer massifs français, ou mélèze massif."),
                dict(texte_tuile="Yacht Club de Monaco<br>Sheraton Paris<br>Villas de la Côte d'Azur",
                     titre="Ils nous ont choisis", texte="Et des villas prestigieuses de la côte atlantique.")],
        reass=[("hands", "Fabrication artisanale", "à Miribel-les-Échelles"), FAMILLE,
               ("sliders", "Sur mesure", "chaque détail à votre choix"),
               ("truck", "Livré et installé", "par nos équipes ou notre réseau formé"), SECURISE],
    ),
}

ETAPES = [
    ("laf-planches-haut.jpg", "La noblesse du bois brut",
     "Tout part du tronc d'arbre. Chêne, érable et noyer français, ou mélèze, sont choisis en plateaux bruts pour leur "
     "veinage, puis travaillés en massif."),
    ("laf-atelier.jpg", "Du bois au billard brut",
     "Un seul ébéniste débite, assemble et ajuste chaque pièce à la main. Le cadre, les pieds et le châssis prennent "
     "forme : votre billard existe, encore brut."),
    ("laf-laque.jpg", "Des finitions à votre image",
     "Teinte, laque, liserés, repères : chaque finition suit vos choix. La laque est appliquée dans une cabine dédiée, "
     "dans la couleur que vous avez retenue."),
    ("laf-drap.jpg", "Le drap, dernière étape",
     "Le drap est coupé puis tendu à la main. Habillé et réglé, votre billard est prêt à prendre place chez vous et à "
     "donner son caractère à la pièce."),
]


def histoire(g, page):
    etapes = "".join(
        f'<section class="etape"><img class="{"bas" if i == 1 else ""}" src="img/{img}"><div><span class="num">0{i}</span><h2>{titre}</h2>'
        f'<p>{texte}</p></div></section>' for i, (img, titre, texte) in enumerate(ETAPES, start=1))
    return html(f"""{tete(g)}
<p class="sur">Fabrication</p>
<h1>Votre billard naîtra en Chartreuse</h1>
<p class="intro">Chaque billard Lafuge est fabriqué à l'unité dans notre atelier de Miribel-les-Échelles, au cœur du
parc naturel régional de Chartreuse. Un seul ébéniste le suit, du bois brut à la pose du drap.</p>
<div class="etapes">{etapes}</div>
<p class="sign">Trois générations de la famille Fitan au service du bois massif depuis 1946.</p>
{pied(g, page)}""")


if __name__ == "__main__":
    sorties = {
        "1-reference": presentation(GAMMES["reference"], "1 / 3"),
        "2-design": presentation(GAMMES["design"], "1 / 3"),
        "3-prestige": presentation(GAMMES["prestige"], "1 / 3"),
        "4-lafuge-page-1": presentation(GAMMES["lafuge"], "1 / 4"),
        "5-lafuge-page-2": histoire(GAMMES["lafuge"], "2 / 4"),
    }
    for nom, contenu in sorties.items():
        (ICI / f"{nom}.html").write_text(contenu, encoding="utf-8")
        print(nom)
