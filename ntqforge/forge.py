"""
NTQ Forge

Forge — high-level facade.

    forge = Forge(document)
    html = forge.render()          # -> HTML string
    forge.build("dist/index.html") # -> writes the file, returns the path
"""

from pathlib import Path

from .document import Document
from .html_renderer import HTMLRenderer


class Forge:

    def __init__(self, document=None, renderer=None):
        self.document = document if document is not None else Document()
        self.renderer = renderer if renderer is not None else HTMLRenderer()

    def render(self):
        """Return the rendered document as a string."""
        return self.renderer.render(self.document)

    def build(self, output="dist/index.html"):
        """Render and write the document to ``output``. Returns the Path."""
        html = self.render()
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")
        print(f"NTQ Forge: wrote {path} ({len(html):,} bytes)")
        return path
