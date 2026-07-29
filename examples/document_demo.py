"""
NTQ Forge — document demo.

Builds a small multi-section document from Chapter / Figure / Table
components and renders it, in the NTQ design, to a self-contained HTML
file. Demonstrates automatic numbering (1, 1.1, ... / Abb. 1 / Tab. 1)
and a manual override.

Run from the repository root:

    python examples/document_demo.py

then open ``dist/document_demo.html`` in a browser.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ntqforge import (  # noqa: E402
    Document,
    Forge,
    HTMLRenderer,
    Chapter,
    Figure,
    Table,
    Text,
)


# A tiny inline SVG using the theme accent colours (self-contained).
DIAGRAM = """
<svg viewBox="0 0 320 120" xmlns="http://www.w3.org/2000/svg" width="320">
  <rect x="12"  y="40" width="80" height="40" rx="6"
        fill="none" stroke="#7b6fff" stroke-width="1.5"/>
  <text x="52" y="65" fill="#e8e8f0" font-family="monospace"
        font-size="11" text-anchor="middle">Objekt</text>
  <line x1="92" y1="60" x2="132" y2="60" stroke="#6bffb8" stroke-width="1.5"/>
  <rect x="132" y="40" width="80" height="40" rx="6"
        fill="none" stroke="#6bffb8" stroke-width="1.5"/>
  <text x="172" y="65" fill="#e8e8f0" font-family="monospace"
        font-size="11" text-anchor="middle">Renderer</text>
  <line x1="212" y1="60" x2="252" y2="60" stroke="#ffb86b" stroke-width="1.5"/>
  <rect x="252" y="40" width="60" height="40" rx="6"
        fill="none" stroke="#ffb86b" stroke-width="1.5"/>
  <text x="282" y="65" fill="#e8e8f0" font-family="monospace"
        font-size="11" text-anchor="middle">HTML</text>
</svg>
"""


def build():
    doc = Document(
        title="PRM",
        language="de",
        metadata={
            "subtitle": "Perspektivisches Referenzpunkt Modell",
            "accent": "R",
        },
    )

    # Chapter 1
    ch1 = Chapter("Einführung")
    ch1.add(Text(
        "NTQ Forge erzeugt strukturierte Dokumente aus semantischen "
        "Objekten. Kapitel, Abbildungen und Tabellen werden automatisch "
        "durchnummeriert."
    ))

    # Chapter 1.1 (nested)
    ch11 = Chapter("Architektur")
    ch11.add(Text(
        "Objekte werden von einem Renderer in ein Zielformat überführt — "
        "hier HTML im NTQ-Design."
    ))
    ch11.add(Figure(
        svg=DIAGRAM,
        caption="Vom semantischen Objekt zum gerenderten HTML.",
    ))
    ch1.add(ch11)

    doc.add(ch1)

    # Chapter 2
    ch2 = Chapter("Komponenten")
    ch2.add(Text("Der aktuelle Stand der Bausteine:"))
    ch2.add(Table(
        headers=["Komponente", "Zweck", "Status"],
        rows=[
            ["Chapter", "Nummerierte Abschnitte", "neu"],
            ["Figure", "Abbildung + Caption", "neu"],
            ["Table", "Datentabelle", "neu"],
            ["Panel / FormulaBar / Grid", "Signatur-Layout", "vorhanden"],
        ],
        caption="Komponenten in NTQ Forge.",
    ))

    # Manual override demo: force this figure's number.
    override_fig = Figure(
        svg=DIAGRAM,
        caption="Dieselbe Pipeline, hier mit manuell gesetzter Nummer.",
        number="2b",
    )
    ch2.add(override_fig)

    doc.add(ch2)

    return doc


def main():
    doc = build()
    forge = Forge(doc, renderer=HTMLRenderer(embed_fonts=True))
    forge.build("dist/document_demo.html")


if __name__ == "__main__":
    main()
