"""Maquettes de la présentation en tête du PDF (27/11) : une page par gamme, deux pour Lafuge.

Variante A : le billard en mode billard et en mode table, côte à côte.
Variante B : une grande photo et une vignette.
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
:root{--noir:#151515;--gris:#3d4248;--doux:#767b80;--sable:#f6f3ee;--lin:#efe9e3;--r:6px}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{width:794px;height:1123px;padding:40px 48px 26px;font:400 11px/1.5 'DM Sans',sans-serif;color:var(--noir);
  display:flex;flex-direction:column}
header{display:flex;justify-content:space-between;align-items:center}
header img{height:30px;display:block}
header img.laf{height:44px}
.ref{text-align:right;font-size:9.5px;color:var(--doux);line-height:1.55}
.ref b{color:var(--noir);font-weight:500}
.cap{font-size:8.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--doux)}
.titre{margin-top:30px}
.titre.duo{display:grid;grid-template-columns:1fr 190px;gap:28px;align-items:end;margin-top:22px}
h1{font:400 60px/1 'EB Garamond',serif;margin-top:6px;letter-spacing:-.01em}
.type{font-size:12.5px;color:var(--gris);margin-top:8px}
.fiche{display:grid;grid-auto-flow:column;grid-auto-columns:1fr;margin-top:18px;border-top:1px solid var(--lin)}
.fiche div{padding:9px 10px 0 0}
.fiche div + div{padding-left:12px;border-left:1px solid var(--lin)}
.fiche b{display:block;font-weight:500;font-size:11px;margin-top:3px}
figure{margin:0}
figure img{display:block;width:100%;object-fit:cover;border-radius:var(--r)}
figcaption{margin-top:6px}
.vide{display:flex;align-items:center;justify-content:center;background:var(--lin);border-radius:var(--r);
  color:var(--doux);font-size:9.5px;text-align:center;padding:10px}
.photos{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:20px}
.photos img,.photos .vide{aspect-ratio:1.22}
.grande{margin-top:18px}
.grande img{aspect-ratio:2.05}
.vignette img,.vignette .vide{aspect-ratio:4/3}
.mention{font-size:8.5px;font-style:italic;color:var(--doux);margin-top:7px}
.accroche{display:grid;grid-template-columns:150px 1fr;gap:20px;margin-top:24px;align-items:baseline}
.accroche p{font:400 22px/1.25 'EB Garamond',serif}
.forts{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:18px}
.forts img,.forts .vide,.forts .typo{aspect-ratio:1.55;border-radius:var(--r);width:100%}
.forts img{display:block;object-fit:cover}
.forts .typo{display:flex;flex-direction:column;justify-content:center;align-items:center;background:var(--sable);
  font:400 14px/1.5 'EB Garamond',serif;text-align:center}
.num{font:400 13px 'EB Garamond',serif;color:var(--doux);margin-top:10px}
.forts h3{font-size:11.5px;font-weight:500;line-height:1.35;margin-top:2px}
.forts p{font-size:10px;color:var(--gris);margin-top:3px;line-height:1.45}
.reass{display:flex;margin-top:auto;border-top:1px solid var(--lin);padding-top:14px}
.reass div{flex:1;display:flex;gap:9px;align-items:flex-start;padding:0 10px}
.reass div:first-child{padding-left:0}
.reass div + div{border-left:1px solid var(--lin)}
.reass img{width:22px;height:22px;flex:none;margin-top:1px}
.reass b{display:block;font-weight:500;font-size:10px;line-height:1.3}
.reass span{display:block;font-size:9px;color:var(--doux);line-height:1.3;margin-top:1px}
footer{display:flex;justify-content:space-between;font-size:8.5px;color:var(--doux);margin-top:14px}
/* Page histoire Lafuge */
.bandeau{margin-top:26px}
.bandeau img{aspect-ratio:1.75;object-position:center 62%}
h2{font:400 40px/1.1 'EB Garamond',serif;margin-top:26px}
.intro{font:400 16px/1.45 'EB Garamond',serif;color:var(--gris);margin-top:10px;max-width:560px}
.temps{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:24px;border-top:1px solid var(--lin);padding-top:14px}
.temps h3{font:400 17px 'EB Garamond',serif}
.temps p{font-size:10.5px;color:var(--gris);margin-top:5px;line-height:1.55}
.trio{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:24px}
.trio img{aspect-ratio:1.05}
.signature{font:italic 13px/1.5 'EB Garamond',serif;color:var(--gris);margin-top:auto;padding-top:18px}
"""


def tete(g):
    logo = '<img class="laf" src="img/logo-lafuge.svg">' if g.get("lafuge") else '<img src="img/logo-bdf.png">'
    return (f'<header>{logo}<div class="ref"><b>Devis n° 2026-0142</b><br>'
            f'M. et Mme Martin · 27 novembre 2026</div></header>')


def pied(g, page):
    gauche = ("Billard Lafuge, maison du groupe Billards de France · billard-lafuge.fr" if g.get("lafuge")
              else "Billards de France · billardsdefrance.fr · 05 62 69 30 20")
    return f'<footer><span>{gauche}</span><span>{page}</span></footer>'


def image(src, cls=""):
    if src.startswith("vide:"):
        return f'<div class="vide {cls}">{src[5:]}</div>'
    return f'<img class="{cls}" src="img/{src}">'


def fiche(g):
    return '<div class="fiche">' + "".join(
        f'<div><span class="cap">{k}</span><b>{v}</b></div>' for k, v in g["fiche"]) + "</div>"


def bloc_titre(g, vignette=None):
    t = (f'<div><p class="cap">Votre billard</p><h1>{g["modele"]}</h1>'
         f'<p class="type">{g["type"]}</p></div>')
    if vignette:
        v = (f'<figure class="vignette">{image(vignette[0])}'
             f'<figcaption class="cap">{vignette[1]}</figcaption></figure>')
        return f'<section class="titre duo">{t}{v}</section>{fiche(g)}'
    return f'<section class="titre">{t}</section>{fiche(g)}'


def photos(g, variante):
    if variante == "A":
        return ('<section class="photos">'
                f'<figure>{image(g["billard"])}<figcaption class="cap">En billard</figcaption></figure>'
                f'<figure>{image(g["table"])}<figcaption class="cap">{g.get("legende_table", "En table")}</figcaption></figure>'
                f'</section><p class="mention">{MENTION}</p>')
    return f'<figure class="grande">{image(g["billard"])}</figure><p class="mention">{MENTION}</p>'


def forts(g):
    cases = []
    for i, p in enumerate(g["forts"], start=1):
        visuel = (f'<div class="typo">{p["typo"]}</div>' if "typo" in p else image(p["img"]))
        cases.append(f'<div>{visuel}<p class="num">0{i}</p><h3>{p["titre"]}</h3><p>{p["texte"]}</p></div>')
    return f'<section class="forts">{"".join(cases)}</section>'


def reass(g):
    return '<section class="reass">' + "".join(
        f'<div><img src="img/{i}.svg"><p><b>{a}</b><span>{b}</span></p></div>' for i, a, b in g["reass"]) + "</section>"


def page_presentation(g, variante, numero):
    vign = (g["table"], g.get("legende_table", "En table")) if variante == "B" else None
    corps = (tete(g) + bloc_titre(g, vign) + photos(g, variante)
             + f'<section class="accroche"><span class="cap">{g.get("label_accroche", "Pourquoi ce billard")}</span>'
               f'<p>{g["accroche"]}</p></section>'
             + forts(g) + reass(g) + pied(g, numero))
    return html(corps)


def html(corps):
    return f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{corps}</body></html>'


FAMILLE = ("wood", "3e génération", "d'ébénistes depuis 1946")
INVENTEUR = ("sliders", "Inventeur du convertible", "depuis 1985")
LIVRAISON = ("truck", "Livraison offerte", "partout en France")
MAIN_GERS = ("hands", "Fait à la main", "à Plaisance-du-Gers")
SECURISE = ("lock", "Paiement sécurisé", "carte, PayPal, Wero")
ONEY = ("lock", "Paiement en 3x ou 4x", "sans frais avec Oney")
A_VENIR = "vide:Photo à venir"

GAMMES = {
    "reference": dict(
        modele="Caracas", type="Billard convertible en table · Référence Premium",
        fiche=[("Taille", "2,10 m"), ("Jeu", "Américain"), ("Tapis", "Bleu royal"), ("Pieds", "Bois massif"),
               ("Plateau", "Bois, 2 parties")],
        billard="ref-billard.jpg", table="ref-table.jpg",
        accroche="Le meilleur rapport qualité-prix du marché en 2,10 m, la taille standard du billard.",
        forts=[dict(img=A_VENIR, titre="Ardoise monobloc de 19 mm",
                    texte="Une pierre naturelle d'un seul tenant : elle ne gonfle pas et ne se déforme pas avec "
                          "l'humidité, contrairement au MDF ou à l'aggloméré."),
               dict(img="ref-pack.jpg", titre="Pack accessoires inclus, d'une valeur de 300 €",
                    texte="16 billes, 4 queues, triangle, craies, brosse et porte-queue."),
               dict(img="ref-pieds.jpg", titre="Pieds bois massif et Formica",
                    texte="Le matériau des plans de travail de cuisine : il résiste aux chocs, aux rayures et aux "
                          "taches.")],
        reass=[INVENTEUR, FAMILLE, LIVRAISON, ONEY],
    ),
    "design": dict(
        modele="Boston", type="Billard convertible en table · Design",
        fiche=[("Taille", "2,10 m"), ("Jeu", "Américain"), ("Laque", "Gris clair, mat"),
               ("Tapis", "Simonis 760, Bleu"), ("Plateau", "Bois laqué")],
        billard="design-billard.jpg", table="design-table.jpg",
        accroche="Le billard convertible en table, laqué et fabriqué à la main dans notre atelier du Gers.",
        forts=[dict(img="design-drap.jpg", titre="Drap Simonis 760 ou Strachan 777 inclus",
                    texte="Les draps des grandes compétitions internationales, en 26 couleurs, sans supplément."),
               dict(img=A_VENIR, titre="Ardoise italienne monobloc de 19 mm",
                    texte="Une pierre naturelle d'un seul tenant : elle ne se déforme pas avec l'humidité."),
               dict(img=A_VENIR, titre="Bandes interchangeables brevetées",
                    texte="Plusieurs jeux sur un même billard : français, américain ou pool, à vous de choisir.")],
        reass=[MAIN_GERS, FAMILLE, INVENTEUR, LIVRAISON, SECURISE],
    ),
    "prestige": dict(
        modele="Paris", type="Billard convertible en table · Prestige",
        fiche=[("Taille", "2,10 m"), ("Jeu", "Américain"), ("Finition", "Cuir et chêne"),
               ("Tapis", "Simonis 760, Bleu"), ("Plateau", "Bois, allonge incluse")],
        billard="prest-billard.jpg", table="vide:Photo en mode table à venir",
        accroche="Le billard convertible en table le plus fonctionnel du marché, allonge incluse pour 12 convives.",
        forts=[dict(img=A_VENIR, titre="Bandes interchangeables brevetées",
                    texte="Plusieurs jeux sur un même billard : vous passez d'un jeu à l'autre en changeant de bandes."),
               dict(img=A_VENIR, titre="Rangement intégré de tous les accessoires",
                    texte="Le système Octopack range sous le billard les queues, les billes, les bandes, les craies "
                          "et les plateaux."),
               dict(img="prest-reception.jpg", titre="Réception centralisée et insonorisée",
                    texte="Goulottes capitonnées en 3 épaisseurs, un tiroir abattant de chaque côté.")],
        reass=[MAIN_GERS, FAMILLE, INVENTEUR, LIVRAISON, SECURISE],
    ),
    "lafuge": dict(
        lafuge=True, modele="Chambord", type="Billard mixte · Billard Lafuge",
        fiche=[("Taille", "2,60 m"), ("Jeu", "Américain"), ("Bois", "Chêne massif français"),
               ("Finition", "Brossée blanchie"), ("Drap", "Simonis 760, Rose")],
        billard="laf-billard.jpg", table="laf-detail2.jpg", legende_table="Détail du pied",
        label_accroche="Notre signature",
        accroche="Le billard le plus personnalisable : essence, teinte, taille, finitions et liserés sont à votre choix.",
        forts=[dict(img="laf-mains.jpg", titre="Une pièce unique, faite à la main",
                    texte="Fabriquée à l'unité par un seul ébéniste, du début à la fin."),
               dict(img="laf-planches.jpg", titre="Essences nobles massives",
                    texte="Chêne, érable et noyer massifs français, ou mélèze massif."),
               dict(typo="Yacht Club de Monaco<br>Sheraton Paris<br>Villas de la Côte d'Azur<br>et de la côte atlantique",
                    titre="Ils nous ont choisis", texte="Des lieux d'exception, en France et à Monaco.")],
        reass=[("hands", "Fabrication artisanale", "en Chartreuse"), FAMILLE,
               ("sliders", "Sur mesure", "chaque détail à votre choix"),
               ("truck", "Livré et installé", "par nos équipes"), SECURISE],
    ),
}

HISTOIRE = """
<figure class="bandeau">{img}</figure>
<h2>De l'arbre au billard</h2>
<p class="intro">Chaque billard Lafuge est fabriqué à l'unité dans notre atelier de Miribel-les-Échelles, au cœur du
parc naturel régional de Chartreuse.</p>
<section class="temps">
<div><h3>Le bois</h3><p>Le travail commence par le bois brut. Chêne, érable et noyer français, ou mélèze, sont
choisis pour leur veinage et travaillés en massif.</p></div>
<div><h3>La main</h3><p>Un seul ébéniste conduit votre billard du début à la fin : assemblage, ajustage, ponçage,
finition. La laque est appliquée dans une cabine dédiée.</p></div>
<div><h3>Le temps</h3><p>Huit semaines de fabrication au minimum. Le billard est ensuite livré, installé et réglé
chez vous par nos équipes.</p></div>
</section>
<section class="trio">
<figure><img src="img/laf-atelier.jpg"><figcaption class="cap">L'atelier</figcaption></figure>
<figure><img src="img/laf-laque.jpg"><figcaption class="cap">La cabine de laque</figcaption></figure>
<figure><img src="img/laf-drap.jpg"><figcaption class="cap">La pose du drap</figcaption></figure>
</section>
<p class="signature">Billard Lafuge, maison du groupe Billards de France. La famille Fitan travaille le bois depuis 1946.</p>
"""

if __name__ == "__main__":
    sorties = {
        "reference-A": page_presentation(GAMMES["reference"], "A", "1 / 3"),
        "reference-B": page_presentation(GAMMES["reference"], "B", "1 / 3"),
        "design-A": page_presentation(GAMMES["design"], "A", "1 / 3"),
        "prestige-B": page_presentation(GAMMES["prestige"], "B", "1 / 3"),
        "lafuge-1": page_presentation(GAMMES["lafuge"], "B", "1 / 4"),
        "lafuge-2": html(tete(GAMMES["lafuge"]) + HISTOIRE.format(img='<img src="img/laf-planches-haut.jpg">')
                         + pied(GAMMES["lafuge"], "2 / 4")),
    }
    for nom, contenu in sorties.items():
        (ICI / f"{nom}.html").write_text(contenu, encoding="utf-8")
        print(nom)
