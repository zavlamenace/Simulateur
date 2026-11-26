"""Produit les fichiers dérivés de l'application Apps Script (devis/appscript/).

- Calcul.html : le moteur calcul.js dans une balise <script> (Apps Script n'inclut que des fichiers HTML) ;
- Logos.html : les logos en données intégrées (logo Billards de France en PNG, logo Lafuge en SVG recoloré en noir) ;
- a-copier/ : les 3 seuls fichiers à coller dans l'éditeur Apps Script (Code.gs, Index.html assemblé, appsscript.json).

Usage :
    python3 devis/outils/assembler_appscript.py            # écrit les fichiers
    python3 devis/outils/assembler_appscript.py --verifier # échoue si les fichiers ne sont pas à jour
"""

import base64
import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
APPSCRIPT = RACINE / "appscript"
LOGOS = RACINE / "logos"
ENCRE = "#151515"


def calcul_html() -> str:
    js = (APPSCRIPT / "calcul.js").read_text(encoding="utf-8")
    if "</script" in js:
        raise SystemExit("calcul.js ne doit pas contenir « </script »")
    return "<script>\n" + js + "</script>\n"


def logos_html() -> str:
    png = base64.b64encode((LOGOS / "billards-de-france.png").read_bytes()).decode("ascii")
    svg = (LOGOS / "lafuge.svg").read_text(encoding="utf-8").replace('fill="#fff"', f'fill="{ENCRE}"')
    svg = svg.replace('<path fill="' + ENCRE + '" d="M0 0h140v66H0z">', '<path fill="#fff" d="M0 0h140v66H0z">')
    logos = {
        "bdf": "data:image/png;base64," + png,
        "lafugeSvg": svg,
        "lafuge": "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("ascii"),
    }
    return "<script>\nwindow.LOGOS = " + json.dumps(logos, ensure_ascii=False, indent=2) + ";\n</script>\n"


def index_assemble() -> str:
    """Index.html avec ses inclusions déjà remplies : le seul fichier HTML à coller dans Apps Script."""
    html = (APPSCRIPT / "Index.html").read_text(encoding="utf-8")
    sources = {"Calcul": calcul_html(), "Logos": logos_html()}

    def remplacer(m):
        nom = m.group(1)
        return sources[nom] if nom in sources else (APPSCRIPT / f"{nom}.html").read_text(encoding="utf-8")

    html = re.sub(r"<\?!=\s*include\('([^']+)'\);\s*\?>", remplacer, html)
    if "<?" in html:
        raise SystemExit("Index assemblé : balise « <? » restante")
    return html


def copie(nom):
    return lambda: (APPSCRIPT / nom).read_text(encoding="utf-8")


FICHIERS = {"Calcul.html": calcul_html, "Logos.html": logos_html, "a-copier/Index.html": index_assemble,
            "a-copier/Code.gs": copie("Code.gs"), "a-copier/appsscript.json": copie("appsscript.json")}


def main() -> int:
    verifier = "--verifier" in sys.argv
    perimes = []
    for nom, fabrique in FICHIERS.items():
        attendu = fabrique()
        chemin = APPSCRIPT / nom
        actuel = chemin.read_text(encoding="utf-8") if chemin.exists() else None
        if actuel == attendu:
            continue
        if verifier:
            perimes.append(nom)
        else:
            chemin.parent.mkdir(exist_ok=True)
            chemin.write_text(attendu, encoding="utf-8")
            print("écrit", chemin.relative_to(RACINE.parent))
    if perimes:
        print("Fichiers à régénérer :", ", ".join(perimes))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
