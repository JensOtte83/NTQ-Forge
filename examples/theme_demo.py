"""
NTQ Forge — theme demo.

Builds a small PRM-style document from semantic components and renders it
to a standalone, self-contained HTML file wearing the NTQ theme.

Run from the repository root:

    python examples/theme_demo.py

then open ``dist/theme_demo.html`` in a browser.
"""

import sys
from pathlib import Path

# Make the repo root importable when run as a plain script.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ntqforge import (  # noqa: E402
    Document,
    Forge,
    HTMLRenderer,
    FormulaBar,
    Grid,
    Panel,
    Heading,
    Text,
    Log,
    Badge,
)


def build():
    doc = Document(
        title="PRM",
        metadata={
            "subtitle": "Perspektivisches Referenzpunkt Modell",
            "accent": "R",
        },
    )

    doc.add(
        FormulaBar(
            equation="E = a . I",
            label="Kernformel",
            expand="mit a = kT . ln(2)  |  in Omega: E ~ I",
            values=[("3", "Delta aktiv"), ("1.42", "I(Delta) gesamt"), ("0.98", "E rel. [kT]")],
        )
    )

    doc.add(
        Grid(
            Panel(
                Heading("Delta-Editor"),
                Text(
                    "Dokumente entstehen aus semantischen Objekten — Kapitel, "
                    "Figuren, Tabellen, Diagramme — statt aus handgeschriebenem "
                    "HTML."
                ),
                Badge("Bootstrap", accent="warning"),
                title="Delta . Editor",
            ),
            Panel(
                Heading("Action Log"),
                Log(
                    entries=[
                        ("System bereit — Theme geladen", "success"),
                        ("3 Unterscheidungen registriert", "info"),
                        ("Boundary-Drift: keine", "success"),
                    ]
                ),
                title="Action Log . Root",
                accent="success",
            ),
            columns=2,
        )
    )

    return doc


def main():
    doc = build()
    forge = Forge(doc, renderer=HTMLRenderer(embed_fonts=True))
    forge.build("dist/theme_demo.html")


if __name__ == "__main__":
    main()
