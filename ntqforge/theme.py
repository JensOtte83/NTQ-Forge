"""
NTQ Forge

Theme.

The Theme owns the NTQ design system living in ``themes/ntq/``. It knows
the CSS files, in the correct cascade order, and can produce a single
inlined stylesheet for embedding into a rendered document.

This is what makes the design "global": the same tokens, fonts and
component styles that originate in the Android PRM tool are read from the
theme directory and emitted into any document NTQ Forge renders.

Token constants (``ACCENT``, ``BG`` ...) mirror ``variables.css`` so the
values are also available programmatically (e.g. for an SVG renderer).
"""

import base64
import re

from .utils import project_root


# -- token mirror (kept in sync with themes/ntq/variables.css) -----------

BG = "#0a0a0f"
SURFACE = "#111118"
SURFACE_2 = "#1a1a24"
BORDER = "#2a2a3a"
ACCENT = "#7b6fff"
ACCENT_2 = "#ff6b6b"
ACCENT_3 = "#6bffb8"
ACCENT_4 = "#ffb86b"
TEXT = "#e8e8f0"
TEXT_DIM = "#7a7a9a"

FONT_MONO = "DM Mono"
FONT_SERIF = "Cormorant Garamond"


# -- font url() rewriting ------------------------------------------------

_FONT_URL_RE = re.compile(r"""url\(\s*["']?([^"')]+\.ttf)["']?\s*\)""")

_MIME = {
    "ttf": "font/ttf",
    "otf": "font/otf",
    "woff": "font/woff",
    "woff2": "font/woff2",
}


class Theme:
    """The NTQ design system, loaded from ``themes/ntq/``."""

    #: CSS files in cascade order. ``theme-dark`` is the default palette;
    #: ``theme-light`` is scoped to ``body.theme-light`` and harmless here.
    CSS_ORDER = (
        "variables.css",
        "fonts.css",
        "base.css",
        "layout.css",
        "components.css",
        "animations.css",
        "theme-dark.css",
        "theme-light.css",
    )

    def __init__(self, name="ntq", root=None):
        self.name = name
        base = project_root() if root is None else root
        self.path = base / "themes" / name

    # -- discovery ----------------------------------------------------

    def css_paths(self):
        """Yield existing CSS file paths, in cascade order."""
        for filename in self.CSS_ORDER:
            candidate = self.path / filename
            if candidate.exists():
                yield candidate

    # -- css assembly -------------------------------------------------

    def inline_css(self, embed_fonts=True):
        """Return the whole theme as one CSS string.

        If ``embed_fonts`` is True, ``url(...ttf)`` references are replaced
        with self-contained ``data:`` URIs, so the output document renders
        identically anywhere with no external files.
        """
        blocks = []
        for path in self.css_paths():
            css = path.read_text(encoding="utf-8")
            if embed_fonts and path.name == "fonts.css":
                css = self._embed_font_urls(css, path.parent)
            blocks.append(f"/* --- {path.name} --- */\n{css}")
        return "\n\n".join(blocks)

    def _embed_font_urls(self, css, css_dir):
        """Replace relative ttf ``url()`` refs with base64 data URIs."""

        def repl(match):
            rel = match.group(1)
            font_path = (css_dir / rel).resolve()
            if not font_path.exists():
                return match.group(0)  # leave as-is if missing
            ext = font_path.suffix.lstrip(".").lower()
            mime = _MIME.get(ext, "application/octet-stream")
            data = base64.b64encode(font_path.read_bytes()).decode("ascii")
            return f'url("data:{mime};base64,{data}")'

        return _FONT_URL_RE.sub(repl, css)
