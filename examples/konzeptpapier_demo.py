"""
NTQ Forge — NTQ-Verse concept paper demo.

Renders the NTQ-Verse concept paper (papers/ntq_verse_konzeptpapier.md) as
a self-contained HTML document in the NTQ design.

Run from the repository root:

    python examples/konzeptpapier_demo.py

then open ``dist/ntq_verse_konzeptpapier.html`` in a browser.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ntqforge import Forge, HTMLRenderer, from_markdown  # noqa: E402


def main():
    source = ROOT / "papers" / "ntq_verse_konzeptpapier.md"
    md = source.read_text(encoding="utf-8")

    # First H1 ("NTQ-Verse") becomes the document title.
    doc = from_markdown(
        md,
        language="de",
        subtitle="A Unified Ecosystem — Konzeptpapier v0.1",
        accent="Q",  # highlight the Q in "NTQ-Verse"
    )

    forge = Forge(doc, renderer=HTMLRenderer(embed_fonts=True, lang="de"))
    forge.build("dist/ntq_verse_konzeptpapier.html")


if __name__ == "__main__":
    main()
