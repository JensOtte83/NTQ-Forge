"""
NTQ Forge

HTML renderer.

Turns a Document into a complete, standalone HTML5 page wearing the NTQ
theme: the design tokens, fonts, background grid and component styles are
all embedded, so the output renders identically wherever it is opened.

    Document(title=..., metadata={"subtitle": ...})
        -> <div class="ntq-app">
             <header class="ntq-header"> logo + subtitle </header>
             ...children...
           </div>

The header is emitted only when the document has a title. ``metadata``
keys used: ``subtitle`` (header sub-line), ``accent`` (a character in the
title to highlight, PRM-style, e.g. "R" in "PRM").
"""

from .renderer import Renderer
from .theme import Theme
from .numbering import assign_numbers


class HTMLRenderer(Renderer):
    """Render a Document to a full themed HTML page."""

    def __init__(self, theme=None, embed_fonts=True, lang="de"):
        self.theme = theme if theme is not None else Theme()
        self.embed_fonts = embed_fonts
        self.lang = lang

    # -- public -------------------------------------------------------

    def render(self, document):
        # Assign automatic numbers (chapters, figures, tables) before render.
        assign_numbers(document)
        lang = getattr(document, "language", None) or self.lang
        css = self.theme.inline_css(embed_fonts=self.embed_fonts)
        title = getattr(document, "title", "") or ""

        head = (
            "<head>\n"
            '<meta charset="UTF-8">\n'
            '<meta name="viewport" '
            'content="width=device-width, initial-scale=1.0">\n'
            f"<title>{self.escape(title)}</title>\n"
            f"<style>\n{css}\n</style>\n"
            "</head>"
        )

        body_parts = ['<div class="ntq-app">']
        header = self._render_header(document)
        if header:
            body_parts.append(header)
        body_parts.append(self.render_children(document))
        body_parts.append("</div>")
        body = "<body>\n" + "\n".join(body_parts) + "\n</body>"

        return (
            "<!DOCTYPE html>\n"
            f'<html lang="{self.escape(lang)}">\n'
            f"{head}\n{body}\n</html>\n"
        )

    # -- helpers ------------------------------------------------------

    def _render_header(self, document):
        title = getattr(document, "title", "") or ""
        if not title:
            return ""
        metadata = getattr(document, "metadata", {}) or {}
        subtitle = metadata.get("subtitle", "")
        accent_char = metadata.get("accent")

        logo = self._logo_markup(title, accent_char)
        left = [f'<div class="ntq-logo">{logo}</div>']
        if subtitle:
            left.append(f'<div class="ntq-subtitle">{self.escape(subtitle)}</div>')

        return (
            '<header class="ntq-header">\n'
            '<div class="ntq-header-left">\n' + "\n".join(left) + "\n</div>\n"
            '<div class="ntq-header-right">'
            '<div class="ntq-badge">NTQ Forge</div>'
            "</div>\n"
            "</header>"
        )

    def _logo_markup(self, title, accent_char):
        """Escape the title, optionally wrapping one char in <span>."""
        if accent_char and accent_char in title:
            idx = title.index(accent_char)
            before = self.escape(title[:idx])
            hit = self.escape(title[idx])
            after = self.escape(title[idx + 1 :])
            return f"{before}<span>{hit}</span>{after}"
        return self.escape(title)

    @staticmethod
    def escape(text):
        from html import escape as _escape

        return _escape(str(text), quote=True)
