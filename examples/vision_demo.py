"""
NTQ Forge — NTQ ↔ Vision concept paper demo.

Renders papers/ntq_vision_konzeptpapier.md in the NTQ design and replaces
the textual reconstruction chain (Input ↓ … ↓ Output) under "Rekonstruktiver
Ablauf" with a generated vertical flow diagram.

Run from the repository root:

    python examples/vision_demo.py

then open ``dist/ntq_vision_konzeptpapier.html`` in a browser.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ntqforge import (  # noqa: E402
    Forge, HTMLRenderer, from_markdown, Figure, flow_diagram,
)


def replace_pipeline(doc):
    """Swap the 'Input ↓ … ↓ Output' paragraph for a vertical flow diagram."""

    def parse_steps(text):
        # text is inline HTML with <br> between lines and '↓' separators
        raw = text.replace("<br>", "\n")
        steps = []
        for part in raw.split("↓"):
            label = part.replace("\n", " ").strip()
            if label:
                steps.append(label)
        return steps

    def walk(container):
        children = getattr(container, "children", None)
        if not isinstance(children, list):
            return False
        for idx, child in enumerate(children):
            text = getattr(child, "text", None)
            if text is not None and "↓" in str(text) \
                    and str(text).strip().startswith("Input"):
                steps = parse_steps(str(text))
                children[idx] = Figure(
                    svg=flow_diagram(steps, width=420, direction="vertical"),
                    caption="Rekonstruktiver Ablauf: Input → Output.",
                    number="",
                )
                return True
            if walk(child):
                return True
        return False

    walk(doc)
    return doc


def main():
    source = ROOT / "papers" / "ntq_vision_konzeptpapier.md"
    md = source.read_text(encoding="utf-8")

    doc = from_markdown(
        md,
        language="de",
        subtitle="Konzeptpapier · visuelle Perspektive im PRM",
        accent="↔",
    )
    replace_pipeline(doc)

    forge = Forge(doc, renderer=HTMLRenderer(embed_fonts=True, lang="de"))
    forge.build("dist/ntq_vision_konzeptpapier.html")


if __name__ == "__main__":
    main()
