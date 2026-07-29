"""
NTQ Forge

Signature components.

These map 1:1 onto the NTQ design system classes defined in
``themes/ntq/*.css``. Building a document from these objects and rendering
it with the :class:`~ntqforge.html_renderer.HTMLRenderer` produces markup
that is styled by the theme — i.e. the PRM/NTQ design, generated from
Python instead of hand-written HTML.

Accent convention
-----------------
Several components accept ``accent`` — one of ``None`` (default violet),
``"success"``, ``"warning"`` or ``"danger"``. These match the modifier
classes in the theme.

Children convention
-------------------
A plain ``str`` child is emitted as raw markup (author-controlled). Use
:class:`Text` for content that must be HTML-escaped.
"""

from .component import Component


_ACCENTS = ("success", "warning", "danger")


def _accent_suffix(accent):
    """Return ``' success'`` etc. for a valid accent, else ``''``."""
    return f" {accent}" if accent in _ACCENTS else ""


class Grid(Component):
    """A responsive grid row.

    ``columns`` is 2 (``.ntq-grid``) or 3 (``.ntq-grid-3``). On narrow
    viewports the theme collapses both to a single column.
    """

    def __init__(self, *children, columns=2):
        super().__init__(*children)
        self.columns = columns

    def render(self, renderer):
        cls = "ntq-grid-3" if self.columns == 3 else "ntq-grid"
        inner = renderer.render_children(self.children)
        return f'<div class="{cls}">\n{inner}\n</div>'


class Panel(Component):
    """A titled panel with the signature accent gradient bar on top.

    ``title`` renders the uppercase ``.ntq-panel-title`` with a status dot;
    pass ``None`` for an untitled panel.
    """

    def __init__(self, *children, title=None, accent=None):
        super().__init__(*children)
        self.title = title
        self.accent = accent

    def render(self, renderer):
        suffix = _accent_suffix(self.accent)
        parts = [f'<div class="ntq-panel{suffix}">']
        if self.title is not None:
            dot = f'<span class="ntq-dot{suffix}"></span>'
            parts.append(
                f'<div class="ntq-panel-title">{dot}'
                f'{self.escape(self.title)}</div>'
            )
        body = renderer.render_children(self.children)
        if body:
            parts.append(body)
        parts.append("</div>")
        return "\n".join(parts)


class FormulaBar(Component):
    """The header formula bar (``E = a . I`` style).

    ``values`` is a list of ``(number, label)`` pairs shown right-aligned.
    """

    def __init__(self, equation, label="Kernformel", expand=None, values=None):
        super().__init__()
        self.equation = equation
        self.label = label
        self.expand = expand
        self.values = list(values or [])

    def render(self, renderer):
        parts = [
            '<div class="ntq-formula">',
            f'<div class="ntq-formula-label">{self.escape(self.label)}</div>',
            f'<div class="ntq-formula-eq">{self.escape(self.equation)}</div>',
        ]
        if self.expand:
            parts.append(
                f'<div class="ntq-formula-expand">{self.escape(self.expand)}</div>'
            )
        if self.values:
            vals = ['<div class="ntq-formula-values">']
            for num, label in self.values:
                vals.append(
                    '<div class="ntq-fval">'
                    f'<div class="ntq-fval-num">{self.escape(num)}</div>'
                    f'<div class="ntq-fval-label">{self.escape(label)}</div>'
                    "</div>"
                )
            vals.append("</div>")
            parts.append("".join(vals))
        parts.append("</div>")
        return "\n".join(parts)


class Heading(Component):
    """A serif section heading (``.ntq-heading``)."""

    def __init__(self, text, level=2):
        super().__init__()
        self.text = text
        self.level = max(1, min(6, int(level)))

    def render(self, renderer):
        tag = f"h{self.level}"
        return f'<{tag} class="ntq-heading">{self.escape(self.text)}</{tag}>'


class Text(Component):
    """A paragraph of escaped text (``.ntq-text``)."""

    def __init__(self, text):
        super().__init__()
        self.text = text

    def render(self, renderer):
        return f'<p class="ntq-text">{self.escape(self.text)}</p>'


class Badge(Component):
    """A small uppercase badge (``.ntq-badge``)."""

    def __init__(self, text, accent=None):
        super().__init__()
        self.text = text
        self.accent = accent

    def render(self, renderer):
        suffix = _accent_suffix(self.accent)
        return f'<span class="ntq-badge{suffix}">{self.escape(self.text)}</span>'


class Log(Component):
    """A monospace log block (``.ntq-log``).

    ``entries`` is a list of either strings or ``(text, kind)`` tuples,
    where ``kind`` is one of ``"success"``, ``"warning"``, ``"error"``,
    ``"info"``.
    """

    _KINDS = ("success", "warning", "error", "info")

    def __init__(self, entries=None):
        super().__init__()
        self.entries = list(entries or [])

    def render(self, renderer):
        rows = ['<div class="ntq-log">']
        for entry in self.entries:
            if isinstance(entry, (tuple, list)):
                text, kind = entry[0], (entry[1] if len(entry) > 1 else None)
            else:
                text, kind = entry, None
            suffix = f" {kind}" if kind in self._KINDS else ""
            rows.append(
                f'<div class="ntq-log-entry{suffix}">{self.escape(text)}</div>'
            )
        rows.append("</div>")
        return "\n".join(rows)


class Raw(Component):
    """Raw, unescaped markup passthrough. Use sparingly."""

    def __init__(self, markup):
        super().__init__()
        self.markup = markup

    def render(self, renderer):
        return str(self.markup)


# =====================================================================
# Structured document components (with automatic numbering)
# =====================================================================


class _Numbered(Component):
    """Mixin base for components that carry an automatic, overridable number.

    ``number`` is the manual override (``None`` = automatic). The numbering
    pass fills ``_computed_number``; ``display_number`` returns whichever
    applies. Set ``.number`` after building the document to override.
    """

    def __init__(self, *children, number=None):
        super().__init__(*children)
        self.number = number
        self._computed_number = None

    @property
    def display_number(self):
        return self.number if self.number is not None else self._computed_number


class Chapter(_Numbered):
    """A titled, hierarchically numbered section (1, 1.1, 1.1.1 ...).

    Chapters may contain any components, including nested chapters. The
    numbering pass sets ``level`` (nesting depth) which drives the heading
    size. Pass ``number=`` to override the label.
    """

    def __init__(self, title, *children, number=None):
        super().__init__(*children, number=number)
        self.title = title
        self.level = 1  # set by the numbering pass

    def render(self, renderer):
        num = self.display_number
        num_html = (
            f'<span class="ntq-num">{self.escape(num)}</span>' if num else ""
        )
        level = max(1, min(6, self.level))
        tag = f"h{level}"
        title = (
            f'<{tag} class="ntq-chapter-title level-{level}">'
            f"{num_html}{self.escape(self.title)}</{tag}>"
        )
        body = renderer.render_children(self.children)
        parts = ['<section class="ntq-chapter">', title]
        if body:
            parts.append(body)
        parts.append("</section>")
        return "\n".join(parts)


class Figure(_Numbered):
    """A figure with a caption and an automatic "Abb. N" label.

    Provide either ``src`` (image URL/path) or ``svg`` (inline SVG markup).
    ``label`` is the caption prefix (default "Abb."). Pass ``number=`` to
    override the figure number.
    """

    def __init__(self, src=None, caption=None, alt=None, svg=None,
                 label="Abb.", number=None):
        super().__init__(number=number)
        self.src = src
        self.svg = svg
        self.caption = caption
        self.alt = alt or ""
        self.label = label

    def render(self, renderer):
        if self.svg:
            media = str(self.svg)
        elif self.src:
            media = (
                f'<img class="ntq-figure-img" src="{self.escape(self.src)}" '
                f'alt="{self.escape(self.alt)}">'
            )
        else:
            media = ""

        caption_html = ""
        if self.caption is not None:
            num = self.display_number
            num_html = (
                f'<span class="ntq-num">{self.escape(self.label)} '
                f"{self.escape(num)}</span>" if num else ""
            )
            caption_html = (
                f'<figcaption class="ntq-figcaption">'
                f"{num_html}{self.escape(self.caption)}</figcaption>"
            )

        parts = ['<figure class="ntq-figure">']
        if media:
            parts.append(media)
        if caption_html:
            parts.append(caption_html)
        parts.append("</figure>")
        return "\n".join(parts)


class Table(_Numbered):
    """A data table with an automatic "Tab. N" caption.

    ``headers`` is a list of column titles; ``rows`` is a list of rows, each
    a list of cell values. ``caption`` and ``label`` (default "Tab.") drive
    the caption line. Pass ``number=`` to override the table number.
    """

    def __init__(self, headers=None, rows=None, caption=None,
                 label="Tab.", number=None):
        super().__init__(number=number)
        self.headers = list(headers or [])
        self.rows = [list(r) for r in (rows or [])]
        self.caption = caption
        self.label = label

    def render(self, renderer):
        parts = ['<table class="ntq-table">']

        if self.caption is not None:
            num = self.display_number
            num_html = (
                f'<span class="ntq-num">{self.escape(self.label)} '
                f"{self.escape(num)}</span>" if num else ""
            )
            parts.append(f"<caption>{num_html}{self.escape(self.caption)}</caption>")

        if self.headers:
            head_cells = "".join(
                f"<th>{self.escape(h)}</th>" for h in self.headers
            )
            parts.append(f"<thead><tr>{head_cells}</tr></thead>")

        if self.rows:
            body_rows = []
            for row in self.rows:
                cells = "".join(f"<td>{self.escape(c)}</td>" for c in row)
                body_rows.append(f"<tr>{cells}</tr>")
            parts.append("<tbody>" + "".join(body_rows) + "</tbody>")

        parts.append("</table>")
        return f'<div class="ntq-table-wrap">\n{"".join(parts)}\n</div>'
