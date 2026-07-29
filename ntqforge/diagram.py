"""
NTQ Forge

SVG diagram engine.

A small, dependency-free builder for producing themed SVG diagrams from
Python. The output is an ``<svg>`` string that drops straight into a
:class:`~ntqforge.components.Figure`::

    from ntqforge import Figure, relation_diagram
    fig = Figure(svg=relation_diagram(), caption="Das Kernsymbol")

Colours come from the NTQ theme. The signature ``relation_diagram`` uses
the ε↔Δ logo palette: violet glyphs, an amber double arrow.

The low-level :class:`Diagram` exposes primitives (``rect``, ``line``,
``arrow``, ``text``, ``circle``); the module-level builders compose them
into ready-made diagrams.
"""

from html import escape as _escape

from .theme import (
    ACCENT, ACCENT_2, ACCENT_3, ACCENT_4,
    TEXT, TEXT_DIM, SURFACE_2, BORDER,
)

_SERIF = "Cormorant Garamond, serif"
_MONO = "DM Mono, monospace"


class Diagram:
    """A themed SVG canvas with drawing primitives."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._defs = []
        self._parts = []

    # -- primitives ---------------------------------------------------

    def add(self, markup):
        self._parts.append(markup)
        return self

    def define(self, markup):
        self._defs.append(markup)
        return self

    def rect(self, x, y, w, h, stroke=ACCENT, fill="none", rx=8, width=1.5):
        self._parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'
        )
        return self

    def line(self, x1, y1, x2, y2, stroke=BORDER, width=1.5, marker_end=None,
             marker_start=None):
        me = f' marker-end="url(#{marker_end})"' if marker_end else ""
        ms = f' marker-start="url(#{marker_start})"' if marker_start else ""
        self._parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{stroke}" stroke-width="{width}"{me}{ms}/>'
        )
        return self

    def circle(self, cx, cy, r, fill=ACCENT, stroke="none", width=1.5):
        self._parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{width}"/>'
        )
        return self

    def polygon(self, points, fill=ACCENT, stroke="none", width=0):
        pts = " ".join(f"{round(x, 2)},{round(y, 2)}" for x, y in points)
        sw = (
            f' stroke="{stroke}" stroke-width="{width}"'
            if stroke != "none" else ""
        )
        self._parts.append(f'<polygon points="{pts}" fill="{fill}"{sw}/>')
        return self

    def text(self, x, y, s, fill=TEXT, size=13, family=_MONO, anchor="middle",
             weight=400, style="normal", spacing=None):
        ls = f' letter-spacing="{spacing}"' if spacing is not None else ""
        self._parts.append(
            f'<text x="{x}" y="{y}" fill="{fill}" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" font-style="{style}" '
            f'text-anchor="{anchor}" dominant-baseline="central"{ls}>'
            f"{_escape(str(s))}</text>"
        )
        return self

    # -- output -------------------------------------------------------

    def svg(self):
        defs = f"<defs>{''.join(self._defs)}</defs>" if self._defs else ""
        return (
            f'<svg viewBox="0 0 {self.width} {self.height}" '
            f'width="{self.width}" xmlns="http://www.w3.org/2000/svg" '
            f'class="ntq-diagram" role="img">'
            f"{defs}{''.join(self._parts)}</svg>"
        )

    def __str__(self):
        return self.svg()


# -- reusable defs -------------------------------------------------------

def _arrowhead(name, color, orient="auto"):
    """An SVG marker arrowhead."""
    return (
        f'<marker id="{name}" markerWidth="9" markerHeight="9" '
        f'refX="7" refY="4.5" orient="{orient}" markerUnits="userSpaceOnUse">'
        f'<path d="M1,1 L8,4.5 L1,8 Z" fill="{color}"/></marker>'
    )


# =====================================================================
# Builders
# =====================================================================


def relation_diagram(left="ε", right="Δ", left_label=None, right_label=None,
                     width=520):
    """The ε↔Δ core symbol: violet glyphs joined by an amber double arrow.

    ``left``/``right`` are the glyphs; optional ``*_label`` render small
    captions beneath them. Works for any relation ``A ↔ B``.
    """
    height = 200 if (left_label or right_label) else 170
    cy = 92
    d = Diagram(width, height)

    ax0 = width * 0.40
    ax1 = width * 0.60

    d.define(
        f'<linearGradient id="ntq-arrow" gradientUnits="userSpaceOnUse" '
        f'x1="{ax0}" y1="0" x2="{ax1}" y2="0">'
        f'<stop offset="0" stop-color="{ACCENT_2}"/>'
        f'<stop offset="1" stop-color="{ACCENT_4}"/></linearGradient>'
    )

    left_x = width * 0.20
    right_x = width * 0.80

    # glyphs
    d.text(left_x, cy, left, fill=ACCENT, size=120, family=_SERIF, weight=600)
    d.text(right_x, cy, right, fill=ACCENT, size=120, family=_SERIF, weight=600)

    # double-headed arrow as a filled shape (robust across renderers,
    # and closer to the solid logo arrow than a stroked line + markers)
    hl, hh, sh = 26, 22, 8  # head length, head half-height, shaft half-height
    d.polygon([
        (ax0, cy),
        (ax0 + hl, cy - hh), (ax0 + hl, cy - sh),
        (ax1 - hl, cy - sh), (ax1 - hl, cy - hh),
        (ax1, cy),
        (ax1 - hl, cy + hh), (ax1 - hl, cy + sh),
        (ax0 + hl, cy + sh), (ax0 + hl, cy + hh),
    ], fill="url(#ntq-arrow)")

    # optional captions
    if left_label:
        d.text(left_x, cy + 78, left_label, fill=TEXT_DIM, size=13,
               family=_MONO, spacing="1")
    if right_label:
        d.text(right_x, cy + 78, right_label, fill=TEXT_DIM, size=13,
               family=_MONO, spacing="1")

    return d.svg()


def flow_diagram(steps, width=640, box_h=52):
    """A horizontal flow of labelled boxes joined by arrows.

    ``steps`` is a list of labels, or ``(label, color)`` tuples. Example::

        flow_diagram(["Objekt", "Renderer", "HTML"])
    """
    palette = [ACCENT, ACCENT_3, ACCENT_4, ACCENT_2]
    n = len(steps)
    height = box_h + 48
    cy = height / 2
    d = Diagram(width, height)
    d.define(_arrowhead("ntq-flow-head", TEXT_DIM, "auto"))

    gap = 34
    box_w = (width - gap * (n - 1)) / n
    x = 0
    for idx, step in enumerate(steps):
        if isinstance(step, (tuple, list)):
            label, color = step[0], step[1]
        else:
            label, color = step, palette[idx % len(palette)]
        y = cy - box_h / 2
        d.rect(x, y, box_w, box_h, stroke=color, fill=SURFACE_2, rx=8, width=1.5)
        d.text(x + box_w / 2, cy, label, fill=TEXT, size=13, family=_MONO)
        if idx < n - 1:
            ax1 = x + box_w + 4
            ax2 = x + box_w + gap - 4
            d.line(ax1, cy, ax2, cy, stroke=TEXT_DIM, width=1.5,
                   marker_end="ntq-flow-head")
        x += box_w + gap

    return d.svg()
