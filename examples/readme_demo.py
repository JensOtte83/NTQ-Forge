"""
NTQ Forge — README demo.

Reads the repository's own README.md and renders it as a self-contained
HTML page in the NTQ design, using the Markdown importer.

Run from the repository root:

    python examples/readme_demo.py

then open ``dist/readme.html`` in a browser.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ntqforge import Forge, HTMLRenderer, from_markdown  # noqa: E402


def main():
    md = (ROOT / "README.md").read_text(encoding="utf-8")

    # First H1 ("NTQ Forge") becomes the title; the rest becomes the body.
    doc = from_markdown(
        md,
        language="en",
        subtitle="rendered by NTQ Forge",
        accent="Q",  # highlight the Q in "NTQ Forge"
    )

    forge = Forge(doc, renderer=HTMLRenderer(embed_fonts=True, lang="en"))
    forge.build("dist/readme.html")


if __name__ == "__main__":
    main()
