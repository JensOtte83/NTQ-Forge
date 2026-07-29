"""
NTQ Forge — NTQ-Verse concept paper demo.

Renders the NTQ-Verse concept paper (papers/ntq_verse_konzeptpapier.md) in
the NTQ design, and replaces the plain "ε ↔ Δ" line under "Das Kernsymbol"
with the generated relation diagram (the ε↔Δ symbol in the logo colours).

Run from the repository root:

    python examples/konzeptpapier_demo.py

then open ``dist/ntq_verse_konzeptpapier.html`` in a browser.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ntqforge import (  # noqa: E402
    Forge, HTMLRenderer, from_markdown, Figure, relation_diagram,
)


def replace_core_symbol(doc):
    """Swap the standalone 'ε ↔ Δ' paragraph for the relation diagram."""
    figure = Figure(
        svg=relation_diagram(
            left="ε", right="Δ",
            left_label="Ausgangszustand", right_label="neuer Zustand",
        ),
        caption="ε ↔ Δ — Relation, Analyse und Transformation.",
        number="",  # keep the concept paper unnumbered
    )

    def walk(container):
        children = getattr(container, "children", None)
        if not isinstance(children, list):
            return False
        for idx, child in enumerate(children):
            text = getattr(child, "text", None)
            if text is not None and str(text).strip() == "ε ↔ Δ":
                children[idx] = figure
                return True
            if walk(child):
                return True
        return False

    walk(doc)
    return doc


def main():
    source = ROOT / "papers" / "ntq_verse_konzeptpapier.md"
    md = source.read_text(encoding="utf-8")

    doc = from_markdown(
        md,
        language="de",
        subtitle="A Unified Ecosystem — Konzeptpapier v0.1",
        accent="Q",
    )
    replace_core_symbol(doc)

    forge = Forge(doc, renderer=HTMLRenderer(embed_fonts=True, lang="de"))
    forge.build("dist/ntq_verse_konzeptpapier.html")


if __name__ == "__main__":
    main()
