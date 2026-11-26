"""Produit les fichiers dérivés de l'application Apps Script (devis/appscript/).

- Calcul.html : le moteur calcul.js dans une balise <script> (Apps Script n'inclut que des fichiers HTML) ;
- Logos.html : les logos en données intégrées (logo Billards de France en PNG, logo Lafuge en SVG recoloré en noir) ;
- a-copier/ : les 8 fichiers à coller dans l'éditeur Apps Script, réunis au même endroit.

Usage :
    python3 devis/outils/assembler_appscript.py            # écrit les fichiers
    python3 devis/outils/assembler_appscript.py --verifier # échoue si les fichiers ne sont pas à jour
"""

import base64
import json
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


def copie(nom):
    return lambda: (APPSCRIPT / nom).read_text(encoding="utf-8")


DEPLOIEMENT = ["Code.gs", "Index.html", "Styles.html", "Calcul.html", "Logos.html", "Pdf.html", "App.html", "appsscript.json"]
FICHIERS = {"Calcul.html": calcul_html, "Logos.html": logos_html}
FICHIERS.update({f"a-copier/{n}": (calcul_html if n == "Calcul.html" else logos_html if n == "Logos.html" else copie(n))
                 for n in DEPLOIEMENT})


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
