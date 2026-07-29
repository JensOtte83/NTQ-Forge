"""
NTQ Forge — SVG diagram demo.

Generates themed SVG diagrams from Python (the ε↔Δ core symbol in the logo
palette, plus a render-pipeline flow) and places them into figures, then
renders the whole thing as a self-contained NTQ-styled page.

Run from the repository root:

    python examples/diagram_demo.py

then open ``dist/diagram_demo.html`` in a browser.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ntqforge import (  # noqa: E402
    Document, Forge, HTMLRenderer,
    Chapter, Text, Figure,
    relation_diagram, flow_diagram,
)


def build():
    doc = Document(
        title="NTQ-Verse",
        language="de",
        metadata={"subtitle": "SVG Diagram Engine", "accent": "Q"},
    )

    ch1 = Chapter("Das Kernsymbol", number="")
    ch1.add(Text(
        "Das ε↔Δ-Symbol – aus Python generiert, in den Logo-Farben: "
        "violette Glyphen, ein bernsteinfarbener Doppelpfeil."
    ))
    ch1.add(Figure(
        svg=relation_diagram(
            left="ε", right="Δ",
            left_label="Ausgangszustand", right_label="neuer Zustand",
        ),
        caption="ε ↔ Δ — Relation, Analyse und Transformation.",
    ))

    ch2 = Chapter("Render-Pipeline", number="")
    ch2.add(Text("Vom semantischen Objekt zum gerenderten Dokument:"))
    ch2.add(Figure(
        svg=flow_diagram(["Objekt", "Renderer", "HTML"]),
        caption="Die HTML-Render-Pipeline.",
    ))

    doc.add(ch1)
    doc.add(ch2)
    return doc


def main():
    forge = Forge(build(), renderer=HTMLRenderer(embed_fonts=True, lang="de"))
    forge.build("dist/diagram_demo.html")


if __name__ == "__main__":
    main()
